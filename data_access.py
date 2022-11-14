"""Minimal wrapper for shelve to cover my most commonly used operations"""
import shelve
from typing import Any


def get_db_keys() -> list[str]:
    """Helper function to get list of db keys"""
    with shelve.open('data/db/data_store') as db:
        keys_list = list(db.keys())

    return keys_list


def load_from_db(db_key_string: str) -> Any:
    """Helper function to load data from db using a key string"""
    with shelve.open('data/db/data_store') as db:
        loaded_item = db[db_key_string]

    return loaded_item


def save_to_db(db_key_string: str, data_to_save: object) -> None:
    """Helper function to save data to db using a key string"""
    with shelve.open('data/db/data_store') as db:
        db[db_key_string] = data_to_save

    return


def report_shelf_contents() -> None:
    """Helper function to report top level contents of the shelf"""
    for key in get_db_keys():
        print(f"{key}: ")
        print(f"{len(load_from_db(db_key_string=key))} items stored.")
        print("\n")
