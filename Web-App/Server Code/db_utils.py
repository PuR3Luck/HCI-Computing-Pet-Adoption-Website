import pymongo
from typing import Tuple, Callable
from pymongo import MongoClient
import sqlite3

def mongo_wrapper(db_name, collection_name):
    def decorator(func):
        """First argument of the wrapped function should be the collection object"""
        def wrapper(*args, **kwargs):
            client = MongoClient('mongodb://localhost:27017/')
            db = client[db_name]
            collection = db[collection_name]
            
            # Running the wrapped function
            try:
                func(collection, *args, **kwargs) 

            # Closing the connection
            finally:
                client.close()

        return wrapper
    return decorator

def sqlite3_wrapper(db_name):
    def decorator(func):
        """First argument of the wrapped function should be the cursor object"""
        def wrapper(*args, **kwargs):
            conn = sqlite3.connect(db_name)
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