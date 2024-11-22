
import asyncio
import math

import xplane.master as xp
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

    def sf_3(sf):
        return math.isclose(sf, 1, rel_tol=0.05)

    await wc.wc_sf.wait_state(sf_3)

    print("1")


@scenario("ABNORMAL", "ICE AND RAIN PROTECTION", "A/I: WINGS FAULT")
async def a_i_wings_fault(ac_state: xp_ac.ACState):
    await cas.show_message(cas.A_I_WINGS_FAULT)


@scenario("ABNORMAL", "ICE AND RAIN PROTECTION", "A/I: STALL WARNING OFFSET")
async def a_i_stall_warning_offset(ac_state: xp_ac.ACState):
    await cas.show_message(cas.A_I_STALL_WARNING_OFFSET)


@scenario("ABNORMAL", "ENGINES", "ABNORMAL START")
async def abnormal_start(ac_state: xp_ac.ACState):
    pass


@scenario("ABNORMAL", "NAVIGATION", "ADS: 1 FAIL")
async def ads_1_fail(ac_state: xp_ac.ACState):
    await cas.show_message(cas.ADS_1_FAIL)


@scenario("ABNORMAL", "NAVIGATION", "ADS: 2 FAIL")
async def ads_2_fail(ac_state: xp_ac.ACState):
    await cas.show_message(cas.ADS_2_FAIL)


@scenario("ABNORMAL", "NAVIGATION", "ADS: 1 NO SLIP COMPL")
async def ads_1_no_slip_comp(ac_state: xp_ac.ACState):
    await cas.show_message(cas.ADS_1_NO_SLIP_COMP)