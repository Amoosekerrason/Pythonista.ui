try:
    from ui import *  # type: ignore
except ImportError:
    from ui_stub import *  # type: ignore
import datetime as dt
import calendar as cl
from typing import Callable
from result import *
from abstract_class import *


class CalenderHeaderContentView(ContentView):

    def __init__(self, parent_width, parrent_height):
        self.frame = (0, 0, parent_width, parrent_height / 6)
        self.background_color = "yellow"
        self.show_content()

    def show_content(self):
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


class CalenderContentView(ContentView):

    def __init__(
        self,
        parent_width,
        parrent_height,
        year=None,
        month=None,
        day=None,
        on_date_selected: Callable = None,
    ):

        self.frame = (0, parrent_height / 6, parent_width,
                      parrent_height * 5 / 6)
        self.background_color = "pink"
        self.year, self.month, self.day = year, month, day
        self.show_content()
        self.previous_selected_btn = None
        self.selected_btn = None
        self.on_date_selected = on_date_selected

    def show_content(self):
        day, days = cl.monthrange(self.year, self.month)

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


class TopSectionView(SectionView):

    def __init__(self,
                 x=0,
                 y=0,
                 year=None,
                 month=None,
                 header_content: ContentView = None,
                 body_content: ContentView = None,
                 on_handle_date: Callable = None):
        self.frame = (x, y, TOP_SECTION_WIDTH, TOP_SECTION_HEIGHT)
        self.background_color = "blue"
        self.header_content = header_content
        self.body_content = body_content
        self.on_handle_date = on_handle_date

    def date_selected(self, month, date):
        if self.on_handle_date:
            res = self.on_handle_date(month, date)
            if res.is_ok():
                print("Succesed", res.val)
            else:
                print("Failed", res.err)


class SelectMonthSectionView(SectionView):

    def __init__(
        self,
        x=0,
        y=0,
    ):
        self.background_color = '#80ae8d'
        self.frame = (x, y, BELOW_SECTION_WIDTH, BELOW_SECTION_HEIGHT * 1 / 4)


class BelowSectionView(SectionView):

    def __init__(self, x=0, y=0):
        self.background_color = '#916aae'
        self.frame = (x, y, BELOW_SECTION_WIDTH, BELOW_SECTION_HEIGHT)
        self.interface_section_list = []


class MainSectionView(SectionView):

    def __init__(self, top_section: SectionView = None, below_section: SectionView = None):
        self.name = f'{dt.datetime.now().month}月'
        self.background_color = "white"
        self.top_section = top_section
        self.below_section = below_section
        self.handled_date = None

    def set_top_section(self, content=SectionView):
        self.top_section = content
        self.add_subview(self.top_section)

    def set_below_section(self, content=SectionView):
        self.below_section = content
        self.add_subview(self.below_section)

    def handle_date(self, month, date) -> Result[tuple[int, int], str]:
        try:
            self.handled_date = (month, int(date))
            return Ok((month, int(date)))
        except Exception as e:
            return Err(str(e))


class Program:

    def entry_screen(self, main_section: SectionView):
        top_section = TopSectionView(
            x=TOP_SECTION_X, y=TOP_SECTION_Y, on_handle_date=main_section.handle_date)
        top_content = self.show_calender(top_section, dt.datetime.now(
        ).year, dt.datetime.now().month, dt.datetime.now().day)

        below_section = BelowSectionView(x=BELOW_SECTION_X, y=BELOW_SECTION_Y)
        below_content = self.show_interface(below_section)

        main_section.set_top_section(top_content)
        main_section.set_below_section(below_content)

    def show_calender(self, top_section: SectionView, year, month,
                      day) -> SectionView:

        header_view = CalenderHeaderContentView(top_section.width,
                                                top_section.height)
        body_view = CalenderContentView(top_section.width,
                                        top_section.height,
                                        year=year,
                                        month=month,
                                        day=day,
                                        on_date_selected=top_section.date_selected)

        top_section.header_content = header_view
        top_section.body_content = body_view
        top_section.add_subview(top_section.header_content)
        top_section.add_subview(top_section.body_content)
        return top_section

    def show_interface(self,
                       below_section: SectionView) -> SectionView:
        select_month_section = SelectMonthSectionView()
        below_section.interface_section_list.append(select_month_section)
        for view in below_section.interface_section_list:
            below_section.add_subview(view)
        return below_section

    def present(self, main_section: MainSectionView):
        main_section.present("fullscreen")

    @staticmethod
    def main():
        program = Program()
        main_section = MainSectionView()
        program.entry_screen(main_section)
        program.present(main_section)


if __name__ == "__main__":
    SCREEN_WIDTH = 375
    SCREEN_HEIGHT = 603
    TOP_SECTION_WIDTH = SCREEN_WIDTH
    TOP_SECTION_HEIGHT = SCREEN_HEIGHT * 4 / 7
    TOP_SECTION_X = 0
    TOP_SECTION_Y = 0
    BELOW_SECTION_WIDTH = SCREEN_WIDTH
    BELOW_SECTION_HEIGHT = SCREEN_HEIGHT * 3 / 7
    BELOW_SECTION_X = 0
    BELOW_SECTION_Y = TOP_SECTION_HEIGHT
    Program.main()
