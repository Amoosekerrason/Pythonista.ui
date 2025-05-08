from abc import ABC, abstractmethod
# from ui_stub import *  # type: ignore
import enum
from sys import exit


class Gender(enum.Enum):
    male = 0
    female = 1


class ContentView(ABC):
    def __init__(self, id: str = "0"):
        self.id = id

    @abstractmethod
    def show_content(self,):
        pass


class SomeContent(ContentView):
    def __init__(self, year: int, month: int):
        self.year = year
        self.month = month

    def show_content(self):
        print(f"I was born in {self.year} {self.month}")


class OtherContent(ContentView):
    def __init__(self, name: str, age: int, gender: str):
        self.name = name
        self.age = age
        self.gender = gender

    def show_content(self):
        print(
            f"my name is {self.name}. I'm a {self.age} years old {self.gender}.")


class AnotherContent(ContentView):
    def __init__(self, intro: str):
        self.intro = intro

    def show_content(self):
        print(f"I'm good at {self.intro}")


class MainView(ContentView):
    def __init__(self, content: ContentView):
        super().__init__()
        self.content = content

    def show_content(self):
        self.content.show_content()


class Program:
    @staticmethod
    def main():
        main = MainView(SomeContent(1991, 10))
        print(main.id)
        main.id = "0-1"
        print(main.id)
        newMain = MainView(SomeContent(1991, 15), id="0-2")
        print(newMain.id)


if __name__ == "__main__":
    Program.main()
