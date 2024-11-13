import asyncio

import xplane as xp
import xp_aircraft_state as xp_ac
from cas import cas
from scenario import scenario
import overhead_panel.dc_supply as elec
import middle_pedestal.emergency as emergency
import overhead_panel.exterior_lights as exterior_lights
import overhead_panel.windshield_heat as windshield
import overhead_panel.flight_control as fc 


@scenario("EMERGENCY", "ELECTRICAL POWER", "26 ELEC: AFT DIST BOX OVHT")
async def _26_elec_aft_dist_box_ovht(ac_state: xp_ac.ACState):
    await asyncio.sleep(5)

    # RED CAS message + sound
    await cas.show_message_alarm(cas.ELEC_AFT_DIST_BOX_OVHT)

    await emergency.ep_elec_rh_ess.wait_state(1)

    await elec.bus_tie.wait_state(0)

    await elec.rh_isol.wait_state(1)

    await elec.cabin_master.wait_state(1)

    # OFF
    await exterior_lights.el_landing_lh.wait_state(0)
    await exterior_lights.el_landing_rh.wait_state(0)

    # OFF
    await exterior_lights.el_taxi.wait_state(0)
    await exterior_lights.el_wing.wait_state(0)

    # OFF
    await windshield.windshield_lh.wait_state(1)
    await windshield.windshield_rh.wait_state(1)


@scenario("EMERGENCY", "ELECTRICAL POWER", "36 ELEC: LH+RH ESS PWR LO")
async def _36_elec_lh_rh_ess_pwr_lo(ac_state: xp_ac.ACState):
    await asyncio.sleep(5)

    # red cas message + sound
    await cas.show_message_alarm(cas.ELEC_LH_RH_ESS_PWR_LO)

    # set elec rh + lh to isol
    await elec.lh_isol.set_state(1)
    await elec.rh_isol.set_state(1)
    # light gen2 off
    await elec.gen2.set_state(1)

    # wait for rh + lh tied
    await elec.lh_isol.wait_state(0)
    await elec.rh_isol.wait_state(0)

    # wait gen2 on
    await elec.gen2.wait_state(0)

    await cas.hide_message(cas.ELEC_LH_RH_ESS_PWR_LO)


@scenario("EMERGENCY", "ELECTRICAL POWER", "38 ELEC GEN 1+2+3 FAULT")
async def _38_elec_gen_2_fault(ac_state: xp_ac.ACState):
    await asyncio.sleep(5)

    # YELLOW CAS message
    await cas.show_message_alarm(cas.ELEC_GEN_1_2_3_FAULT)

    # light gen2 off
    await elec.gen2.set_state(1)

    # wait gen2 on
    await elec.gen2.wait_state(0)

    # light gen2 on unsuccessfull - light gen2 off again
    await elec.gen2.set_state(1)

    await elec.bus_tie.wait_state(1)

    # wind shield AUTO
    await windshield.windshield_lh.wait_state(0)
    await windshield.windshield_rh.wait_state(0)


@scenario("EMERGENCY", "ENGINES", "54 ENG 1 OIL TOO LO PRESS")
async def _54_eng1_oil_too_low_press(ac_state: xp_ac.ACState):
    await asyncio.sleep(5)

    # RED CAS message + sound: 54 ENG 1 OIL TOO LOW PRESS
    await cas.show_message_alarm(cas.ENG_1_OIL_TOO_LO_PRESS)

    # PDU automatically shows ENG TRM
    await xp.set_param(xp.Params["sim/7x/choixtcas"], 1)

    await xp.set_param(xp.Params["sim/custom/7x/z_eng1_oil_press_override"], 1)
    await xp.set_param(xp.Params["sim/custom/7x/z_eng1_oil_press"], 0)

    N2 = xp.Params["sim/cockpit2/engine/indicators/N2_percent"]
    await xp_ac.ACState.wait_until_parameter_condition(N2, lambda p: p[0] < 10)

    # hide CAS msg ?
    await cas.hide_message(cas.ENG_1_OIL_TOO_LO_PRESS)
    
    # restore original oil pressure
    await xp.set_param(xp.Params["sim/custom/7x/z_eng1_oil_press_override"], 0)


@scenario("EMERGENCY", "FCS", "66 FCS: DIRECT LAWS ACTIVE")
async def _66_fcs_direct_laws_active(ac_state: xp_ac.ACState):
    await asyncio.sleep(5)

    # RED CAS message: FCS: DIRECT LAWS ACTIVE
    await cas.show_message(cas.FCS_DIRECT_LAWS_ACTIVE)

    await fc.airbrake_auto.wait_state(1)

    # YELLOW CAS message: FCS: MFCC FAULT
    await cas.show_message(cas.FCS_MFCC_FAULT)

    await fc.fcs_engage_stby.wait_state(1)

    # hide RED CAS message: FCS: DIRECT LAWS ACTIVE
    await cas.hide_message(cas.FCS_DIRECT_LAWS_ACTIVE)


async def fcs_direct_laws_active_2(ac_state: xp_ac.ACState):
    await asyncio.sleep(5)

    # YELLOW CAS message: FCS: BOTH AILERONS FAIL
    print("FCS: BOTH AILERONS FAIL")
    await cas.show_message(cas.FCS_BOTH_AILERONS_FAIL)

    await fc.airbrake_auto.wait_state(1)

    # YELLOW CAS message: FCS: BOTH AILERONS FAIL
    await cas.hide_message(cas.FCS_BOTH_AILERONS_FAIL)


@scenario("EMERGENCY", "ELECTRICAL POWER", "26 ELEC: AFT DIST BOX OVHT")
async def _26_elec_aft_dist_box_ovht(ac_state: xp_ac.ACState):
    await asyncio.sleep(5)

    # RED CAS message + sound
    await cas.show_message_alarm(cas.ELEC_AFT_DIST_BOX_OVHT)

    await emergency.ep_elec_rh_ess.wait_state(1)

    await elec.bus_tie.wait_state(0)

    await elec.rh_isol.wait_state(1)

    await elec.cabin_master.wait_state(1)

    # OFF
    await exterior_lights.el_landing_lh.wait_state(0)
    await exterior_lights.el_landing_rh.wait_state(0)

    # OFF
    await exterior_lights.el_taxi.wait_state(0)
    await exterior_lights.el_wing.wait_state(0)

    # OFF
    await windshield.windshield_lh.wait_state(1)
    await windshield.windshield_rh.wait_state(1)
