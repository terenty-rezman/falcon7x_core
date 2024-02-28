import asyncio
import time

from .overhead_panel import add_to_overhead_panel, TwoStateButton, ThreeStateButton, FloatSwitch, DiscreteSwitch
import xplane as xp


@add_to_overhead_panel
class wings(ThreeStateButton):
    dataref: xp.Params = xp.Params["sim/custom/7x/AIwingsel"]


@add_to_overhead_panel
class ice_brake(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/weapons/mis_thrust2"]
    index = 3


@add_to_overhead_panel
class ice_eng1(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/cockpit2/ice/ice_inlet_heat_on_per_engine"]
    index = 0


@add_to_overhead_panel
class ice_eng2(ThreeStateButton):
    dataref: xp.Params = xp.Params["sim/custom/7x/AIengcentre"]


@add_to_overhead_panel
class ice_eng3(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/cockpit2/ice/ice_inlet_heat_on_per_engine"]
    index = 2
