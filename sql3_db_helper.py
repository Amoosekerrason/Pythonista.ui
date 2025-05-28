import sqlite3 as sql
from abstract_class import DBHelper, DBQueue


class SQL3DBqueue(DBQueue):
    def create(self, table, columns):
        # columns type mean:(col_name,col_type,col_conditions)
        cols_str = ", ".join(f" ".join(col) for col in columns)
        return f"CREATE TABLE IF NOT EXISTS {table} ({cols_str});"

    def insert(self, table, columns, values):
        cols_str = ", ".join(columns)
        placeholder = ", ".join(["?"] * len(values))
        sql_str = f"INSERT INTO {table} ({cols_str}) VALUES ({placeholder}));"
        return sql_str, values

    def select(self, table, columns, where=None):
        cols_str = ", ".join(columns)
        sql_str = f"SELECT {cols_str} FROM {table};"
        params = []
        if where:
            where_clauses = []
            for key, value in where.items():
                where_clauses.append(f"{key} = ?")
                params.append(value)
            where_str = " AND ".join(where_clauses)
            sql_str += f" WHERE {where_str}"
        return sql_str, params

    def update(self, table, set_values, where=None):
        set_clauses = [f"{col} = ?" for col in set_values]
        set_values_list = list(set_values.values())

        sql_str = f"UPDATE {table} SET {', '.join(set_clauses)}"

        params = set_values_list

        if where:
            where_clauses = [f"{col} = ?" for col in where]
            where_values = list(where.values())
            sql_str += f" WHERE {' AND '.join(where_clauses)}"
            params.extend(where_values)

        return sql_str, params

    def delete(self, table, where=None):
        sql_str = f"DELETE FROM {table}"
        params = []

        if where:
            where_clauses = [f"{col} = ?" for col in where]
            where_values = list(where.values())
            sql_str += f" WHERE {' AND '.join(where_clauses)}"
            params.extend(where_values)

        return sql_str, params


class SQL3DBHelper(DBHelper):
    def __init__(self, db_path):
        super().__init__(db_path)

    def create_table(self, queue):
        cur = self.conn.cursor()
        cur.execute(
            queue.create(
                "arrangements info",
                [
                    ("id", "INTERGER", "PRIMARY KEY NOT NULL AUTOINCREMENT"),
                    ("name", "TEXT", "NOT NULL"),
                    ("gender", "TEXT"),
                    ("seats", "INTERGER"),
                    ("tables", "TEXT", "NOT NULL"),
                    ("phoneNumber", "TEXT", "NOT NULL"),
                    ("when", "TIMESTAMP", "NOT NULL"),
                    ("isSpecify", "INTERGER"),
                    ("shoesOff", "INTERGER"),
                    ("eventTime", "TIMESTAMP", "DEFAULT CURRENT_TIMESTAMP"),
                    ("representative", "TEXT"),
                ],
            )
        )
        cur.execute(
            queue.create(
                "employee info",
                [("id", "INTERGER", "UNIQUE NOT NULL"), ("name", "TEXT", "NOT NULL")],
            )
        )
        self.conn.commit()
        cur.close()

    def insert_data(self, queue):
        return super().insert_data(queue)

    def select_data(self, queue):
        return super().select_data(queue)

    def update_data(self, queue):
        return super().update_data(queue)

    def delete_data(self, queue):
        return super().delete_data(queue)
