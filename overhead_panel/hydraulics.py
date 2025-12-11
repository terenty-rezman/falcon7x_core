import asyncio
import time

from common.instrument_panel import add_to_panel, TwoStateButton, ThreeStateButton, NStateXPLongPressButton
import xplane.master as xp
import common.xp_aircraft_state as xp_ac
import common.util as util


@add_to_panel
class shutoff_a1(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/weapons/mis_thrust2"]
    index = 22


@add_to_panel
class shutoff_a3(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/weapons/mis_thrust2"]
    index = 23


@add_to_panel
class backup_pump(NStateXPLongPressButton):
    dataref: xp.Params = xp.Params["sim/custom/7x/selecthyd"]
    states = [1, 2, 0]


@add_to_panel
class backup_pump_on(backup_pump):
    @classmethod 
    def get_state(cls):
        if cls.override_indication is not None:
            return cls.override_indication

        return backup_pump.get_state() == 1


@add_to_panel
class backup_pump_off(backup_pump):
    @classmethod 
    def get_state(cls):
        if cls.override_indication is not None:
            return cls.override_indication

        return backup_pump.get_state() == 2


@add_to_panel
class shutoff_b2(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/weapons/mis_thrust2"]
    index = 24


@add_to_panel
class shutoff_b3(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/weapons/mis_thrust3"]
    index = 2


@add_to_panel
class shutoff_c2(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/weapons/mis_thrust3"]
    index = 3
