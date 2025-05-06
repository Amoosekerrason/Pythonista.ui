from abc import ABC, abstractmethod
# from ui_stub import *  # type: ignore
import enum
from sys import exit


class Gender(enum.Enum):
    male = 0
    female = 1


class ContentView(ABC):
    def __init__(self,):
        super().__init__()

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


class MainView():
    def __init__(self, content: ContentView):
        self.content = content

    def show(self):
        self.content.show_content()


class Program:
    @staticmethod
    def main():
        while True:
            MainView(OtherContent("John", 18, Gender.male.name)).show()
            print("1. born time")
            print("2. hobbit")
            match input("display what: "):
                case "1":
                    MainView(SomeContent(1991, 10)).show()
                    print()
                case "2":
                    MainView(AnotherContent("sleeping")).show()
                    print()

                case _:
                    exit()


if __name__ == "__main__":
    Program.main()
