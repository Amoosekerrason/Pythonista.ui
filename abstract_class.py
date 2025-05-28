try:
    from ui import *  # type: ignore
except ImportError:
    from ui_stub import *  # type: ignore
from abc import ABC, abstractmethod

from typing import Optional, Dict, Any
import sqlite3 as sql


class ContentView(ABC, View):
    def __init__(self, view_id: str, parent_section: "SectionView" = None, x=0, y=0):
        super().__init__()
        self.view_id = view_id
        self.parent_section = parent_section
        self.x, self.y = x, y

    @abstractmethod
    def show_content(self):
        pass


class SectionView(ABC, View):
    def __init__(self, view_id: str, parent_section: "SectionView" = None, x=0, y=0):
        super().__init__()
        self.view_id = view_id
        self.parent_section = parent_section
        self.x, self.y = x, y

    @abstractmethod
    def set_content(self):
        pass


class DBQueue(ABC):

    @abstractmethod
    def create(
        self, table: str, columns: list[tuple[str, str, str]]
    ):  # columns type mean:(col_name,col_type,col_condition)
        pass

    @abstractmethod
    def insert(self, table: str, columns: list[str], values: list[Any]):
        pass

    @abstractmethod
    def select(
        self, table: str, columns: list[str], where: Optional[Dict[str, Any]] = None
    ):
        pass

    @abstractmethod
    def update(
        self,
        table: str,
        set_values: Dict[str, Any],
        where: Optional[Dict[str, Any]] = None
    ):
        pass

    @abstractmethod
    def delete(self, table: str, where: Optional[Dict[str, Any]] = None):
        pass


class DBHelper(ABC):
    def __init__(self, db_path: str, db_queue: DBQueue):
        self.conn = sql.connect(db_path)
        self.queue = db_queue

    @abstractmethod
    def create_table(self):
        pass

    @abstractmethod
    def insert_data(self, table: str, columns: list[str], values: list[Any]):
        pass

    @abstractmethod
    def select_data(self, table: str, columns: list[str], where: Optional[Dict[str, Any]] = None):
        pass

    @abstractmethod
    def update_data(self, table: str,
                    set_values: Dict[str, Any],
                    where: Optional[Dict[str, Any]] = None):
        pass

    @abstractmethod
    def delete_data(self, table: str, where: Optional[Dict[str, Any]] = None):
        pass
