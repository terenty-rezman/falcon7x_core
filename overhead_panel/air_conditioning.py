
import asyncio
import time

from .overhead_panel import add_to_overhead_panel, TwoStateButton, ThreeStateButton, FloatSwitch
import xplane as xp


@add_to_overhead_panel
class aft_temp(FloatSwitch):
    dataref: xp.Params = xp.Params["sim/weapons/mis_thrust2"]
    index = 9
    float_left_most_value = 0
    float_right_most_value = -3


@add_to_overhead_panel
class fwd_temp(FloatSwitch):
    dataref: xp.Params = xp.Params["sim/weapons/mis_thrust2"]
    index = 10
    float_left_most_value = 0
    float_right_most_value = -3


@add_to_overhead_panel
class fwd_temp_push(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/weapons/mis_thrust2"]
    index = 12


@add_to_overhead_panel
class crew_temp(FloatSwitch):
    dataref: xp.Params = xp.Params["sim/weapons/mis_thrust2"]
    index = 11
    float_left_most_value = 0
    float_right_most_value = -3


@add_to_overhead_panel
class crew_temp_push(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/weapons/mis_thrust2"]
    index = 14


@add_to_overhead_panel
class crew_ratio(FloatSwitch):
    dataref: xp.Params = xp.Params["sim/weapons/mis_thrust3"]
    index = 20
    float_left_most_value = 0
    float_right_most_value = -3
