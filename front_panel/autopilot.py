import asyncio
import time

from common.instrument_panel import add_to_panel, TwoStateButton, Indicator, PushButton, NLocalStateButton,FloatStepper, ThreeStateButton, LocalStateDiscreteSwitch
import xplane.master as xp
import common.xp_aircraft_state as xp_ac
import common.util as util
        

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
class vhf_push_lh(PushButton):
    @classmethod
    async def click(cls):
        pass


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
class fp_speed_mach_man_fms(LocalStateDiscreteSwitch):
    states = [0, 1]
    state = 0


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
class fp_hdg_trk_switch(LocalStateDiscreteSwitch):
    states = [0, 1]
    state = 0


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


@add_to_panel
class fp_pilot_side(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/cockpit/radios/ap_src"]
    states = [0, 1]


@add_to_panel
class fp_autopilot(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/cockpit/autopilot/autopilot_mode"]
    states = [1, 2, 0]

    @classmethod
    async def click(cls):
        state = cls.get_state()
        if state is None:
            return

        if state == 1:
            await cls.set_state(0) 
        else:
            await cls.set_state(1)


@add_to_panel
class fp_vs_path(FloatStepper):
    dataref: xp.Params = xp.Params["sim/weapons/targ_h"]
    index = 0

    left_most_value = -30
    right_most_value = 30
    step = 0.6

    val_type = float


@add_to_panel
class fp_clb(NLocalStateButton):
    states = [0, 1]
    state = 0

    @classmethod
    async def click(cls):
        await super().click()


@add_to_panel
class fp_vs(ThreeStateButton):
    dataref: xp.Params = xp.Params["sim/cockpit2/autopilot/vvi_status"]
    states = [0, 1, 2]

    @classmethod
    async def click(cls):
        await xp.run_command_once(xp.Commands["sim/autopilot/vertical_speed"])


@add_to_panel
class fp_vnav(ThreeStateButton):
    dataref: xp.Params = xp.Params["sim/cockpit2/autopilot/fms_vnav"]
    states = [0, 1, 2]

    @classmethod
    async def click(cls):
        await xp.run_command_once(xp.Commands["sim/autopilot/FMS"])


@add_to_panel
class fp_asel(FloatStepper):
    dataref = xp.Params["sim/cockpit2/autopilot/altitude_dial_ft"]

    left_most_value = 0
    right_most_value = 51000
    step = 100

    val_type = float


@add_to_panel
class fp_asel_ft(LocalStateDiscreteSwitch):
    states = [0, 1]
    state = 0

    @classmethod
    async def set_state(cls, state):
        if state == 0:
            fp_asel.step = 100
        else:
            fp_asel.step = 1000

        return await super().set_state(state)


@add_to_panel
class fp_alt(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/cockpit2/autopilot/altitude_hold_armed"]
    states = [1, 0]

    @classmethod
    async def click(cls):
        await xp.run_command_once(xp.Commands["sim/autopilot/altitude_hold"])


@add_to_panel
class baro_push_rh(baro_push_lh):
    pass


@add_to_panel
class baro_rot_rh(baro_rot_lh):
    pass


@add_to_panel
class fdtd_rh(fdtd_lh):
    pass


@add_to_panel
class swap_rh(swap_lh):
    pass


@add_to_panel
class vhf_push_rh(vhf_push_lh):
    pass


@add_to_panel
class vhf_control_rh(vhf_control_lh):
    pass


# F7X_SDD_Avionics_Vol1 22-21 front panel autopilot
