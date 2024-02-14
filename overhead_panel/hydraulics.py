import asyncio
import time

from .overhead_panel import add_to_overhead_panel, TwoStateButton, Indicator, array_str
import xplane as xp
import xp_aircraft_state as xp_ac
import util


@add_to_overhead_panel
class shutoff_a1(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/weapons/mis_thrust2"]
    index = 22
    enabled_val = array_str(index, "1")
    disabled_val = array_str(index, "0")


@add_to_overhead_panel
class shutoff_a2(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/weapons/mis_thrust2"]
    index = 23
    enabled_val = array_str(index, "1")
    disabled_val = array_str(index, "0")
