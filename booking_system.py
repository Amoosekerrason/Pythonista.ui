try:
    from ui import *  # type: ignore
except ImportError:
    from ui_stub import *  # type: ignore
import datetime as dt
import calendar as cl
from result import *
from abstract_class import *


class CalendarHeaderContentView(ContentView):

    def __init__(self, view_id, parent_section):
        super().__init__(view_id, parent_section)
        self.background_color = "yellow"
        self.show_content()

    def show_content(self):
        if self.parent_section:
            self.frame = (self.x, self.y, self.parent_section.width,
                          self.parent_section.height / 6)
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


class CalendarContentView(ContentView):

    def __init__(
        self,
        view_id,
        parent_section,
        year=None,
        month=None,
        day=None,
    ):
        super().__init__(view_id, parent_section)
        self.parent_section = parent_section
        self.background_color = "pink"
        self.year, self.month, self.day = year, month, day
        self.show_content()
        self.previous_selected_btn = None

    def show_content(self):
        if not self.parent_section:
            return
        if self.subviews:
            for view in self.subviews:
                self.remove_subview(view)
        self.frame = (self.x, self.parent_section.height / 6,
                      self.parent_section.width,
                      self.parent_section.height * 5 / 6)
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
        sender.background_color = "#9bf1ff"
        if self.previous_selected_btn:
            self.previous_selected_btn.background_color = None

        self.previous_selected_btn = sender
        self.selected_btn = sender
        if self.parent_section:
            self.parent_section.handle_date(
                self.year, self.month, int(sender.title))


class TopSectionView(SectionView):

    def __init__(
        self,
        view_id,
        parent_section,
        year=None,
        month=None,
        header_content: ContentView = None,
        body_content: ContentView = None,
    ):
        super().__init__(view_id, parent_section)

        self.parent_section = parent_section
        self.background_color = "blue"
        self.header_content = header_content
        self.body_content = body_content
        self.set_content()

    def set_content(self):
        if not self.parent_section:
            return
        self.frame = (self.x, self.y, TOP_SECTION_WIDTH, TOP_SECTION_HEIGHT)
        if self.header_content:
            self.add_subview(self.header_content)
        if self.body_content:
            self.add_subview(self.body_content)

    def handle_date(self, year, month, date):
        if self.parent_section:
            res = self.parent_section.handle_date(year, month, date)
            if res.is_ok():
                print("Succesed", res.val)
            else:
                print("Failed", res.err)


class CRUDContentView(ContentView):

    def __init__(self, view_id, parent_section):
        super().__init__(view_id, parent_section)

    def show_content(self):
        return super().show_content()


class CRUDSectionView(SectionView):

    def __init__(self, view_id, parent_section):
        super().__init__(view_id, parent_section)
        self.set_content()

    def set_content(self):
        self.frame = (self.x, self.y, self.parent_section.width,
                      self.parent_section.height * 3 / 4)


class SelectMonthContentView(ContentView):

    def __init__(
        self,
        view_id,
        parent_section,
    ):
        super().__init__(view_id, parent_section)
        self.show_content()

    def show_content(self):
        if self.parent_section:
            self.frame = (self.x, self.y, self.parent_section.width,
                          self.parent_section.height)
            last_btn, next_btn = Button(), Button()

            last_btn.frame = (self.x, self.parent_section.height * (1 / 4),
                              self.parent_section.width * 2 / 7,
                              self.parent_section.height * 2 / 3)
            next_btn.frame = (self.parent_section.width * 5 / 7,
                              self.parent_section.height * (1 / 4),
                              self.parent_section.width * 2 / 7,
                              self.parent_section.height * 2 / 3)
            last_btn.title = '上月'
            last_btn.action = self.last_on_click
            next_btn.title = '下月'
            next_btn.action = self.next_on_click
            btns = [last_btn, next_btn]
            for btn in btns:
                btn.border_width = 1
                btn.background_color = '#ff9064'
                self.add_subview(btn)

    def last_on_click(self, sender):
        if self.parent_section:
            self.parent_section.month -= 1
            if self.parent_section.month == 0:
                self.parent_section.month = 12
                self.parent_section.year -= 1
            self.parent_section.change_month(self.parent_section.year,
                                             self.parent_section.month,
                                             self.parent_section.day)

    def next_on_click(self, sender):
        if self.parent_section:
            self.parent_section.month += 1
            if self.parent_section.month == 13:
                self.parent_section.month = 1
                self.parent_section.year += 1
            self.parent_section.change_month(self.parent_section.year,
                                             self.parent_section.month,
                                             self.parent_section.day)


class SelectMonthSectionView(SectionView):

    def __init__(
        self,
        view_id,
        parent_section,
        year,
        month,
        day,
        btns: ContentView = None,
    ):
        super().__init__(view_id, parent_section)
        self.background_color = 'gray'
        self.year, self.month, self.day = year, month, day
        self.btns = btns
        self.set_content()

    def set_content(self):
        if self.parent_section:

            self.frame = (self.x, self.y, self.parent_section.width,
                          self.parent_section.height * 1 / 4)
        if self.btns:
            self.add_subview(self.btns)

    def handle_date(self, year, month, day):
        if self.parent_section:
            self.parent_section.handle_date(year, month, day)

    def change_month(self, year, month, date):
        if self.parent_section:
            self.parent_section.change_month(year, month, date)


