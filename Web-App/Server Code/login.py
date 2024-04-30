from db_utils import sql_wrapper

@sql_wrapper
def login(cursor, username:str, input_password:str) -> bool:
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

  # User exists inside the

  password = password_tuple[0]

  if input_password == password:
    return True
  else:
    return False

@sql_wrapper
def register(cursor,username:str, password:str) -> bool:
  """
    Registers a new user in the database

    Args:
      cursor: sqlite3 cursor object
      username: str, the username of the new user
      password: str, the password of the new user

    Returns:
      bool, True if the registration is successful, False otherwise
  """ 
  if cursor.execute("SELECT COUNT(*) FROM USER WHERE username = ?", (username,)).fetchone() is not None: # Another user with the same username already exists
    return False
  
  cursor.execute("INSERT INTO USER(username, password) VALUES (?, ?)", (username, password))
  
  return True

@sql_wrapper
def change_password(cursor,username:str, prev_password:str, new_password:str) -> bool:
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
def delete_account(cursor, username, password):
  """
    Deletes the user account from the database after validating the username and password purges all instances where user is referenced

    Args:
      cursor: sqlite3 cursor object
      username: str, the username of the user
      password: str, the password of the user

    Returns:
      bool, True if the account deletion is successful, False otherwise
"""

  raise NotImplementedError