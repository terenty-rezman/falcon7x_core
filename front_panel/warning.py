import asyncio
import time

from instrument_panel import add_to_panel, TwoStateButton, Indicator, PushButton
import xplane as xp
import xp_aircraft_state as xp_ac
import util
        

@add_to_panel
class pty_lh(Indicator):
    dataref: xp.Params = xp.Params["sim/weapons/mis_thrust2"]
    index = 15


@add_to_panel
class master_warning(TwoStateButton):
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
