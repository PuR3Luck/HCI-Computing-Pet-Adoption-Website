import pymongo
from typing import Tuple, Callable
from pymongo import MongoClient


def get_db(db_name:str):
    client = MongoClient('mongodb://localhost:27017/')
    db = client[db_name]
    return db, client

def close_connection(client):
    client.close()

def db_context_manager(db_name:str, func:Callable):
    def wrapper(*args, **kwargs):
        db, client = get_db(db_name)
        try:
            return func(db, *args, **kwargs)
        finally:
            close_connection(client)
    return wrapper

def adoption_db(func:Callable):
    return db_context_manager('adoption', func)

def user_db(func:Callable):
    return db_context_manager('user', func)