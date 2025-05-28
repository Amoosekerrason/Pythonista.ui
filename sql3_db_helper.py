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
    def __init__(self, db_path, db_queue):
        super().__init__(db_path, db_queue)

    def create_table(self):
        cur = self.conn.cursor()
        cur.execute(
            self.queue.create("arrangements_info", [
                ("id", "INTEGER", "PRIMARY KEY AUTOINCREMENT"),
                ("name", "TEXT", "NOT NULL"),
                ("gender", "TEXT"),
                ("seats", "INTEGER"),
                ("tables", "TEXT", "NOT NULL"),
                ("phoneNumber", "TEXT", "NOT NULL"),
                ("arrangementTime", "TIMESTAMP", "NOT NULL"),
                ("isSpecify", "INTEGER"),
                ("shoesOff", "INTEGER"),
                ("eventTime", "TIMESTAMP", "DEFAULT CURRENT_TIMESTAMP"),
                ("contacter", "TEXT")
            ]
            )
        )

        cur.execute(
            self.queue.create("employee_info", [
                ("id", "INTEGER", "UNIQUE NOT NULL"),
                ("name", "TEXT", "NOT NULL")
            ],
            )
        )
        self.conn.commit()
        cur.close()

    def insert_data(self, table, columns, values):
        return super().insert_data(table, columns, values)

    def update_data(self, table, set_values, where=None):
        return super().update_data(table, set_values, where)

    def delete_data(self, table, where=None):
        return super().delete_data(table, where)


def main():
    queue = SQL3DBqueue()
    db = SQL3DBHelper('database.db', queue)
    db.create_table()


if __name__ == '__main__':
    main()
