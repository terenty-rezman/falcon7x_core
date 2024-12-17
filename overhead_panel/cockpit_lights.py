
import asyncio
import time

from common.instrument_panel import add_to_panel, TwoStateButton, ThreeStateButton, FloatSwitch, DiscreteSwitch
import xplane.master as xp


@add_to_panel
class cl_overhead(FloatSwitch):
    dataref: xp.Params = xp.Params["sim/cockpit2/switches/instrument_brightness_ratio"]
    index = 4
    float_left_most_value = 2
    float_right_most_value = 0


@add_to_panel
class cl_panel(FloatSwitch):
    dataref: xp.Params = xp.Params["sim/cockpit2/switches/instrument_brightness_ratio"]
    index = 0
    float_left_most_value = 0.6
    float_right_most_value = 3


@add_to_panel
class cl_dim(FloatSwitch):
    dataref: xp.Params = xp.Params["sim/cockpit2/switches/instrument_brightness_ratio"]
    index = 2
    float_left_most_value = 0
    float_right_most_value = 1


@add_to_panel
class cl_shield(FloatSwitch):
    dataref: xp.Params = xp.Params["sim/cockpit2/switches/instrument_brightness_ratio"]
    index = 1
    float_left_most_value = 0
    float_right_most_value = 3
