import sqlite3 as sql
from abstract_class import DBHelper, DBQueue
import os


class SQL3DBqueue(DBQueue):
    def create(self, table_name, columns):
        return super().create(table_name, columns)

    def insert(self, table, columns, values):
        return super().insert(table, columns, values)

    def update(self, table, set_values, where=None):
        return super().update(table, set_values, where)

    def delete(self, table, where=None):
        return super().delete(table, where)

    def select(self, table, columns, where=None):
        return super().select(table, columns, where)


class SQL3DBHelper(DBHelper):
    def __init__(self, db_path):
        super().__init__(db_path)

    def load_data(self):
        return super().load_data()

    def write_data(self):
        return super().write_data()
