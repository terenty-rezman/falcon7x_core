
import asyncio
import time

from instrument_panel import add_to_panel, TwoStateButton, Indicator, PushButton, NLocalStateButton, LocalStateIndicator, FloatStepper, array_str
import xplane as xp
import xp_aircraft_state as xp_ac
import util
        
# F7X_SDD_Avionics_Vol1.pdf

@add_to_panel
class en_motor(TwoStateButton):
    @classmethod
    async def set_state(cls, state):
        pass


@add_to_panel
class en_ign(TwoStateButton):
    @classmethod
    async def set_state(cls, state):
        pass


@add_to_panel
class en_normal(TwoStateButton):
    @classmethod
    async def set_state(cls, state):
        pass


@add_to_panel
class en_start(TwoStateButton):
    @classmethod
    async def set_state(cls, state):
        val = array_str(3, state) 
        await xp.set_param(xp.Params["sim/weapons/warhead_type"], val)


@add_to_panel
class en_fuel_off_1(TwoStateButton):
    idx = 0
    @classmethod
    async def set_state(cls, state):
        if state == 1:
            val = array_str(cls.idx, 0) 
            await xp.set_param(xp.Params["sim/weapons/warhead_type"], val)


@add_to_panel
class en_fuel_on_1(TwoStateButton):
    idx = 0
    @classmethod
    async def set_state(cls, state):
        if state == 1:
            val = array_str(cls.idx, 1) 
            await xp.set_param(xp.Params["sim/weapons/warhead_type"], val)


@add_to_panel
class en_fuel_off_2(en_fuel_off_1):
    idx = 1


@add_to_panel
class en_fuel_on_2(en_fuel_on_1):
    idx = 1


@add_to_panel
class en_fuel_off_3(en_fuel_off_1):
    idx = 2


@add_to_panel
class en_fuel_on_3(en_fuel_on_1):
    idx = 2