class BelowSectionView(SectionView):

    def __init__(self, view_id, parent_section):
        super().__init__(view_id, parent_section)
        self.background_color = '#916aae'
        self.interface_section_list = []
        self.set_content()

    def set_content(self):
        if not self.parent_section:
            return
        self.frame = (self.x, self.y, BELOW_SECTION_WIDTH,
                      BELOW_SECTION_HEIGHT)
        if self.interface_section_list:
            for view in self.interface_section_list:
                self.add_subview(view)

    def handle_date(self, year, month, day):
        if self.parent_section:
            res = self.parent_section.handle_date(year, month, day)
            if res.is_ok():
                print("Success", res.val)
            else:
                print('Failed', res.err)

    def change_month(self, year, month, date):
        if self.parent_section:
            self.parent_section.change_month(year, month, date)


class MainSectionView(SectionView):

    def __init__(
        self,
        view_id,
        root_node,
        top_section: SectionView = None,
        below_section: SectionView = None,
    ):
        super().__init__(view_id, root_node)
        self.root_node = self.parent_section
        self.name = f'{dt.datetime.now().month}月'
        self.background_color = "white"
        self.top_section = top_section
        self.below_section = below_section
        self.handled_date = None

    def set_content(self):
        if self.top_section:
            self.add_subview(self.top_section)
        if self.below_section:
            self.add_subview(self.below_section)

    def handle_date(self, year, month,
                    date) -> Result[tuple[int, int, int], str]:
        try:
            self.handled_date = (year, month, date)
            return Ok((year, month, int(date)))
        except Exception as e:
            return Err(str(e))

    def change_month(self, year, month,
                     date) -> Result[tuple[int, int, int], str]:
        try:
            self.name = f'{month}月'
            # self.remove_subview(self.top_section)
            # self.remove_subview(self.below_section)
            # self.root_node.entry_screen(self, year, month, date)
            calendar = self.parent_section.view_id_dict["0-1-2"]
            calendar.year, calendar.month, calendar.day = year, month, date
            calendar.show_content()
            return Ok((year, month, int(date)))
        except Exception as e:
            return Err(str(e))


class Program:

    def __init__(self):
        self.calender_date = None
        self.view_id_dict = {}

    def show_calendar(self, top_section: SectionView, year, month,
                      day) -> SectionView:

        header_view = CalendarHeaderContentView("0-1-1",
                                                parent_section=top_section)
        body_view = CalendarContentView("0-1-2",
                                        parent_section=top_section,
                                        year=year,
                                        month=month,
                                        day=day)
        self.view_id_dict[header_view.view_id] = header_view
        self.view_id_dict[body_view.view_id] = body_view

        top_section.header_content = header_view
        top_section.body_content = body_view
        top_section.add_subview(top_section.header_content)
        top_section.add_subview(top_section.body_content)
        return top_section

    def show_interface(self, below_section: SectionView, year, month,
                       day) -> SectionView:
        select_month_section = SelectMonthSectionView(
            "0-2-1",
            below_section,
            year,
            month,
            day,
        )
        select_month_btns = SelectMonthContentView(
            "0-2-1-1", select_month_section)
        self.view_id_dict[select_month_section.view_id] = select_month_section
        self.view_id_dict[select_month_btns.view_id] = select_month_btns
        select_month_section.btns = select_month_btns
        select_month_section.set_content()
        below_section.interface_section_list.append(select_month_section)
        below_section.set_content()
        return below_section

    def entry_screen(self, main_section: SectionView, year, month, day):
        top_section = TopSectionView("0-1", main_section)
        top_section.x = TOP_SECTION_X
        top_section.y = TOP_SECTION_Y
        self.view_id_dict[top_section.view_id] = top_section
        below_section = BelowSectionView("0-2", main_section)
        below_section.x = BELOW_SECTION_X
        below_section.y = BELOW_SECTION_Y
        self.view_id_dict[below_section.view_id] = below_section
        top_content = self.show_calendar(top_section, year, month, day)
        below_content = self.show_interface(below_section, year, month, day)
        main_section.top_section = top_content
        main_section.below_section = below_content
        main_section.set_content()

    def remove_all_view(self, section: View):
        for view in section.subviews:
            self.remove_all_view(view)
            section.remove_subview(view)

    def present(self, main_section: MainSectionView):
        main_section.present("fullscreen")

    @staticmethod
    def main():
        program = Program()
        main_section = MainSectionView("0", program)
        program.view_id_dict[main_section.view_id] = main_section
        program.entry_screen(main_section,
                             dt.datetime.now().year,
                             dt.datetime.now().month,
                             dt.datetime.now().day)
        program.present(main_section)
        with open('view_id.txt', 'w') as f:
            for i in sorted(program.view_id_dict.keys(),
                            key=lambda k: [int(x) for x in k.split('-')]):
                view = program.view_id_dict[i]
                f.write(f'{i}:{view.__class__.__name__}\n')


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
