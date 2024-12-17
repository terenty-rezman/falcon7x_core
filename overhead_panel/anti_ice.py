import asyncio
import time

from common.instrument_panel import add_to_panel, TwoStateButton, ThreeStateButton, FloatSwitch, DiscreteSwitch
import xplane.master as xp


@add_to_panel
class ice_wings(ThreeStateButton):
    dataref: xp.Params = xp.Params["sim/custom/7x/AIwingsel"]


@add_to_panel
class ice_wings_stby(ice_wings):
    @classmethod
    def get_state(cls):
        return ice_wings.get_state() == 1


@add_to_panel
class ice_wings_on(ice_wings):
    @classmethod
    def get_state(cls):
        return ice_wings.get_state() == 2


@add_to_panel
class ice_brake(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/weapons/mis_thrust2"]
    index = 3


@add_to_panel
class ice_eng1(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/cockpit2/ice/ice_inlet_heat_on_per_engine"]
    index = 0


@add_to_panel
class ice_eng2(ThreeStateButton):
    dataref: xp.Params = xp.Params["sim/custom/7x/AIengcentre"]


@add_to_panel
class ice_eng2_on(ice_eng2):
    @classmethod
    def get_state(cls):
        return ice_eng2.get_state() == 2


@add_to_panel
class ice_eng2_stby(ice_eng2):
    @classmethod
    def get_state(cls):
        return ice_eng2.get_state() == 1


@add_to_panel
class ice_eng3(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/cockpit2/ice/ice_inlet_heat_on_per_engine"]
    index = 2
