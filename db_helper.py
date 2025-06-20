import sqlite3
from typing import List, Tuple, Any, Optional

class SQLiteHelper:
    def __init__(self, db_name: str):
        self.db_name = db_name

    def connect(self):
        return sqlite3.connect(self.db_name)

    def create_table(self, table_name: str, columns: str):
        """
        columns: "id INTEGER PRIMARY KEY, name TEXT, age INTEGER"
        """
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})")
            conn.commit()

    def drop_table(self, table_name: str):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
            conn.commit()

    def insert(self, table_name: str, columns: List[str], values: Tuple[Any, ...]):
        placeholders = ", ".join(["?"] * len(values))
        cols = ", ".join(columns)
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(f"INSERT INTO {table_name} ({cols}) VALUES ({placeholders})", values)
            conn.commit()

    def read(self, query: str, params: Optional[Tuple[Any, ...]] = None) -> List[Tuple]:
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            return cursor.fetchall()

    def update(self, table_name: str, updates: str, condition: str, params: Tuple[Any, ...]):
        """
        updates: "name = ?, age = ?"
        condition: "id = ?"
        """
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(f"UPDATE {table_name} SET {updates} WHERE {condition}", params)
            conn.commit()

    def delete(self, table_name: str, condition: str, params: Tuple[Any, ...]):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM {table_name} WHERE {condition}", params)
            conn.commit()

    def table_exists(self, table_name: str) -> bool:
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name=?;",
                (table_name,)
            )
            return cursor.fetchone() is not None
