
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

