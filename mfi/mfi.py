from collections import defaultdict
from dataclasses import dataclass
import asyncio


mfi_screen_basic_size = {
    "MID": [1167, 696]
}

all_buttons = defaultdict(list) 


@dataclass
class BOX:
    left: int
    top: int
    right: int
    bottom: int


def mfi_button_on_click(screen_name: str, box: BOX):
    def wrapper(fcn):
        all_buttons[screen_name].append({ "box": box, "callback": fcn })
        return fcn
    
    return wrapper


def click_inside_box(click_x: int, click_y: int, box: BOX):
    if click_x > box.left and click_x < box.right and \
        click_y > box.top and click_y < box.bottom:
        return True
    return False


def mfi_click(screen_name: str, click_x: int, click_y: int, screen_w: int, screen_h: int):
    screen_buttons = all_buttons.get(screen_name)
    if screen_buttons is None:
        print(f"MFI error: no such screen: {screen_name} !")
        return
    
    basic_size = mfi_screen_basic_size.get(screen_name)
    if basic_size is None:
        print(f"MFI error: no size for screen: {screen_name} !")
        return
    
    basic_w = basic_size[0]
    basic_h = basic_size[1]

    basic_x_click = click_x * basic_w / screen_w
    basic_y_click = click_y * basic_h / screen_h

    for button in screen_buttons:
        if click_inside_box(basic_x_click, basic_y_click, button["box"]):
            asyncio.create_task(button["callback"]())
            break


from mfi import synoptic
