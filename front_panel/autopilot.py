import asyncio
import time

from instrument_panel import add_to_panel, TwoStateButton, Indicator, PushButton, NLocalStateButton, LocalStateIndicator, FloatStepper, ThreeStateButton
import xplane as xp
import xp_aircraft_state as xp_ac
import util
        

# F7X_SDD_Avionics_Vol1 23-4 front panel autopilot

@add_to_panel
class swap_lh(PushButton):
    @classmethod
    async def click(cls):
        pass


@add_to_panel
class vhf_control_lh(FloatStepper):
    dataref = xp.Params["sim/cockpit2/radios/actuators/com1_standby_frequency_hz_833"]

    left_most_value = 119000
    right_most_value = 135000
    step = 0.01

    val_type = int


@add_to_panel
class baro_push_lh(PushButton):
    @classmethod
    async def click(cls):
        await xp.set_param(xp.Params["sim/cockpit2/gauges/actuators/barometer_setting_in_hg_pilot"], 29.92)


@add_to_panel
class baro_rot_lh(FloatStepper):
    dataref = xp.Params["sim/cockpit2/gauges/actuators/barometer_setting_in_hg_pilot"]

    left_most_value = 28
    right_most_value = 32
    step = 0.01

    val_type = float


@add_to_panel
class fdtd_lh(ThreeStateButton):
    dataref: xp.Params = xp.Params["sim/custom/7x/flydir"]
    states = [0, 1, 2]


# F7X_SDD_Avionics_Vol1 22-21 front panel autopilot
