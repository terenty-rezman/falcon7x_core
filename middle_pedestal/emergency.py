
import asyncio
import time

from instrument_panel import add_to_panel, TwoStateButton, Indicator, PushButton, NLocalStateButton, LocalStateIndicator, FloatStepper
import xplane as xp
import xp_aircraft_state as xp_ac
import util
        
# F7X_SDD_Avionics_Vol1.pdf

@add_to_panel
class elec_rh_ess(NLocalStateButton):
    states = [0, 1]
    state = 0

    @classmethod
    async def click(cls):
        await super().click()
