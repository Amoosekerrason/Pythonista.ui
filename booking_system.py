# region import
try:
    from ui import *  # type: ignore
except ImportError:
    from ui_stub import *  # type: ignore
import datetime as dt
import calendar as cl
from result import *
from abstract_class import *
from sql3_db_helper import SQL3DBqueue, SQL3DBHelper
import logging


# endregion

# region Calandar


class CalendarHeaderContentView(ContentView):

    def __init__(self, view_id, parent_section):
        super().__init__(view_id, parent_section)
        if COLOR_TOGGLE:
            self.background_color = "yellow"
        self.show_content()

    def show_content(self):
        if self.parent_section:
            self.frame = (
                self.x,
                self.y,
                self.parent_section.width,
                self.parent_section.height / 6,
            )
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
        if COLOR_TOGGLE:
            self.background_color = "pink"
        self.year, self.month, self.day = year, month, day
        self.previous_selected_btn = None
        self.selected_btn = None
        self.show_content()

    def show_content(self):
        if not self.parent_section:
            return
        if self.subviews:
            for view in self.subviews:
                self.remove_subview(view)
        self.frame = (
            self.x,
            self.parent_section.height / 6,
            self.parent_section.width,
            self.parent_section.height * 5 / 6,
        )
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
                if int(btn.title) == self.day:
                    btn.background_color = "#9bf1ff"
                    self.previous_selected_btn = btn
                    self.selected_btn = btn
                btn.action = self.btn_clicked
                self.add_subview(btn)
                btn_title += 1

    def btn_clicked(self, sender):
        if self.previous_selected_btn:
            self.previous_selected_btn.background_color = None
        sender.background_color = "#9bf1ff"
        self.previous_selected_btn = sender
        self.selected_btn = sender
        if self.parent_section:
            self.parent_section.handle_date(
                self.year, self.month, int(sender.title))


# endregion


# region CRUD ui
class CreateArrangementContentView(ContentView):

    def __init__(self, view_id, parent_section=None, x=0, y=0, date=None):
        super().__init__(view_id, parent_section, x, y)
        self.date = date
        self.show_content()

    def show_content(self):
        if not self.parent_section:
            return
        self.frame = (
            self.x,
            self.y,
            self.parent_section.width,
            self.parent_section.height,
        )
        self.create_arrangement_ui = load_view("create_arrangement_ui.pyui")
        self.year_filed = self.create_arrangement_ui["year_text"]
        self.year_filed.text = str(self.date[0] - 1911)
        self.month_field = self.create_arrangement_ui["month_text"]
        self.month_field.text = str(self.date[1])
        self.day_field = self.create_arrangement_ui["day_text"]
        self.day_field.text = str(self.date[2])
        self.create_arrangement_ui["send_btn"].action = self.re_crud

        self.add_subview(self.create_arrangement_ui)

    def change_field_text(self):
        if self.create_arrangement_ui["gender_text"].text.lower() == "r":
            self.create_arrangement_ui["gender_text"].text = "先生"
        elif self.create_arrangement_ui["gender_text"].text.lower() == "s":
            self.create_arrangement_ui["gender_text"].text = "小姐"
        if self.create_arrangement_ui["contact_text"].text == "000":
            self.create_arrangement_ui["contact_text"].text = "陳帥"

    def re_crud(self, sender):
        self.change_field_text()
        print(f'性別是 {self.create_arrangement_ui["gender_text"].text}')
        print(f'接洽人是 {self.create_arrangement_ui["contact_text"].text}')
        self.parent_section.re_crud()

    def handled_date(self, date: tuple[int, int, int]):
        self.year_filed.text = str(date[0] - 1911)
        self.month_field.text = str(date[1])
        self.day_field.text = str(date[2])


class ReadArrangementContentView(ContentView):

    def __init__(self, view_id, parent_section=None, x=0, y=0):
        super().__init__(view_id, parent_section, x, y)

    def show_content(self):
        return super().show_content()


class UploadArrangementContentView(ContentView):

    def __init__(self, view_id, parent_section=None, x=0, y=0):
        super().__init__(view_id, parent_section, x, y)

    def show_content(self):
        return super().show_content()


