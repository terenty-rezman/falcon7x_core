import asyncio
import time

from .overhead_panel import add_to_overhead_panel, TwoStateButton, Indicator
import xplane as xp
import xp_aircraft_state as xp_ac
import util


        

@add_to_overhead_panel
class apu_master(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/cockpit2/electrical/APU_generator_on"]


@add_to_overhead_panel
class apu_start_stop(TwoStateButton):
    blink = util.blink_anim(0.7)

    @classmethod
    async def on_enabled(cls):
        if xp_ac.ACState.get_curr_param_if_available(xp.Params["sim/cockpit2/electrical/APU_generator_on"]):
            await xp.begin_command(xp.Commands["sim/electrical/APU_start"])
            await asyncio.sleep(0.1)
            await xp.end_command(xp.Commands["sim/electrical/APU_start"])

    @classmethod
    async def on_disabled(cls):
        await xp.run_command_once(xp.Commands["sim/electrical/APU_off"])

    @classmethod
    def get_state(cls):
        return xp_ac.ACState.get_curr_param_if_available(xp.Params["sim/cockpit2/electrical/APU_starter_switch"])

    @classmethod
    def get_indication(cls):
        param = xp.Params["sim/cockpit2/electrical/APU_N1_percent"]

        if (val := xp_ac.ACState.get_curr_param_if_available(param)) is None:
            return

        if val < 5:
            return 0 
        elif val > 98:
            return 1
        # blink animation
        elif next(cls.blink):
            return 1
        else: 
            return 0
