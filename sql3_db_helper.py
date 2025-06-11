import sqlite3 as sql
from abstract_class import DBHelper, DBQueue
from result import *
import logging
logger = logging.getLogger(__name__)


class SQL3DBqueue(DBQueue):
    def __init__(self):
        logger.info("built SQL3DBqueue")

    def create(self, table, columns):
        # columns type mean:(col_name,col_type,col_conditions)
        cols_str = ", ".join(f" ".join(col) for col in columns)
        return f"CREATE TABLE IF NOT EXISTS {table} ({cols_str})"

    def insert(self, table, columns, values):
        cols_str = ", ".join(columns)
        placeholder = ", ".join(["?"] * len(values))
        sql_str = f"INSERT INTO {table} ({cols_str}) VALUES ({placeholder})"
        return sql_str, values

    def select(self, table, columns, where=None, orderby=None):
        cols_str = ", ".join(columns)
        sql_str = f"SELECT {cols_str} FROM {table}"
        params = []
        if where:
            where_clauses = []
            for key, value in where.items():
                where_clauses.append(f"{key} = ?")
                params.append(value)
            where_str = " AND ".join(where_clauses)
            sql_str += f" WHERE {where_str}"
        if isinstance(orderby, list):
            sql_str += " ORDER BY "+",".join(orderby)
        else:
            sql_str += f" ORDER BY {orderby}"
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
        self.arrangements_info_table = "arrangements_info"
        self.employee_info_table = "employee_info"
        logger.info("built SQL3DBHelper")

    def _get_cursor(self):
        try:
            return Ok(self.conn.cursor())
        except Exception as e:
            return Err(f"get cursor gone wrong: {e}")

    def create_table(self):
        cur = self._get_cursor()
        if cur.is_ok():
            cur.val.execute(
                self.queue.create(self.arrangements_info_table, [
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
                    ("contacter", "TEXT"),
                    ("memo", "TEXT")
                ]
                )
            )

            cur.val.execute(
                self.queue.create(self.employee_info_table, [
                    ("id", "INTEGER", "UNIQUE NOT NULL"),
                    ("name", "TEXT", "NOT NULL")
                ],
                )
            )
            self.conn.commit()
            cur.val.close()
        else:
            logger.error(cur.err)
            return cur

    def insert_data(self, table, columns, values):
        cur = self._get_cursor()
        if cur.is_ok():
            try:
                sql_str, values = self.queue.insert(table, columns, values)
                cur.val.execute(sql_str, values)
                self.conn.commit()
                return Ok("insert done")
            except Exception as e:
                return Err(f"insert failed: {e}")
            finally:
                cur.val.close()
        else:
            logger.error(cur.err)
            return cur

    def select_data(self, table, columns, where=None, orderby=None):
        cur = self._get_cursor()
        if cur.is_ok():

            try:
                sql_str, params = self.queue.select(
                    table, columns, where, orderby)
                res = cur.val.execute(sql_str, params)
                result = res.fetchall()
                return Ok(result)

            except Exception as e:
                return Err(f'select failed: {e}')
            finally:
                cur.val.close()
        else:
            logger.error(cur.err)
            return cur

    def update_data(self, table, set_values, where=None):
        cur = self._get_cursor()
        if cur.is_ok():
            try:
                sql_str, params = self.queue.update(table, set_values, where)
                cur.val.execute(sql_str, params)
                self.conn.commit()
                return Ok("update done")
            except Exception as e:
                return Err(f"update failed: {e}")
            finally:
                cur.val.close()
        else:
            logger.error(cur.err)
            return cur

    def delete_data(self, table, where=None):
        cur = self._get_cursor()
        if cur.is_ok():
            try:
                sql_str, params = self.queue.delete(table, where)
                cur.val.execute(sql_str, params)
                self.conn.commit()
                return Ok("delete done")
            except Exception as e:
                return Err(f"delete failed: {e}")
            finally:
                cur.val.close()
        else:
            logger.error(cur.err)
            return cur


def main():
    queue = SQL3DBqueue()
    db = SQL3DBHelper('database.db', queue)
    db.create_table()


if __name__ == '__main__':
    main()
