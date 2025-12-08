import asyncio
import time

from common.instrument_panel import add_to_panel, TwoStateButton, Indicator, PushButton
import xplane.master as xp
import common.xp_aircraft_state as xp_ac
import common.util as util
import common.simulation as sim
        

@add_to_panel
class eng_1(PushButton):
    @classmethod
    async def click(cls):
        pass


@add_to_panel
class eng_2(PushButton):
    @classmethod
    async def click(cls):
        pass


@add_to_panel
class eng_3(PushButton):
    @classmethod
    async def click(cls):
        pass


@add_to_panel
class apu_master(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/cockpit2/electrical/APU_generator_on"]

    blink = util.blink_anim(0.5)
    blink_timer = None

    @classmethod
    async def set_state(cls, state):
        if state == 1:
            cls.blink_timer = util.Timer()
            cls.blink_timer.start()
        else:
            cls.blink_timer = None
            
        return await super().set_state(state)

    @classmethod
    def get_indication(cls):
        if cls.override_indication is not None:
            return cls.override_indication

        if cls.blink_timer:
            if cls.blink_timer.elapsed() < 4:
                return next(cls.blink)
            else:
                cls.blink_timer = None
            
        return cls.get_state() or 0


@add_to_panel
class apu_start_stop(TwoStateButton):
    blink = util.blink_anim(0.7)

    @classmethod
    async def set_state(cls, state):
        if state == 1:
            if xp_ac.ACState.get_curr_param(xp.Params["sim/cockpit2/electrical/APU_generator_on"]):
                await xp.begin_command(xp.Commands["sim/electrical/APU_start"])
                await sim.sleep(0.1)
                await xp.end_command(xp.Commands["sim/electrical/APU_start"])
        elif state == 0:
            await xp.run_command_once(xp.Commands["sim/electrical/APU_off"])

    @classmethod
    def get_state(cls):
        state = xp_ac.ACState.get_curr_param(xp.Params["sim/cockpit2/electrical/APU_running"])
        if state:
            return 1
        else:
            return 0

    @classmethod
    def get_indication(cls):
        if cls.override_indication is not None:
            return cls.override_indication

        param = xp.Params["sim/cockpit2/electrical/APU_N1_percent"]

        if (val := xp_ac.ACState.get_curr_param(param)) is None:
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