class DeleteArrangementContentView(ContentView):

    def __init__(self, view_id, parent_section=None, x=0, y=0):
        super().__init__(view_id, parent_section, x, y)

    def show_content(self):
        return super().show_content()


# endregion

# region Interface


class JumpToDateContentView(ContentView):

    def __init__(self, view_id, parent_section, x=0, y=0):
        super().__init__(view_id, parent_section, x, y)
        self.show_content()

    def show_content(self):
        if not self.parent_section:
            return
        self.frame = (
            self.x,
            self.y,
            self.parent_section.width,
            self.parent_section.height,
        )
        self.background_color = "white"
        self.datepicker = DatePicker()
        # self.datepicker.border_width=1
        self.datepicker.mode = DATE_PICKER_MODE_DATE
        self.datepicker.frame = (
            self.parent_section.width / 4 - 50,
            self.parent_section.height / 4 - 10,
            self.parent_section.width / 2,
            self.parent_section.height / 2,
        )
        self.add_subview(self.datepicker)
        confirm_btn = Button()
        # confirm_btn.border_width = 1
        confirm_btn.title = "前往"
        confirm_btn.frame = (
            self.datepicker.width + 50,
            self.datepicker.height / 2 + 16,
            75,
            50,
        )
        confirm_btn.action = self.go_to_date
        self.add_subview(confirm_btn)

    def go_to_date(self, sender):
        date = (
            self.datepicker.date.year,
            self.datepicker.date.month,
            self.datepicker.date.day,
        )
        self.parent_section.go_to_date(date)


class CRUDContentView(ContentView):

    def __init__(self, view_id, parent_section):
        super().__init__(view_id, parent_section)
        self.show_content()

    def show_content(self):
        if not self.parent_section:
            return
        self.frame = (
            self.x,
            self.y,
            self.parent_section.width,
            self.parent_section.height,
        )
        total_width = self.parent_section.width
        total_height = self.parent_section.height
        btn_margin = 20
        btn_width = (total_width - 4 * btn_margin) / 2
        btn_height = (total_height - 4 * btn_margin) / 2
        NW_btn_x, NW_btn_y = btn_margin, btn_margin
        NE_btn_x, NE_btn_y = NW_btn_x + btn_width + 2 * btn_margin, NW_btn_y
        SW_btn_x, SW_btn_y = NW_btn_x, NW_btn_y + btn_height + 2 * btn_margin
        SE_btn_x, SE_btn_y = (
            NW_btn_x + btn_width + 2 * btn_margin,
            NW_btn_y + btn_height + 2 * btn_margin,
        )
        NW_btn, NE_btn, SW_btn, SE_btn = Button(), Button(), Button(), Button()
        btns = [NW_btn, NE_btn, SW_btn, SE_btn]
        NW_btn.frame = (NW_btn_x, NW_btn_y, btn_width, btn_height)
        NE_btn.frame = (NE_btn_x, NE_btn_y, btn_width, btn_height)
        SW_btn.frame = (SW_btn_x, SW_btn_y, btn_width, btn_height)
        SE_btn.frame = (SE_btn_x, SE_btn_y, btn_width, btn_height)
        NW_btn.title = "建立預約"
        NW_btn.action = self.create_create_arrangement_content
        NE_btn.title = "修改預約"
        SW_btn.title = "刪除預約"
        SE_btn.title = "查詢預約"
        for btn in btns:
            btn.border_width = 1
            btn.background_color = "light blue"
            self.add_subview(btn)

    def create_create_arrangement_content(self, sender):
        self.parent_section.create_create_arrangement_content()


class CRUDSectionView(SectionView):

    def __init__(self, view_id, parent_section, content: ContentView = None):
        super().__init__(view_id, parent_section)
        self.content = content
        self.set_content()

    def set_content(self):
        if not self.parent_section:
            return
        self.frame = (
            self.x,
            self.parent_section.height / 4,
            self.parent_section.width,
            self.parent_section.height * 3 / 4,
        )
        if COLOR_TOGGLE:
            self.background_color = "#b1f4ff"
        if self.content:
            self.add_subview(self.content)

    def go_to_date(self, date: tuple[int, int, int]):
        self.remove_subview(self.content)
        self.parent_section.go_to_date(date)
        self.parent_section.handled_date(date)

    def create_create_arrangement_content(self):
        self.remove_subview(self.content)
        self.parent_section.create_create_arrangement_content()

    def re_crud(self):
        self.remove_subview(self.content)
        self.parent_section.re_crud()


