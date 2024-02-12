import asyncio

from .overhead_panel import add_to_overhead_panel, TwoStateButton, Indicator
import xplane as xp
import xp_aircraft_state as xp_ac


@add_to_overhead_panel("apu_master")
class apu_master(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/cockpit2/electrical/APU_generator_on"]


@add_to_overhead_panel("apu_start_stop")
class apu_start_stop(TwoStateButton):
    @classmethod
    async def on_enabled(cls):
        if xp_ac.ACState.param_available(xp.Params["sim/cockpit2/electrical/APU_generator_on"]):
            if xp_ac.ACState.curr_params[xp.Params["sim/cockpit2/electrical/APU_generator_on"]]:
                await xp.begin_command(xp.Commands["sim/electrical/APU_start"])
                await asyncio.sleep(0.1)
                await xp.end_command(xp.Commands["sim/electrical/APU_start"])

    @classmethod
    async def on_disabled(cls):
        await xp.run_command_once(xp.Commands["sim/electrical/APU_off"])

    @classmethod
    async def click(cls):
        if xp_ac.ACState.param_available(xp.Params["sim/cockpit2/electrical/APU_starter_switch"]):
            val = xp_ac.ACState.curr_params[xp.Params["sim/cockpit2/electrical/APU_starter_switch"]]
            if val == 0:
                await cls.set_enabled(True) 
            elif val == 1:
                await cls.set_enabled(False)

    @classmethod
    def get_state(cls):
        param = xp.Params["sim/cockpit2/electrical/APU_N1_percent"]

        if xp_ac.ACState.param_available(param):
            val = xp_ac.ACState.curr_params[param]

            if val < 5:
                return 0 
            elif val > 90:
                return 1
            # blink animation
            elif (val // 10) % 2 == 0:
                return 0
            else: 
                return 1
