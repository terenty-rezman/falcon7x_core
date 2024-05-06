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


@add_to_panel
class fp_speed_is_mach_push(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/cockpit/autopilot/airspeed_is_mach"]
    states = [0, 1]

    @classmethod
    async def click(cls):
        await xp.run_command_once(xp.Commands["sim/autopilot/knots_mach_toggle"])
        await super().click()


@add_to_panel
class fp_speed_kts_mach(FloatStepper):
    dataref: xp.Params = xp.Params["sim/cockpit2/autopilot/airspeed_dial_kts_mach"]

    is_mach_dref = xp.Params["sim/cockpit/autopilot/airspeed_is_mach"]

    left_most_kts = 95
    right_most_kts = 370
    step_kts = 1.0

    left_most_mach = 0.0
    right_most_mach = 1.0
    step_mach = 0.01

    val_type = float

    @classmethod
    async def set_state(cls, state: float):
        is_mach = xp_ac.ACState.get_curr_param(cls.is_mach_dref)
        if is_mach is None:
            return
        
        if is_mach:
            cls.left_most_value = cls.left_most_mach
            cls.right_most_value = cls.right_most_mach
            cls.step = cls.step_mach
        else:
            cls.left_most_value = cls.left_most_kts
            cls.right_most_value = cls.right_most_kts
            cls.step = cls.step_kts
        
        await super().set_state(state)
    
    @classmethod 
    def get_state(cls):
        is_mach = xp_ac.ACState.get_curr_param(cls.is_mach_dref)
        if is_mach is None:
            return
        
        if is_mach:
            cls.left_most_value = cls.left_most_mach
            cls.right_most_value = cls.right_most_mach
            cls.step = cls.step_mach
        else:
            cls.left_most_value = cls.left_most_kts
            cls.right_most_value = cls.right_most_kts
            cls.step = cls.step_kts

        return super().get_state()


@add_to_panel
class fp_autothrottle(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/cockpit2/autopilot/autothrottle_enabled"]
    states = [0, 1]

    @classmethod
    async def click(cls):
        await xp.run_command_once(xp.Commands["sim/autopilot/autothrottle_toggle"])
        await super().click()


@add_to_panel
class fp_approach(ThreeStateButton):
    dataref: xp.Params = xp.Params["sim/cockpit2/autopilot/approach_status"]
    states = [0, 1, 2]

    @classmethod
    async def click(cls):
        await xp.run_command_once(xp.Commands["sim/autopilot/approach"])


@add_to_panel
class fp_lnav(ThreeStateButton):
    dataref: xp.Params = xp.Params["sim/cockpit2/autopilot/nav_status"]
    states = [0, 1, 2]

    @classmethod
    async def click(cls):
        await xp.run_command_once(xp.Commands["sim/autopilot/NAV"])


@add_to_panel
class fp_hdg_trk(FloatStepper):
    dataref: xp.Params = xp.Params["sim/cockpit/autopilot/heading_mag"]

    left_most_value = 0
    right_most_value = 360
    step = 1

    val_type = float


@add_to_panel
class fp_hdg_trk_push(PushButton):
    @classmethod
    async def click(cls):
        await xp.run_command_once(xp.Commands["sim/autopilot/heading_sync"])


@add_to_panel
class fp_hdg_trk_mode(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/cockpit2/autopilot/heading_mode"]
    states = [0, 1, 2]

    @classmethod
    async def click(cls):
        await xp.run_command_once(xp.Commands["sim/autopilot/heading"])
    
    @classmethod
    def get_indication(cls):
        status = super().get_indication()
        return 0 if status == 2 else status


# F7X_SDD_Avionics_Vol1 22-21 front panel autopilot
