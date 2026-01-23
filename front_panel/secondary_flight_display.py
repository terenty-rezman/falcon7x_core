import math
import asyncio
import time

from common.instrument_panel import add_to_panel, TwoStateButton, Indicator, PushButton, NLocalStateButton, LocalStateIndicator, FloatStepper
import xplane.master as xp
import common.xp_aircraft_state as xp_ac
import common.util as util


@add_to_panel
class sfd_menu(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/weapons/mis_thrust3"]
    index = 11 
    states = [0, 1]


@add_to_panel
class sfd_std(PushButton):
    @classmethod
    async def click(cls):
        await xp.set_param(xp.Params["sim/cockpit2/gauges/actuators/barometer_setting_in_hg_copilot"], 29.90)


@add_to_panel
class sfd_set(FloatStepper):
    dataref = xp.Params["sim/cockpit2/gauges/actuators/barometer_setting_in_hg_copilot"]

    left_most_value = 28
    right_most_value = 32
    step = 0.01

    val_type = float


@add_to_panel
class sfd_brt(FloatStepper):
    dataref: xp.Params = xp.Params["sim/custom/7x/z_mini_screen_brightness"]

    logic_left = 0
    logic_right = 10.0

    left_most_value = 0
    right_most_value = 100

    step = 0.01
    state = 0

    OUTPUT = 0
    uso_receive_dt = 0.01
    T = 0.5

    @classmethod
    async def set_state(cls, state: float):
        if not math.isclose(state, cls.OUTPUT, abs_tol=0.1):
            cls.OUTPUT = state

            state = min(max(cls.logic_left, state), cls.logic_right)

            cls.state = state

            # from [logic_left logic_right] to [0 1]
            val_01 = (state - cls.logic_left) / (cls.logic_right - cls.logic_left)

            xp_val = (cls.right_most_value - cls.left_most_value) * val_01 + cls.left_most_value
            xp_val = int(xp_val)

            await xp.set_param(cls.dataref, xp_val)
            print(xp_val)
