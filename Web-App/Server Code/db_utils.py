from typing import Callable
import sqlite3

def sql_wrapper(func: Callable):
  """First argument of the wrapped function should be the cursor object"""
  def wrapper(*args, **kwargs):
    conn = sqlite3.connect("pets.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    
    # Running the wrapped function
    try:
      result = func(cur, *args, **kwargs)
      conn.commit()
      return result
    finally:
      conn.close()
  return wrapper

# Example usage:
"""
@sql_wrapper()
def add_pet(cursor, name, age, type):
  cursor.execute("INSERT INTO pets (name, age, type) VALUES (?, ?, ?)", (name, age, type))
  return cursor.lastrowid

# Using the function
new_pet_id = add_pet("Fluffy", 3, "Cat")
print(f"New pet added with ID: {new_pet_id}")
"""