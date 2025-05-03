try:
	from ui import *  # type: ignore
except ImportError:
	from ui_stub import *  # type: ignore
import datetime as dt
import calendar as cl
from typing import Callable

SCREEN_WIDTH = 375
SCREEN_HEIGHT = 603
CALENDER_WIDTH = SCREEN_WIDTH
CALENDER_HEIGHT = SCREEN_HEIGHT * 3 / 5
CALENDER_X = 0
CALENDER_Y = 0


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
		self.frame = (0, parrent_height / 6, parent_width, parrent_height * 5 / 6)
		self.background_color = "pink"
		self.year, self.month = year, month
		self.create_dates_btns(year, month)
		self.previous_selected_btn = None
		self.selected_btn = None
		self.on_date_selected = on_date_selected

	def create_dates_btns(self, year, month):
		day, days = cl.monthrange(year, month)  # day: 本月第一天是星期幾（0=Mon）

		# 轉換成以「日」開頭（對應你標題的 '日 一 二 三...'）
		resorted_day_index = [6, 0, 1, 2, 3, 4, 5]  # 原始 weekday 改成你要的順序
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
				 self.width / 7 * col + 2,
				 self.height / 6 * row + 2,
				 self.width / 7 - 4,
				 self.height / 6 - 4,
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
			self.on_date_selected(self.month, sender.title)


class CalenderView(View):

	def __init__(self, x=0, y=0):
		super().__init__()
		self.frame = (x, y, CALENDER_WIDTH, CALENDER_HEIGHT)
		self.background_color = "blue"
		self.add_subview(CalenderHeaderView(self.width, self.height))
		self.add_subview(
		 CalenderContentView(self.width,
		                     self.height,
		                     on_date_selected=self.date_selected))
		self.output_date = None

	def date_selected(self, month, date):
		self.output_date = (month, date)


class EntryView(View):

	def __init__(self):
		super().__init__()
		self.name = "test2"
		self.background_color = "white"
		self.add_subview(CalenderView(x=CALENDER_X, y=CALENDER_Y))


start = EntryView()
start.present("fullscreen")

