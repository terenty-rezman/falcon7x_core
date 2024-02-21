import asyncio
import time

from .overhead_panel import add_to_overhead_panel, TwoStateButton, ThreeStateButton, array_str
import xplane as xp
import xp_aircraft_state as xp_ac
import util


@add_to_overhead_panel
class shutoff_a1(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/weapons/mis_thrust2"]
    index = 22


@add_to_overhead_panel
class shutoff_a2(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/weapons/mis_thrust2"]
    index = 23


@add_to_overhead_panel
class backup_pump(ThreeStateButton):
    dataref: xp.Params = xp.Params["sim/custom/7x/selecthyd"]
    states = [1, 2, 0]


@add_to_overhead_panel
class shutoff_b2(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/weapons/mis_thrust2"]
    index = 24


@add_to_overhead_panel
class shutoff_b3(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/weapons/mis_thrust3"]
    index = 2


@add_to_overhead_panel
class shutoff_c2(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/weapons/mis_thrust3"]
    index = 3