# endregion

# region Select Month


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
            self.frame = (
                self.x,
                self.y,
                self.parent_section.width,
                self.parent_section.height,
            )
            last_btn, middle_btn, next_btn = Button(), Button(), Button()

            total_width = self.parent_section.width
            btn_height = self.parent_section.height * 2 / 3
            side_btn_width, middle_btn_width = total_width * 2 / 7, total_width * 3 / 7
            left_btn_x, middle_btn_x, right_btn_x = (
                total_width * 0 / 7,
                total_width * 2 / 7,
                total_width * 5 / 7,
            )
            btn_y = (self.parent_section.height - btn_height) / 2

            last_btn.frame = (left_btn_x, btn_y, side_btn_width, btn_height)
            middle_btn.frame = (middle_btn_x, btn_y,
                                middle_btn_width, btn_height)
            next_btn.frame = (right_btn_x, btn_y, side_btn_width, btn_height)

            last_btn.title = "上月"
            last_btn.action = self.last_on_click
            middle_btn.title = f"{self.parent_section.year}/{self.parent_section.month}/{self.parent_section.day}"
            self.middle_btn = middle_btn
            middle_btn.action = self.middle_on_click
            next_btn.title = "下月"
            next_btn.action = self.next_on_click
            btns = [last_btn, middle_btn, next_btn]
            for btn in btns:
                btn.border_width = 1
                if COLOR_TOGGLE:
                    btn.background_color = "#ff9064"
                self.add_subview(btn)

    def last_on_click(self, sender):
        if self.parent_section:
            self.parent_section.month -= 1
            if self.parent_section.month == 0:
                self.parent_section.month = 12
                self.parent_section.year -= 1
            self.parent_section.change_month_and_go_to_date(
                self.parent_section.year,
                self.parent_section.month,
                self.parent_section.day,
            )
            self.middle_btn.title = f"{self.parent_section.year}/{self.parent_section.month}/{self.parent_section.day}"

    def middle_on_click(self, sender):
        self.parent_section.crud_to_date_picker()

    def next_on_click(self, sender):
        if self.parent_section:
            self.parent_section.month += 1
            if self.parent_section.month == 13:
                self.parent_section.month = 1
                self.parent_section.year += 1
            self.parent_section.change_month_and_go_to_date(
                self.parent_section.year,
                self.parent_section.month,
                self.parent_section.day,
            )
            self.middle_btn.title = f"{self.parent_section.year}/{self.parent_section.month}/{self.parent_section.day}"

    def handled_date(self, date: tuple[int, int, int]):
        self.middle_btn.title = f"{date[0]}/{date[1]}/{date[2]}"


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

        self.year, self.month, self.day = year, month, day
        self.btns = btns
        self.set_content()

    def set_content(self):

        if self.parent_section:

            self.frame = (
                self.x,
                self.y,
                self.parent_section.width,
                self.parent_section.height * 1 / 4,
            )
            if COLOR_TOGGLE:
                self.background_color = "gray"
            self.border_width = 1
        if self.btns:
            self.add_subview(self.btns)

    def handle_date(self, year, month, day):
        if self.parent_section:
            self.parent_section.handle_date(year, month, day)

    def change_month_and_go_to_date(self, year, month, date):
        if self.parent_section:
            self.parent_section.change_month_and_go_to_date(year, month, date)

    def handled_date(self, date: tuple[int, int, int]):
        self.year, self.month, self.day = date[0], date[1], date[2]
        self.btns.handled_date(date)

    def crud_to_date_picker(self):
        self.parent_section.crud_to_date_picker()


# endregion

