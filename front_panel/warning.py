import asyncio
import time

from instrument_panel import add_to_panel, TwoStateButton, Indicator, PushButton, NLocalStateButton
import xplane as xp
import xp_aircraft_state as xp_ac
import util
        

# F7X_SDD_Avionics_Vol1 31-11 front panel warnings

@add_to_panel
class pty_lh(Indicator):
    dataref: xp.Params = xp.Params["sim/weapons/mis_thrust2"]
    index = 15


@add_to_panel
class master_warning_lh(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/cockpit2/annunciators/master_warning"]
    blink = util.blink_anim(0.5)

    @classmethod
    async def click(cls):
        command = xp.Commands["sim/annunciator/clear_master_warning"]
        await xp.run_command_once(command)

        param = xp.Params["sim/cockpit2/annunciators/plugin_master_warning"]
        await xp.set_param(param, 0)

    @classmethod
    def get_indication(cls):
        state = cls.get_state()

        if state == 1:
            return next(cls.blink) 
        
        return 0


@add_to_panel
class master_caution_lh(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/cockpit2/annunciators/master_caution"]
    blink = util.blink_anim(0.5)

    @classmethod
    async def click(cls):
        command = xp.Commands["sim/annunciator/clear_master_caution"]
        await xp.run_command_once(command)

        param = xp.Params["sim/cockpit2/annunciators/plugin_master_caution"]
        await xp.set_param(param, 0)

    @classmethod
    def get_indication(cls):
        state = cls.get_state()

        if state == 1:
            return next(cls.blink) 
        
        return 0


@add_to_panel
class sil_aural_alarm_lh(PushButton):
    @classmethod
    async def click(cls):
        pass


@add_to_panel
class fms_msg_lh(NLocalStateButton):
    states = [0, 1]
    state = 0

    @classmethod
    async def click(cls):
        await super().click()


@add_to_panel
class event_lh(NLocalStateButton):
    states = [0, 1]
    state = 0

    @classmethod
    async def click(cls):
        await super().click()

# F7X_SDD_Avionics_Vol1 22-21 front panel autopilot
