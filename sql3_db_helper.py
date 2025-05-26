import sqlite3 as sql
from abstract_class import DBHelper, DBQueue
import os


class SQL3DBqueue(DBQueue):
    def create(self, table, columns):
        cols_str = ",".join(f" ".join(col) for col in columns)
        sql_str = f"CREATE TABLE IF NOT EXISTS {table} ({cols_str});"
        return sql_str

    def insert(self, table, columns, values):
        cols_str = ",".join(columns)
        values_str = ",".join(values)
        sql_str = f"INSERT INTO {table} ({cols_str} VALUES ({values_str}));"
        return sql_str

    def update(self, table, set_values, where=None):
        set_values_list = []
        for key, val in set_values.items():
            set_values_list.append(f"{key} = {val}")
        set_values_str = ",".join(set_values_list)
        if where:
            sql_str = f"UPDATE {table} SET {set_values_str} WHERE {where}"
        else:
            sql_str = f"UPDATE {table} SET {set_values_str}"
        return sql_str

    def delete(self, table, where=None):
        return super().delete(table, where)

    def select(self, table, columns, where=None):
        return super().select(table, columns, where)


class SQL3DBHelper(DBHelper):
    def __init__(self, db_path):
        super().__init__(db_path)

    def create_table(self, queue):
        return super().create_table(queue)

    def insert_data(self, queue):
        return super().insert_data(queue)

    def select_data(self, queue):
        return super().select_data(queue)

    def update_data(self, queue):
        return super().upload_data(queue)

    def delete_data(self, queue):
        return super().delete_data(queue)
