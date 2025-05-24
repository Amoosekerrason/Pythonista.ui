import sqlite3 as sql
from abstract_class import DBHelper, DBQueue
import os


class SQL3DBHelper(DBHelper):
    def __init__(self, db_path):
        super().__init__(db_path)

    def load_data(self):
        return super().load_data()

    def write_data(self):
        return super().write_data()
