from abc import ABC, abstractmethod
from ui_stub import *  # type: ignore


class ContentView(ABC, View):
    def __init__(self, view_id: str, parent_section: 'SectionView', x=0, y=0):
        super().__init__()
        self.view_id = view_id
        self.parent_section = parent_section
        self.x, self.y = x, y

    @abstractmethod
    def show_content(self):
        pass


class SectionView(ABC, View):
    def __init__(self, view_id: str, parent_section: 'SectionView', x=0, y=0):
        super().__init__()
        self.view_id = view_id
        self.parent_section = parent_section
        self.x, self.y = x, y

    @abstractmethod
    def set_content(self):
        pass
