from db_utils import sql_wrapper
from typing import List, Tuple, Optional
import dataclasses
import sqlite3

@dataclasses.dataclass
class filter_properties:
  from_users: Optional[List[int]] # List of user ids
  min_age: Optional[int]
  max_age: Optional[int]
  min_fee: Optional[int]
  max_fee: Optional[int]
  sex: Optional[str]
  type: Optional[str]


@sql_wrapper
def convert_type_str_to_id(cursor: sqlite3.Cursor, type: str) -> Tuple[Optional[int], bool]:
  """
  Converts the given string `type` to an integer representation.

  Args:
    cursor (sqlite3.Cursor): The database cursor object.
    type (str): The string value to convert to an integer.

  Returns:
    Tuple[Optional[int], bool]: A tuple containing the integer representation of the input `type` string and a boolean indicating success.
  """
  try:
      cursor.execute("SELECT type_id FROM TYPE WHERE type =?", (type,))

      result = cursor.fetchone()

      return result[0], True
    
  except sqlite3.Error as e:
      print(f"Error occurred while converting type: {e}")
      return None, False
  
@sql_wrapper
def search(cursor: sqlite3.Cursor, filters:filter_properties) -> List[int]:
 """
   Searches the database using the provided filter properties.

   Operates by incrementally building a query based on the filter properties provided.

   Args:
     cursor (sqlite3.Cursor): The database cursor object.
     filters (filter_properties): A dataclass containing the filter properties to use for the search.

   Returns:
     List[int]: A list of integers representing the pet IDs that match the search criteria.
 """

 query = "SELECT pet_id FROM PET WHERE "

 # User filter
 if filters.from_users is not None:
    add_string = "user_id IN (" + ",".join(str(user_id) for user_id in filters.from_users) + ") AND "
    query += add_string

 # Age filter
 if filters.min_age is not None:
    query += "age >= " + str(filters.min_age) + " AND "
 if filters.max_age is not None:
    query += "age <= " + str(filters.max_age) + " AND "

 # Fee filter
 if filters.min_fee is not None:
    query += "fee >= " + str(filters.min_fee) + " AND "
 if filters.max_fee is not None:
    query += "fee <= " + str(filters.max_fee) + " AND "

 # Sex filter
 if filters.sex is not None:
    query += "sex = '" + filters.sex + "' AND "

 # Type filter
 if filters.type is not None:
    type_id, success = convert_type_str_to_id(cursor, filters.type)
    if success:
        query += "type_id = " + str(type_id)

 query = query.rstrip(" AND ") # Remove trailing " AND "

 cursor.execute(query)

 results = cursor.fetchall() # results is a list of tuples of ints

 pet_ids = [result[0] for result in results]

 return pet_ids
 