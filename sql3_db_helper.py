import sqlite3 as sql
from abstract_class import DBHelper, DBQueue
import os


class SQL3DBqueue(DBQueue):
    def create(self, table, columns):
        cols_str = ",".join(f" ".join(col) for col in columns)
        sql_str = f"CREATE TABLE IF NOT EXISTS {table} ({cols_str});"
        return sql_str

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

    def insert_data(self, queue):
        return super().insert_data(queue)

    def select_data(self, queue):
        return super().select_data(queue)

    def update_data(self, queue):
        return super().upload_data(queue)

    def delete_data(self, queue):
        return super().delete_data(queue)
