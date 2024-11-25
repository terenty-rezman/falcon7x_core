
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


@scenario("ABNORMAL", "NAVIGATION", "ADS: 1 PROBE HEAT FAIL")
async def ads_1_probe_heat_fail(ac_state: xp_ac.ACState):
    await cas.show_message(cas.ADS_1_PROBE_HEAT_FAIL)


@scenario("ABNORMAL", "AUTOFLIGHT", "AFCS: ADS ALL MISCOMPARE")
async def afcs_ads_all_miscompare(ac_state: xp_ac.ACState):
    await cas.show_message(cas.AFCS_ADS_ALL_MISCOMPARE)


@scenario("ABNORMAL", "AUTOFLIGHT", "AFCS: AP FAIL")
async def afcs_ap_fail(ac_state: xp_ac.ACState):
    await cas.show_message(cas.AFCS_AP_FAIL)


@scenario("ABNORMAL", "AUTOFLIGHT", "AFCS: IRS .. MISCOMPARE")
async def afcs_irs_miscompare(ac_state: xp_ac.ACState):
    await cas.show_message(cas.AFCS_IRS_MISCOMPARE)


@scenario("ABNORMAL", "AUTOFLIGHT", "AFCS: IRS ALL MISCOMPARE")
async def afcs_irs_all_miscompare(ac_state: xp_ac.ACState):
    await cas.show_message(cas.AFCS_IRS_ALL_MISCOMPARE)


@scenario("ABNORMAL", "AUTOFLIGHT", "A/I: ENG.. RESID PRESS")
async def a_i_eng_1_2_3_resid_press(ac_state: xp_ac.ACState):
    await cas.show_message(cas.A_I_ENG_1_2_3_RESID_PRESS)


@scenario("ABNORMAL", "APU", "APU: AUTO SHUTDOWN")
async def apu_auto_shutdown(ac_state: xp_ac.ACState):
    await cas.show_message(cas.APU_AUTO_SHUTDOWN)


@scenario("ABNORMAL", "INDICATING AND RECORDING SYSTEM", "AVC: DU LH HI TEMP")
async def avc_du_lh_hi_temp(ac_state: xp_ac.ACState):
    await cas.show_message(cas.AVC_DU_LH_HI_TEMP)


@scenario("ABNORMAL", "INDICATING AND RECORDING SYSTEM", "AVC: DU LW HI TEMP")
async def avc_du_lw_hi_temp(ac_state: xp_ac.ACState):
    await cas.show_message(cas.AVC_DU_LW_HI_TEMP)


@scenario("ABNORMAL", "INDICATING AND RECORDING SYSTEM", "AVC: MAU 1A FAIL")
async def avc_mau_1a_fail(ac_state: xp_ac.ACState):
    await cas.show_message(cas.AVC_MAU_1A_FAIL)


@scenario("ABNORMAL", "INDICATING AND RECORDING SYSTEM", "AVC: MAU 1A HI TEMP")
async def avc_mau_1a_hi_temp(ac_state: xp_ac.ACState):
    await cas.show_message(cas.AVC_MAU_1A_HI_TEMP)


@scenario("ABNORMAL", "BLEED AIR", "BLEED: 1 FAIL")
async def bleed_1_fail(ac_state: xp_ac.ACState):
    await cas.show_message(cas.BLEED_1_FAIL)