# region Primary Section


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
        if COLOR_TOGGLE:
            self.background_color = "blue"
        self.header_content = header_content
        self.body_content = body_content
        self.set_content()

    def set_content(self):
        if not self.parent_section:
            return
        self.frame = (
            self.x,
            self.y,
            self.parent_section.width,
            self.parent_section.height * TOP_SECTION_RATIO,
        )
        if self.header_content:
            self.add_subview(self.header_content)
        if self.body_content:
            self.add_subview(self.body_content)

    def handle_date(self, year, month, date):
        if self.parent_section:
            self.parent_section.handle_date(year, month, date)


class BelowSectionView(SectionView):

    def __init__(self, view_id, parent_section):
        super().__init__(view_id, parent_section)
        if COLOR_TOGGLE:
            self.background_color = "purple"
        self.interface_section_list = []
        self.set_content()

    def set_content(self):
        if not self.parent_section:
            return
        self.frame = (
            self.x,
            self.y,
            self.parent_section.width,
            self.parent_section.height * BELOW_SECTION_RATIO,
        )
        if self.interface_section_list:
            for view in self.interface_section_list:
                self.add_subview(view)

    def handle_date(self, year, month, day):
        if self.parent_section:
            self.parent_section.handle_date(year, month, day)

    def change_month_and_go_to_date(self, year, month, date):
        if self.parent_section:
            self.parent_section.change_month_and_go_to_date(year, month, date)

    def handled_date(self, date: tuple[int, int, int]):
        for view in self.interface_section_list:
            if type(view) == SelectMonthSectionView:
                view.handled_date(date)

    def crud_to_date_picker(self):
        self.parent_section.crud_to_date_picker()

    def go_to_date(self, date: tuple[int, int, int]):
        self.parent_section.change_month_and_go_to_date(
            date[0], date[1], date[2])
        self.parent_section.re_crud()

    def create_create_arrangement_content(self):
        self.parent_section.create_create_arrangement_content()

    def re_crud(self):
        self.parent_section.re_crud()


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
        self.name = f"訂位君"

        self.background_color = "white"
        self.top_section = top_section
        self.below_section = below_section
        self.handled_date = None
        self.present("fullscreen")

    def set_content(self):
        if not self.parent_section:
            return
        if self.top_section:
            self.add_subview(self.top_section)
        if self.below_section:
            self.add_subview(self.below_section)

    def handle_date(self, year, month, date):
        self.parent_section.handle_date(year, month, date)

    def crud_to_date_picker(self):
        self.parent_section.crud_to_date_picker()

    def change_month_and_go_to_date(self, year, month, date):
        self.parent_section.change_month_and_go_to_date(year, month, date)

    def re_crud(self):
        self.parent_section.re_crud()

    def create_create_arrangement_content(self):
        self.parent_section.create_create_arrangement_content()


# endregion

# region System-level Class


class ViewFactory:
    _types = {
        "main": MainSectionView,
        "below": BelowSectionView,
        "top": TopSectionView,
        "select month section": SelectMonthSectionView,
        "select month content": SelectMonthContentView,
        "jump to date content": JumpToDateContentView,
        "crud section": CRUDSectionView,
        "crud content": CRUDContentView,
        "calendar content": CalendarContentView,
        "calandar header content": CalendarHeaderContentView,
        "create arrangement content": CreateArrangementContentView,
    }

    @staticmethod
    def produce_product(type: str, *args, **kwargs) -> Result[View, str]:
        view_class = ViewFactory._types.get(type)
        if not view_class:
            return Err(f"unknown view type: {type}")

        try:
            instance = view_class(*args, **kwargs)
            return Ok(instance)
        except Exception as e:
            return Err(f"failed to create view: {e}")


