

import asyncio

import xplane as xp
import xp_aircraft_state as xp_ac
from cas import cas
from scenario import scenario
import overhead_panel.dc_supply as elec
import middle_pedestal.emergency as emergency
import overhead_panel.exterior_lights as exterior_lights
import overhead_panel.windshield_heat as windshield
import middle_pedestal.wings_config as wc


@scenario("NORMAL", None, "POWER ON")
async def power_on(ac_state: xp_ac.ACState):
    pass
