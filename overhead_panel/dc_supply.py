import asyncio
import time

from .overhead_panel import add_to_overhead_panel, TwoStateButton, ThreeStateButton, array_str
import xplane as xp


@add_to_overhead_panel
class galley_master(ThreeStateButton):
    dataref: xp.Params = xp.Params["sim/weapons/mis_thrust2"]
    index = 5

    state1_val = 2
    state2_val = 0
    state3_val = 1 

    @classmethod
    def get_indication(cls):
        state = super().get_state()
        if state == 0:
            return 0
        if state == 1:
            return 2
        if state == 2:
            return 1