class Program:

    def __init__(self, dbhelper: DBHelper):
        self.dbhelper = dbhelper
        self.date = (
            dt.datetime.now().year,
            dt.datetime.now().month,
            dt.datetime.now().day,
        )
        self.view_id_dict = {}

    def init_all_components(self):
        self.main_section_res = ViewFactory.produce_product("main", "0")
        self.top_section_res = ViewFactory.produce_product("top", "0-1")
        self.calendar_header_content_res = ViewFactory.produce_product(
            "calandar header content", "0-1-1")
        self.calendar_content_res = ViewFactory.produce_product(
            "calendar content", "0-1-2")
        self.below_section_res = ViewFactory.produce_product("below", "0-2")
        self.select_month_section_res = ViewFactory.produce_product(
            "select month section", "0-2-1")
        self.select_month_content_res = ViewFactory.produce_product(
            "select month content", "0-2-1-1")
        self.jump_to_date_content_res = ViewFactory.produce_product(
            "jump to date content", "0-2-1-2")
        self.crud_section_res = ViewFactory.produce_product(
            "crud section", "0-2-2")
        self.crud_content_res = ViewFactory.produce_product(
            "crud content", "0-2-2-1")
        self.create_arrangement_content_res = ViewFactory.produce_product(
            "create arrangement content", "0-2-2-2")

    # region ui functions
    '''
    def entry_screen(self, main_section: SectionView, year, month, day):
        top_section_res = ViewFactory.produce_product(
            "top", "0-1", main_section)
        if top_section_res.is_ok():
            self.top_section = top_section_res.val
            self.top_section.x = 0
            self.top_section.y = 0
            self.register_view(self.top_section)
            below_section_res = ViewFactory.produce_product("below", "0-2",
                                                            main_section)
            if below_section_res.is_ok():
                self.below_section = below_section_res.val
                self.below_section.x = 0
                self.below_section.y = self.top_section.height
                self.register_view(self.below_section)
                top_content = self.show_calendar(
                    year, month, day, self.top_section)
                below_content = self.show_interface(year, month, day,
                                                    self.below_section)
                main_section.top_section = top_content
                main_section.below_section = below_content
                main_section.set_content()
            else:
                logger.error(below_section_res.err)
        else:
            logger.error(top_section_res.err)

    def show_calendar(self,
                      year,
                      month,
                      day,
                      section: SectionView = None) -> SectionView:

        header_view = CalendarHeaderContentView(
            "0-1-1", parent_section=section)
        body_view = CalendarContentView("0-1-2",
                                        parent_section=section,
                                        year=year,
                                        month=month,
                                        day=day)

        self.register_view(header_view)

        self.register_view(body_view)

        section.header_content = header_view
        section.body_content = body_view
        section.add_subview(section.header_content)
        section.add_subview(section.body_content)
        return section

    def show_interface(self,
                       year,
                       month,
                       day,
                       section: SectionView = None) -> SectionView:
        select_month_section = self.get_select_month_section(
            year, month, day, section)

        crud_section = self.get_crud_section()
        try:
            section.interface_section_list.append(select_month_section)
            section.interface_section_list.append(crud_section)
            section.set_content()
            return section
        except Exception as e:
            raise Exception(
                f"this section doesn't have interface section list") from e

    def get_select_month_section(self,
                                 year,
                                 month,
                                 day,
                                 section: SectionView = None):
        select_month_section = SelectMonthSectionView(
            "0-2-1",
            section,
            year,
            month,
            day,
        )
        select_month_btns = SelectMonthContentView(
            "0-2-1-1", select_month_section)
        self.register_view(select_month_section)
        self.register_view(select_month_btns)

        select_month_section.btns = select_month_btns
        select_month_section.set_content()
        return select_month_section

    def get_crud_section(self):
        crud_section = CRUDSectionView("0-2-2", self.below_section)
        crud_content = CRUDContentView("0-2-2-1", crud_section)

        self.register_view(crud_section)

        self.register_view(crud_content)

        crud_section.content = crud_content
        crud_section.set_content()
        return crud_section

    def crud_to_date_picker(self):
        crud_section = self.view_id_dict["0-2-2"]
        # self.remove_all_view(crud_section)
        for subview in crud_section.subviews:
            subview.hidden = True
        datepicker = JumpToDateContentView("0-2-2-2", crud_section)
        self.register_view(datepicker)
        crud_section.content = datepicker
        crud_section.set_content()
        # datepicker.present("sheet")

    '''
    # endregion

    # region callback functions

    def re_crud(self):
        crud_section = self.view_id_dict["0-2-2"]
        crud_content = CRUDContentView("0-2-2-1", crud_section)
        # crud_content = self.view_id_dict["0-2-2-1"]
        crud_section.content = crud_content
        crud_section.set_content()

    def change_month_and_go_to_date(self, year, month,
                                    date) -> Result[tuple[int, int, int], str]:

        try:
            create_arrangement_ui = self.view_id_dict.get("0-2-2-3", None)
            if create_arrangement_ui:
                create_arrangement_ui.handled_date((year, month, date))
            self.date = (year, month, date)
            calendar = self.view_id_dict["0-1-2"]
            calendar.year, calendar.month, calendar.day = year, month, date
            calendar.show_content()
            return Ok((year, month, int(date)))
        except Exception as e:
            return Err(str(e))

    def handle_date(self, year, month,
                    date) -> Result[tuple[int, int, int], str]:
        self.date = (year, month, date)

        below_section = self.view_id_dict["0-2"]
        main_section = self.view_id_dict["0"]
        create_arrangement_ui = self.view_id_dict.get("0-2-2-3", None)
        try:
            if create_arrangement_ui:
                create_arrangement_ui.handled_date(self.date)
            main_section.handled_date = self.date
            below_section.handled_date(self.date)

            return Ok((year, month, int(date)))
        except Exception as e:
            return Err(str(e))

    def create_create_arrangement_content(self):
        crud_section = self.view_id_dict["0-2-2"]
        if not self.create_arrangement_content:
            create_arrangement_content_res = ViewFactory.produce_product(
                "create arrangement content", "0-2-2-3", crud_section, date=self.date)
            if create_arrangement_content_res.is_ok():
                self.create_arrangement_content = create_arrangement_content_res.val
                self.register_view(self.create_arrangement_content)
                crud_section.content = self.create_arrangement_content
                crud_section.set_content()
            else:
                logger.error(create_arrangement_content_res.err)
        else:
            self.create_arrangement_content.hidden = False
            crud_section.content = self.create_arrangement_content
            crud_section.set_content()

    # endregion

    def remove_all_view(self, section: View):
        for view in section.subviews:
            self.remove_all_view(view)
            section.remove_subview(view)

    def register_view(self, view):
        if view.view_id not in self.view_id_dict.keys():
            logger.info(
                f'{view.__class__.__name__}:{view.view_id} registered.')
            self.view_id_dict[view.view_id] = view
            with open("view_id.txt", "a") as f:
                f.write(f"{view.view_id}:{view.__class__.__name__}\n")

    def present(self, main_section: MainSectionView):
        main_section.present("fullscreen")

    @staticmethod
    def log():
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            filename="booking.log",
            filemode="w"
        )
        logger = logging.getLogger(__name__)
        logger.info("start add handler")
        if not logger.handlers:
            console = logging.StreamHandler()
            console.setLevel(logging.DEBUG)
            formatter = logging.Formatter(
                '%(asctime)s [%(levelname)s] %(name)s: %(message)s')
            console.setFormatter(formatter)
            logger.addHandler(console)
            logger.info("added handler")
        else:
            logger.info("got handler")
        return logger

    @staticmethod
    def main():
        logger.info("start running")
        dbqueue = SQL3DBqueue()
        dbhelper = SQL3DBHelper("database.db", dbqueue)
        program = Program(dbhelper)
        with open("view_id.txt", "w") as f:
            f.write("View ID Registry:\n")
        main_section_res = ViewFactory.produce_product("main", "0", program)
        if main_section_res.is_ok():
            main_section = main_section_res.val
            program.register_view(main_section)
            program.entry_screen(
                main_section,
                dt.datetime.now().year,
                dt.datetime.now().month,
                dt.datetime.now().day,
            )

        else:
            logger.error(main_section_res.err)
        # main_section = MainSectionView("0", program)
        # with open("view_id.txt", "w") as f:
        #     for i in sorted(
        #         program.view_id_dict.keys(),
        #         key=lambda k: [int(x) for x in k.split("-")],
        #     ):
        #         view = program.view_id_dict[i]
        #         f.write(f"{i}:{view.__class__.__name__}\n")


# endregion

if __name__ == "__main__":
    TOP_SECTION_RATIO = 4 / 7
    BELOW_SECTION_RATIO = 1 - TOP_SECTION_RATIO
    COLOR_TOGGLE = False
    logger = Program.log()
    Program.main()
