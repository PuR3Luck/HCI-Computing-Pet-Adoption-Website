import pymongo
from typing import Callable
from pymongo import MongoClient
import sqlite3
import functools

def sql_wrapper():
    def decorator(func:Callable):
        """First argument of the wrapped function should be the cursor object"""
        def wrapper(*args, **kwargs):
            conn = sqlite3.connect("pets.db")
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            
            # Running the wrapped function
            try:
                func(cur, *args, **kwargs) 

            # Closing the connection
            finally:
                conn.commit()
                conn.close()

        return wrapper
    return decorator