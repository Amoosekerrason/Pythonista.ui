try:
    from ui import *  # type: ignore
except ImportError:
    from ui_stub import *  # type: ignore
import datetime as dt
import calendar as cl
from typing import Callable
from result import *


class CalenderHeaderView(View):
    def __init__(self, parent_width, parrent_height):
        super().__init__()
        self.frame = (0, 0, parent_width, parrent_height / 6)
        self.background_color = "yellow"
        self.create_weekdays_label()

    def create_weekdays_label(self):
        days = "日 一 二 三 四 五 六".split()
        label_width = self.width / 7
        label_height = self.height
        for i, day in enumerate(days):
            label = Label()
            label.frame = (i * label_width, 0, label_width, label_height)
            label.text = day
            label.alignment = ALIGN_CENTER
            label.border_width = 0.7
            self.add_subview(label)


class CalenderContentView(View):

    def __init__(
        self,
        parent_width,
        parrent_height,
        year=dt.datetime.now().year,
        month=dt.datetime.now().month,
        on_date_selected: Callable = None,
    ):
        super().__init__()
        self.frame = (0, parrent_height / 6, parent_width,
                      parrent_height * 5 / 6)
        self.background_color = "pink"
        self.year, self.month = year, month
        self.create_dates_btns(year, month)
        self.previous_selected_btn = None
        self.selected_btn = None
        self.on_date_selected = on_date_selected

    def create_dates_btns(self, year, month):
        day, days = cl.monthrange(year, month)

        
        resorted_day_index = [6, 0, 1, 2, 3, 4, 5]  
        started_place_index = resorted_day_index.index(day)
        btn_title = 1

        for row in range(6):
            for col in range(7):
                label = Label()
                label.border_width = 0.7
                label.frame = (
                    self.width / 7 * col,
                    self.height / 6 * row,
                    self.width / 7,
                    self.height / 6,
                )
                self.add_subview(label)
                index = row * 7 + col
                if index < started_place_index:
                    continue

                if btn_title > days:
                    continue

                btn = Button(title=str(btn_title))
                btn.frame = (
                    self.width / 7 * col + 3,
                    self.height / 6 * row + 3,
                    self.width / 7 - 6,
                    self.height / 6 - 6,
                )
                btn.action = self.btn_clicked

                self.add_subview(btn)
                btn_title += 1

    def btn_clicked(self, sender):
        if self.previous_selected_btn:
            self.previous_selected_btn.background_color = None

        sender.background_color = "#9bf1ff"
        self.previous_selected_btn = sender
        self.selected_btn = sender
        if self.on_date_selected:
            self.on_date_selected(self.month, int(sender.title))


class CalenderView(View):

    def __init__(self, x=0, y=0,year=None,month=None, on_handle_date: Callable = None):
        super().__init__()
        self.frame = (x, y, CALENDER_WIDTH, CALENDER_HEIGHT)
        self.background_color = "blue"
        self.add_subview(CalenderHeaderView(self.width, self.height))
        self.add_subview(
            CalenderContentView(self.width,
                                self.height,
                                on_date_selected=self.date_selected))
        self.on_handle_date = on_handle_date

    def date_selected(self, month, date):
        if self.on_handle_date:
            Result = self.on_handle_date(month, date)
            if Result.is_ok():
                print("Succesed", Result.value)
            else:
                print("Failed", Result.error)

class SelectMonthView(View):
    def __init__(self,parent:View,x=0,y=0,):
        self.background_color='#80ae8d'
        self.frame=(x,y,parent.width,parent.height*1/4)

class InterfaceView(View):
    def __init__(self,x=0,y=0):
        super().__init__()
        self.background_color='#916aae'
        self.frame=(x,y,INTERFACE_WIDTH,INTERFACE_HEIGHT)
        self.add_subview(SelectMonthView(parent=self))


class EntryView(View):

    def __init__(self):
        super().__init__()
        self.name = f'{dt.datetime.now().month}月'
        self.background_color = "white"
        self.add_subview(
            CalenderView(x=CALENDER_X,
                         y=CALENDER_Y,
                         on_handle_date=self.handle_date))
        self.add_subview(InterfaceView(x=INTERFACE_X,y=INTERFACE_Y))
        self.handled_date = None

    def handle_date(self, month, date) -> Result[tuple[int, int], str]:
        try:
            self.handled_date = (month, int(date))
            return Ok((month, int(date)))
        except Exception as e:
            return Err(str(e))


class Program:

    @staticmethod
    def main():
        start = EntryView()

        start.present("fullscreen")


if __name__ == "__main__":
    SCREEN_WIDTH = 375
    SCREEN_HEIGHT = 603
    CALENDER_WIDTH = SCREEN_WIDTH
    CALENDER_HEIGHT = SCREEN_HEIGHT * 4 / 7
    CALENDER_X = 0
    CALENDER_Y = 0
    INTERFACE_WIDTH = SCREEN_WIDTH
    INTERFACE_HEIGHT=SCREEN_HEIGHT * 3/7
    INTERFACE_X=0
    INTERFACE_Y= CALENDER_HEIGHT
    Program.main()

