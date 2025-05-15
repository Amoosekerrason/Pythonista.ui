from typing import Callable, Optional

ALIGN_LEFT: int
ALIGN_CENTER: int
ALIGN_RIGHT: int

CONTENT_MODE_SCALE_TO_FILL: int
CONTENT_MODE_SCALE_ASPECT_FIT: int
CONTENT_MODE_SCALE_ASPECT_FILL: int

def get_screen_size() -> tuple[int, int]: ...
def open_url(url: str) -> None: ...
def set_clipboard(text: str) -> None: ...
def get_clipboard() -> str: ...

class Color:
    def __init__(self, r: float, g: float, b: float, a: float = 1.0): ...

class View:
    alpha: float
    background_color: str
    border_color: Optional[str]
    border_width: float
    bounds: tuple[float, float, float, float]
    center = tuple[float, float]
    content_mode = str
    corner_radius: float
    enabled: bool
    frame: tuple[float, float, float, float]
    flex: str
    height: int
    hidden: bool
    multitouch_enabled: bool
    name: str
    subviews: tuple
    superview: View
    width: int
    x: int
    y: int

    def __init__(self): ...
    def add_subview(self, view: "View") -> None: ...
    def remove_subview(self, view: "View") -> None: ...
    def bring_to_front(self) -> None: ...
    def send_to_back(self) -> None: ...
    def present(
        self,
        style: str = "default",
        animated: bool = True,
        popover_location=None,
        hide_title_bar: bool = False,
        title_bar_color: str = None,
        title_color: str = None,
        orientations=None,
        hide_close_button=False,
    ) -> None: ...
    def close(self) -> None: ...
    def layout(self) -> None: ...
    def set_needs_display(self) -> None: ...
    def wait_modal(self) -> any: ...

class Label(View):
    text: str
    text_color: str
    font: tuple[str, float]
    alignment: int
    number_of_lines: int
    line_break_mode: int

class Button(View):
    title: str
    image: Optional[any]
    tint_color: Optional[str]
    font: tuple[str, float]
    enabled: bool
    action: Optional[Callable[["Button"], None]]

class ImageView(View):
    image: Optional[any]
    content_mode: int
    flex: str

class TextField(View):
    text: str
    placeholder: str
    secure: bool
    keyboard_type: int
    autocapitalization_type: int
    spellchecking_type: int
    autocorrection_type: int
    enabled: bool
    delegate: Optional[any]

class TextView(View):
    text: str
    font: tuple[str, float]
    text_color: str
    editable: bool
    delegate: Optional[any]

class Slider(View):
    value: float
    min_value: float
    max_value: float
    continuous: bool
    action: Optional[Callable[["Slider"], None]]

class Switch(View):
    value: bool
    action: Optional[Callable[["Switch"], None]]

class TableView(View):
    data_source: Optional[any]
    delegate: Optional[any]
    allows_multiple_selection: bool
    allows_selection: bool
    separator_color: str
    row_height: float
    flex: str
    def reload(self) -> None: ...

class TableViewCell(View):
    text_label: Label
    image_view: ImageView
    accessory_type: int

class DatePicker(View):
    action: Optional[Callable[["DatePicker"], None]]
    enabled: bool
