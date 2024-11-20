
import asyncio
import time

from instrument_panel import add_to_panel, TwoStateButton, Indicator, PushButton, NLocalStateButton, LocalStateIndicator, FloatStepper
import xplane.master as xp
import xp_aircraft_state as xp_ac
import util


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
