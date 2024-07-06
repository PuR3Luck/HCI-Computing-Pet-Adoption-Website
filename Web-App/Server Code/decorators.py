from typing import Callable
from flask import session, redirect
import sqlite3
import functools

def sql_wrapper(func: Callable):
  """First argument of the wrapped function should be the cursor object"""
  def wrapper(*args, **kwargs):
    conn = sqlite3.connect("pets.db")
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

def login_required(func: Callable):
  @functools.wraps(func)
  def check_login(*args, **kwargs):
    if (not session.get('logged_in')): # User has not logged in
      return redirect("/login")
    return func(*args, **kwargs)

  return check_login
