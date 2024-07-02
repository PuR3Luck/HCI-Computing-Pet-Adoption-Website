from db_utils import sql_wrapper
import sqlite3
from typing import List, Tuple

@sql_wrapper()
def view_interest(cursor: sqlite3.Cursor, pet_id: int) -> Tuple[List[Tuple[str, int]],bool]:
  """
    View all parties interested in a pet.

  Args:
      cursor: sqlite3 cursor object
      pet_id: int, the ID of the pet whose interests are to be viewed

  Returns:
    List[Tuple[str, int]], a list of tuples containing the username and contact number of interested parties
    bool, True if the interest was successfully viewed, False otherwise
  """

  try:
    cursor.execute("SELECT user_id FROM INTERESTS WHERE pet_id =?", (pet_id,))

    # Get all the user_ids of interested parties
    results = cursor.fetchall()
    user_ids = [result[0] for result in results]

    # Get the name and contact number of interested parties
    info_list = []

    for user_id in user_ids:
      cursor.execute("SELECT username, contact_number FROM USER WHERE user_id =?", (user_id,))
      info_list.append(cursor.fetchone())
    
    return info_list, True
  
  except sqlite3.Error as e:
    print(f"Error occurred while viewing interest: {e}")

    return [], False