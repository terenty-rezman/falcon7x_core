import asyncio
import time

from .overhead_panel import add_to_overhead_panel, TwoStateButton, ThreeStateButton, FloatSwitch, DiscreteSwitch, PushButton
import xplane as xp
import xp_aircraft_state as xp_ac
import util


@add_to_overhead_panel
class il_emerge_lights(DiscreteSwitch):
    dataref: xp.Params = xp.Params["sim/weapons/warhead_type"]
    states = [2, 1, 0, 3]
    index = 7

    @classmethod
    def get_state(cls):
        state = super().get_state()

        if state is None:
            return

        if state > 2:
            return 2

        return state

    @classmethod
    async def click(cls):
        state = cls.get_state()
        if state is None:
            return

        if state > 2:
            await cls.set_state(0) 
        else:
            await cls.set_state(state)

    @classmethod
    def get_indication(cls):
        param = xp_ac.ACState.get_curr_param(xp.Params["sim/cockpit2/switches/generic_lights_switch"])
        if param is None:
            return 0
        
        param = param[0]
        return param


@add_to_overhead_panel
class il_fasten(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/cockpit2/switches/fasten_seat_belts"]


@add_to_overhead_panel
class il_smoking(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/cockpit2/switches/no_smoking"]


@add_to_overhead_panel
class il_cabin(ThreeStateButton):
    dataref: xp.Params = xp.Params["sim/custom/7x/paxlum"]
    states = [1, 2, 0]


@add_to_overhead_panel
class rain_rplint_rh(PushButton):
    @classmethod
    async def click(cls):
        pass
