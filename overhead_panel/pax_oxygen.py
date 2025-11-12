
import asyncio
import time

from common.instrument_panel import add_to_panel, TwoStateButton, ThreeStateButton, FloatSwitch, DiscreteSwitch
import xplane.master as xp


@add_to_panel
class pax_oxygen(DiscreteSwitch):
    dataref: xp.Params = xp.Params["sim/weapons/target_index"]
    index = 1
    states = [1, 2, 3, 0]


@add_to_panel
class pax_oxygen_closed(pax_oxygen):
    @classmethod
    async def set_state(cls, state):
        if state == 1:
            await super().set_state(3)


@add_to_panel
class pax_oxygen_firstaid(pax_oxygen):
    @classmethod
    async def set_state(cls, state):
        if state == 1:
            await super().set_state(1)


@add_to_panel
class pax_oxygen_normal(pax_oxygen):
    @classmethod
    async def set_state(cls, state):
        if state == 1:
            await super().set_state(0)


@add_to_panel
class pax_oxygen_oride(pax_oxygen):
    @classmethod
    async def set_state(cls, state):
        if state == 1:
            await super().set_state(2)
