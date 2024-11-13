
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


@scenario("ABNORMAL", "ICE AND RAIN PROTECTION", "A/I: STALL WARNING OFFSET")
async def a_i_stall_warning_offset(ac_state: xp_ac.ACState):
    await cas.show_message(cas.A_I_STALL_WARNING_OFFSET)


@scenario("ABNORMAL", "ICE AND RAIN PROTECTION", "A/I: WINGS FAULT")
async def a_i_stall_warning_offset(ac_state: xp_ac.ACState):
    await cas.show_message(cas.A_I_WINGS_FAULT)
