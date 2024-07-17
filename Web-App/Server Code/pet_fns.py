from decorators import sql_wrapper
import sqlite3

@sql_wrapper
def add_pet(cursor: sqlite3.Cursor,owner_id:int, name:str, age:int, fee:float, writeup:str, sex:str, type_id:int, photos):
  """
    Adds a new pet to the database.

    Args:
      cursor: sqlite3 cursor object
      owner_id: int, the ID of the user who is adding the pet
      name: str, the name of the pet
      age: int, the age of the pet
      fee: float, the adoption fee for the pet
      writeup: str, a description of the pet
      sex: str, the sex of the pet ('M' or 'F')
      type_id: int, the ID of the pet type (e.g. dog, cat, etc.)
      photos: photos of the pet, storing the photo paths as comma-separated values

    Returns:
      bool, True if the pet was successfully added, False otherwise
  """
  try:
    cursor.execute("INSERT INTO PET (user_id, name, age, fee, writeup, sex, type_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (owner_id, name, age, fee, writeup, sex, type_id))
    
    pet_id = cursor.lastrowid  # Get the ID of the inserted pet
        
    for file in photos:
      if file and file.filename:  # Check if file is actually present
        file_data = file.read()  # Read the file data
        cursor.execute("""INSERT INTO PET_PHOTOS (pet_id, photo_blob) VALUES (?, ?)""", 
                      (pet_id, file_data))
    
    return True
  except sqlite3.Error as e:
    print(f"Error occurred while adding pet: {e}")
    return False

@sql_wrapper
def edit_pet(cursor: sqlite3.Cursor, pet_id: int, name: str = None, age: int = None, fee: float = None, writeup: str = None, sex: str = None, type_id: int = None, photos=None):
  """
  Edits an existing pet in the database.
  Args:
    cursor: sqlite3 cursor object
    pet_id: int, the ID of the pet to be edited
    name: str, the new name of the pet (optional)
    age: int, the new age of the pet (optional)
    fee: float, the new adoption fee for the pet (optional)
    writeup: str, the new description of the pet (optional)
    sex: str, the new sex of the pet ('M' or 'F', optional)
    type_id: int, the new ID of the pet type (optional)
    photos: photos of the pet, storing the photo paths as comma-separated values (optional)
  Returns:
    bool, True if the pet was successfully edited, False otherwise
  """
  try:
    cursor.execute("""
      UPDATE PET 
      SET name = ?, age = ?, fee = ?, writeup = ?, sex = ?, type_id = ? 
      WHERE pet_id = ?
    """, (name, age, fee, writeup, sex, type_id, pet_id))

    if photos is not None:
      cursor.execute("DELETE FROM PET_PHOTOS WHERE pet_id = ?", (pet_id, ))

      for file in photos:
        if file and file.filename:
          file_content = file.read()
          cursor.execute("INSERT INTO PET_PHOTOS (pet_id, photo_blob) VALUES (?, ?)", (pet_id, sqlite3.Binary(file_content)))

    return True
  
  except sqlite3.Error as e:
    print(f"Error occurred while editing pet: {e}")
    return False
  
@sql_wrapper
def delete_pet(cursor: sqlite3.Cursor, pet_id: int) -> bool:
  """
  Deletes a pet from the database.

  Args:
    cursor: sqlite3 cursor object
    pet_id: int, the ID of the pet to be deleted

  Returns:
    bool, True if the pet was successfully deleted, False otherwise
  """

  try:
    cursor.execute("DELETE FROM PET WHERE pet_id = ?", (pet_id,))
    cursor.execute("DELETE FROM PET_PHOTOS WHERE pet_id = ?", (pet_id,))
    cursor.execute("DELETE FROM INTERESTS WHERE pet_id = ?", (pet_id,))
    return True
  
  except sqlite3.Error as e:
    print(f"Error occurred while deleting pet: {e}")
    return False