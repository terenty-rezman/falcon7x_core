
import asyncio
import time

from instrument_panel import add_to_panel, TwoStateButton, ThreeStateButton, FloatSwitch, DiscreteSwitch
import xplane as xp


@add_to_panel
class aft_temp(FloatSwitch):
    dataref: xp.Params = xp.Params["sim/weapons/mis_thrust2"]
    index = 9
    float_left_most_value = 0
    float_right_most_value = -3


@add_to_panel
class fwd_temp(FloatSwitch):
    dataref: xp.Params = xp.Params["sim/weapons/mis_thrust2"]
    index = 10
    float_left_most_value = 0
    float_right_most_value = -3


@add_to_panel
class fwd_temp_push(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/weapons/mis_thrust2"]
    index = 12


@add_to_panel
class crew_temp(FloatSwitch):
    dataref: xp.Params = xp.Params["sim/weapons/mis_thrust2"]
    index = 11
    float_left_most_value = 0
    float_right_most_value = -3


@add_to_panel
class crew_temp_push(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/weapons/mis_thrust2"]
    index = 14


@add_to_panel
class crew_ratio(FloatSwitch):
    dataref: xp.Params = xp.Params["sim/weapons/mis_thrust3"]
    index = 20
    float_left_most_value = 0
    float_right_most_value = -3


@add_to_panel
class gnd_vent(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/weapons/mis_thrust3"]
    index = 0
    states = [1, 0]


@add_to_panel
class pack(DiscreteSwitch):
    dataref: xp.Params = xp.Params["sim/weapons/target_index"]
    index = 0
    states = [1, 2, 3, 4, 0]


@add_to_panel
class bag_isol(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/weapons/mis_thrust2"]
    index = 8


@add_to_panel
class xbleed_ecs(ThreeStateButton):
    dataref: xp.Params = xp.Params["sim/weapons/mis_thrust2"]
    index = 20
    states = [2, 0, 1]

    @classmethod
    def get_indication(cls):
        state = super().get_state()
        if state == 0:
            return 0
        if state == 1:
            return 2
        if state == 2:
            return 1
