from db_utils import sql_wrapper
import sqlite3

@sql_wrapper()
def submit_interest(cursor: sqlite3.Cursor, user_id: int, pet_id: int) -> bool:
  """
    Submits an interest for a pet by a user.

    Args:
      cursor: sqlite3 cursor object
      user_id: int, the ID of the user submitting the interest
      pet_id: int, the ID of the pet the user is interested in
    
    Returns:
      bool, True if the interest was successfully submitted, False otherwise
  """
  try:
    cursor.execute("INSERT INTO INTERESTS (user_id, pet_id) VALUES (?, ?)", (user_id, pet_id))
    return True
  except sqlite3.Error as e:
    print(f"Error occurred while submitting interest: {e}")
    return False

@sql_wrapper()
def delete_interest(cursor: sqlite3.Cursor, user_id: int, pet_id: int) -> bool:
  """
    Delete a submission of interest for a pet by a user.

    Args:
      cursor: sqlite3 cursor object
      user_id: int, the ID of the user whose interest is to be deleted
      pet_id: int, the ID of the pet whose interest is to be deleted

    Returns:
      bool, True if the interest was successfully deleted, False otherwise
  """

  try:
    cursor.execute("DELETE FROM INTERESTS WHERE user_id = ? AND pet_id = ?", (user_id, pet_id))
    return True
  
  except sqlite3.Error as e:
    print(f"Error occurred while deleting interest: {e}")
    return False