from db_utils import sql_wrapper
import sqlite3

@sql_wrapper
def login(cursor:sqlite3.Cursor, username:str, input_password:str) -> bool:
  """
    Checks if login is successful

    Args: 
      cursor: sqlite3 cursor object
      username: str, the username of the user
      password: str, the password of the user

    Returns:
      bool, True if the login is successful, False otherwise
  """

  password_tuple = cursor.execute("SELECT password FROM USER WHERE username = ?", (username,)).fetchone()

  # Check if username is inside the database
  if password_tuple is None: # This means that the username was not found in the database
    return False

  # User exists inside the database

  password = password_tuple[0]

  if input_password == password:
    return True
  else:
    return False

@sql_wrapper
def register(cursor: sqlite3.Cursor,username:str, password:str, contact_number:int) -> bool:
  """
    Registers a new user in the database

    Args:
      cursor: sqlite3 cursor object
      username: str, the username of the new user
      password: str, the password of the new user
      contact_number: int, the contact number of the new user

    Returns:
      bool, True if the registration is successful, False otherwise
  """ 
  if cursor.execute("SELECT COUNT(*) FROM USER WHERE username = ?", (username,)).fetchone() is not None: # Another user with the same username already exists
    return False
  
  cursor.execute("INSERT INTO USER(username, password, contact_number) VALUES (?, ?)", (username, password, contact_number))
  
  return True

@sql_wrapper
def change_password(cursor: sqlite3.Cursor,username:str, prev_password:str, new_password:str) -> bool:
  """
    Changes the password of the user after first validating that the user exists and the previous password is correct

    Args:
      cursor: sqlite3 cursor object
      username: str, username of the user
      prev_password: str, the previous password of the user
      new_password: str, the new password of the user
    
    Returns:
      bool, True if the password change is successful, False otherwise
  """

  password_tuple = cursor.execute("SELECT password FROM USER WHERE username = ?", (username,)).fetchone()

  if password_tuple is None: # User does not exists in the database
    return False 

  password = password_tuple[0]

  if password != prev_password: # Previous password is not correct stop the password change from occuring
    return False
  
  cursor.execute("UPDATE USER SET password = ? WHERE username = ?", (new_password, username))

  return True

@sql_wrapper
def delete_account(cursor: sqlite3.Cursor, username:str, password:str):
  """
    Deletes the user account from the database after validating the username and password purges all instances where user is referenced

    Args:
      cursor: sqlite3 cursor object
      username: str, the username of the user
      password: str, the password of the user

    Returns:
      bool, True if the account deletion is successful, False otherwise
  """
  if cursor.execute("SELECT COUNT(*) FROM USER WHERE username = ?", (username,)).fetchone()[0] == 0: # User does not exist in the database
    return False
  
  user_password = cursor.execute("SELECT password FROM USER WHERE username = ?", (username,)).fetchone()[0]

  if user_password != password:
    return False
  
  else:
    # Password is correct, delete the user account
    # Must also delete all their pets and all their requests

    # Get user_id
    user_id = cursor.execute("SELECT id FROM USER WHERE username = ?", (username,)).fetchone()[0]

    # Delete all pets associated with the user
    cursor.execute("DELETE FROM PETS WHERE owner_id = ?", (user_id,))

    # Delete all interest submissions by the user
    cursor.execute("DELETE FROM INTERESTS WHERE user_id = ?", (user_id,))

    # Delete the user account
    cursor.execute("DELETE FROM USER WHERE username = ?", (username,))

    return True