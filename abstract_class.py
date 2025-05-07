from abc import ABC, abstractmethod
from ui_stub import *  # type: ignore


class ContentView(ABC, View):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def show_content(self):
        pass


class SectionView(ABC, View):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def set_content(self):
        pass
