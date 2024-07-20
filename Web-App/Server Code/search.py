from decorators import sql_wrapper
from typing import List, Tuple, Optional
import dataclasses
import sqlite3
import base64

@dataclasses.dataclass
class filter_properties:
  from_user: Optional[int] = None
  min_age: Optional[int] = None
  max_age: Optional[int] = None
  min_fee: Optional[int] = None
  max_fee: Optional[int] = None
  sex: Optional[str] = None
  type: Optional[str] = None

@dataclasses.dataclass
class pet_properties:
   id: int
   name: str
   age: int
   fee: float
   writeup: str
   sex: str
   pet_type: str
   photos: List[str]

@dataclasses.dataclass
class maximum_values:
   age: int
   price: int


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
      cursor.execute("SELECT type_id FROM TYPES WHERE type =?", (type,))

      result = cursor.fetchone()

      return result[0], True
    
  except sqlite3.Error as e:
      print(f"Error occurred while converting type: {e}")
      return None, False
  
@sql_wrapper
def convert_type_id_to_str(cursor: sqlite3.Cursor, type_id: int) -> Tuple[Optional[str], bool]:
  """
  Converts the given integer `type_id` to a string representation.

  Args:
    cursor (sqlite3.Cursor): The database cursor object.
    type_id (int): The integer value to convert to a string.
  """

  try:
      cursor.execute("SELECT type FROM TYPES WHERE type_id =?", (type_id,))

      result = cursor.fetchone()

      return result[0], True
  
  except sqlite3.Error as e:
      print(f"Error occurred while converting type: {e}")
      return None, False

  
@sql_wrapper
def search(cursor: sqlite3.Cursor, filters: filter_properties, exclude_user: bool) -> List[int]:
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
  if filters.from_user is not None:
    if exclude_user:
      query += "NOT user_id = " + str(filters.from_user) + " AND "
    else:
      query += "user_id = " + str(filters.from_user) + " AND "
 
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
    type_id, success = convert_type_str_to_id(filters.type)
    if success:
        query += "type_id = " + str(type_id)
 
  query = query.rstrip(" AND ") # Remove trailing " AND "
 
  cursor.execute(query)
 
  results = cursor.fetchall() # results is a list of tuples of ints
 
  pet_ids = [result[0] for result in results]
 
  return pet_ids

@sql_wrapper
def fetch(cursor: sqlite3.Cursor, pet_id: int) -> pet_properties:
  """
    Fetches the pet properties for the given pet ID.

    Args:
      cursor (sqlite3.Cursor): The database cursor object
      pet_id (int): The ID of the pet to fetch.

    Returns:
        pet_properties: A dataclass containing the pet properties.
  """
  pet_data = cursor.execute("SELECT name, age, fee, writeup, sex, type_id FROM PET WHERE pet_id = ?", (pet_id,)).fetchone()
  pet_photos = cursor.execute("SELECT photo_blob FROM PET_PHOTOS WHERE pet_id = ?", (pet_id, )).fetchall()
  pet_photos = [base64.b64encode(photo[0]).decode("utf-8") for photo in pet_photos]

  pet_name = pet_data[0]
  pet_age = pet_data[1]
  pet_fee = pet_data[2]
  pet_writeup = pet_data[3]
  pet_sex = pet_data[4]
  pet_type_id = pet_data[5]
  pet_type = convert_type_id_to_str(pet_type_id)[0]

  return_value = pet_properties(
    id=pet_id,
    name=pet_name,
    age=pet_age,
    fee=pet_fee,
    writeup=pet_writeup,
    sex=pet_sex,
    pet_type=pet_type,
    photos=pet_photos
  )

  return return_value


@sql_wrapper
def get_maximum_values(cursor: sqlite3.Cursor) -> maximum_values:
  """
    Fetches the maximum values for age and fee from the database.
  """
  if cursor.execute("SELECT COUNT(*) FROM PET").fetchone()[0] == 0:
    return maximum_values(
      age=0,
      price=0
    )
  
  max_age = cursor.execute("SELECT MAX(age) FROM PET").fetchone()[0]
  max_price = cursor.execute("SELECT MAX(fee) FROM PET").fetchone()[0]

  return_value = maximum_values(
    age=max_age,
    price=max_price
  )

  return return_value