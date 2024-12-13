"""Simple example showing how to get gamepad events."""

from __future__ import print_function
from threading import Lock, Thread
from time import sleep
import math

from inputs import get_gamepad, UnpluggedError, devices


def normalize_axis_value_16bit(val) -> float:
    v = max(min(val / 32767.0, 1), -1)
    v = round(v, 2)
    return v

def normalize_axis_value_8bit(val) -> float:
    v = max(min(val / 255.0, 1), -1)
    v = round(v, 2)
    return v


class Joystick:
    def __init__(self) -> None:
        self.lock = Lock()
        self.thread = None

        self.axis_X = 0
        self.axis_Y = 0
        self.axis_Z = 0
        self.axis_RZ = 0


    def get_axes_values(self):
        with self.lock:
            return [self.axis_X, self.axis_Y, self.axis_Z, self.axis_RZ]
    
    def is_plugged(self):
        try:
            gamepad = devices.gamepads[0]
        except IndexError:
            return False
        return True

    def run_in_thread(self):
        def poll_events():
            while True:
                events = get_gamepad()
                with self.lock:
                    for event in events:
                        # print(event.ev_type, event.code, event.state)
                        if event.code == "ABS_X":
                            self.axis_X = normalize_axis_value_16bit(event.state)
                        if event.code == "ABS_Y":
                            self.axis_Y = normalize_axis_value_16bit(event.state)
                        if event.code == "ABS_Z":
                            self.axis_Z = normalize_axis_value_8bit(event.state)
                        if event.code == "ABS_RZ":
                            self.axis_RZ = normalize_axis_value_8bit(event.state)

        self.thread = Thread(target=poll_events)
        self.thread.start()
        


def main():
    """Just print out some event infomation when the gamepad is used."""
    j = Joystick()
    j.run_in_thread()

    while True:
        # print(j.get_axes_values())
        sleep(0.1)
        


if __name__ == "__main__":
    main()
