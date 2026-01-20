import asyncio
import time

from common.instrument_panel import add_to_panel, TwoStateButton, Indicator, PushButton, NLocalStateButton, LocalStateIndicator
import xplane.master as xp
from xplane.params import Params, Commands
import common.xp_aircraft_state as xp_ac
import common.util as util
import common.external_sound as sounds
from cas import cas
        

# F7X_SDD_Avionics_Vol1 31-11 front panel warnings

@add_to_panel
class pty_lh(LocalStateIndicator):
    states = [0, 1]
    state = 0


@add_to_panel
class master_warning_lh(TwoStateButton):
    dataref: Params = Params["sim/cockpit2/annunciators/master_warning"]
    blink = util.blink_anim(0.5)

    # @classmethod
    # async def click(cls):
    #     command = Commands["sim/annunciator/clear_master_warning"]
    #     await xp.run_command_once(command)

    #     param = Params["sim/cockpit2/annunciators/plugin_master_warning"]
    #     await xp.set_param(param, 0)
    
    @classmethod
    async def set_state(cls, state):
        param = Params["sim/cockpit2/annunciators/plugin_master_warning"]

        if state == 0:
            command = Commands["sim/annunciator/clear_master_warning"]
            await xp.run_command_once(command)
            await xp.set_param(param, 0)
        else:
            await xp.set_param(param, 1)
        
        await cas.read_messages()


    @classmethod
    def get_indication(cls):
        if cls.override_indication is not None:
            return cls.override_indication

        state = cls.get_state()

        if state == 1:
            return next(cls.blink) 
        
        return 0


@add_to_panel
class master_caution_lh(TwoStateButton):
    dataref: Params = Params["sim/cockpit2/annunciators/plugin_master_caution"]
    blink = util.blink_anim(0.5)

    @classmethod
    async def set_state(cls, state):
        if state == 0:
            command = Commands["sim/annunciator/clear_master_caution"]
            await xp.run_command_once(command)
            await xp.set_param(cls.dataref, 0)
        else:
            await xp.set_param(cls.dataref, 1)

        await cas.read_messages()

    @classmethod
    def get_indication(cls):
        if cls.override_indication is not None:
            return cls.override_indication

        state = cls.get_state()

        if state == 1:
            return next(cls.blink) 
        
        return 0


@add_to_panel
class sil_aural_alarm_lh(PushButton):
    @classmethod
    async def click(cls):
        await sounds.stop_all_sounds()


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


@add_to_panel
class event_rh(NLocalStateButton):
    states = [0, 1]
    state = 0

    @classmethod
    async def click(cls):
        await super().click()


@add_to_panel
class fms_msg_rh(NLocalStateButton):
    states = [0, 1]
    state = 0

    @classmethod
    async def click(cls):
        await super().click()


@add_to_panel
class sil_aural_alarm_rh(sil_aural_alarm_lh):
    pass


@add_to_panel
class master_caution_rh(master_caution_lh):
    pass


@add_to_panel
class master_warning_rh(master_warning_lh):
    pass


@add_to_panel
class pty_rh(LocalStateIndicator):
    states = [0, 1]
    state = 0

# F7X_SDD_Avionics_Vol1 22-21 front panel autopilot
