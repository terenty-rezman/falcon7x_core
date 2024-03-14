
import asyncio
import time

from instrument_panel import add_to_panel, TwoStateButton, ThreeStateButton, FloatSwitch, DiscreteSwitch
import xplane as xp


@add_to_panel
class pax_oxygen(DiscreteSwitch):
    dataref: xp.Params = xp.Params["sim/weapons/target_index"]
    index = 1
    states = [1, 2, 3, 0]
