import asyncio

import xplane.master as xp
import common.xp_aircraft_state as xp_ac
from cas import cas
from common.scenario import scenario
import overhead_panel.dc_supply as elec
import middle_pedestal.emergency as emergency
import overhead_panel.exterior_lights as exterior_lights
import overhead_panel.windshield_heat as windshield
import overhead_panel.flight_control as fc 
import front_panel.warning as fpw
import overhead_panel.fire_panel as fp 
import overhead_panel.engines_apu as overhead_engines
import middle_pedestal.engine as engine_panel

from common import plane_control as pc
from aircraft_systems import engine
import common.util as util

APU_N1 = xp.Params["sim/cockpit2/electrical/APU_N1_percent"]


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

    await cas.remove_message(cas.ELEC_LH_RH_ESS_PWR_LO)


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

    N2 = xp.Params["sim/cockpit2/engine/indicators/N2_percent[0]"]
    await xp_ac.ACState.wait_until_parameter_condition(N2, lambda p: p < 10)

    # hide CAS msg ?
    await cas.remove_message(cas.ENG_1_OIL_TOO_LO_PRESS)
    
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
    await cas.remove_message(cas.FCS_DIRECT_LAWS_ACTIVE)


async def fcs_direct_laws_active_2(ac_state: xp_ac.ACState):
    await asyncio.sleep(5)

    # YELLOW CAS message: FCS: BOTH AILERONS FAIL
    print("FCS: BOTH AILERONS FAIL")
    await cas.show_message(cas.FCS_BOTH_AILERONS_FAIL)

    await fc.airbrake_auto.wait_state(1)

    # YELLOW CAS message: FCS: BOTH AILERONS FAIL
    await cas.remove_message(cas.FCS_BOTH_AILERONS_FAIL)


@scenario("EMERGENCY", "BLEED", "09 BLEED: 2 OVHT")
async def _09_bleed_2_ovht(ac_state: xp_ac.ACState):
    await cas.show_message(cas.BLEED_2_OVHT)


@scenario("EMERGENCY", "ENGINE", "50 ENG 2 DUCT DOOR OPEN")
async def _50_eng_2_duct_door_open(ac_state: xp_ac.ACState):
    await cas.show_message(cas.ENG_2_DUCT_DOOR_OPEN)


@scenario("EMERGENCY", "AIR CONDITIONING", "15 COND: AFT FCS BOX OVHT")
async def _15_cond_aft_fcs_box_ovht(ac_state: xp_ac.ACState):
    await cas.show_message(cas.COND_AFT_FCS_BOX_OVHT)


@scenario("EMERGENCY", "DOORS", "18 DOOR: BAG")
async def _18_door_bag(ac_state: xp_ac.ACState):
    await cas.show_message(cas.DOOR_PAX___BAG)


@scenario("EMERGENCY", "ELECTRICAL POWER", "40 ELEC: RAT GEN FAULT")
async def _40_elec_rat_gen_fault(ac_state: xp_ac.ACState):
    await cas.show_message(cas.ELEC_RAT_GEN_FAULT)


@scenario("EMERGENCY", "ENGINES", "52 ENG 2: FAIL")
async def _52_eng_2_fail(ac_state: xp_ac.ACState):
    await cas.show_message(cas.ENG_1_2_3_FAIL)


@scenario("EMERGENCY", "FCS", "60 FCS: BACK-UP ACTIVE")
async def _60_fcs_backup_active(ac_state: xp_ac.ACState):
    await cas.show_message(cas.FCS_BACK_UP_ACTIVE)


@scenario("EMERGENCY", "FCS", "69 FCS: THS PROT FAIL")
async def _69_fcs_ths_prot_fail(ac_state: xp_ac.ACState):
    await cas.show_message(cas.FCS_THS_PROT_FAIL)


@scenario("EMERGENCY", "FIRE", "72 FIRE: APU")
async def _72_fire_apu(ac_state: xp_ac.ACState):
    try:
        await xp.set_param(xp.Params["sim/operation/failures/rel_apu_fire"], 0)
        await fpw.master_warning_lh.set_state(0)
        await fpw.master_warning_rh.set_state(0)
        await fp.apu_disch.set_state(0)
        # await overhead_engines.apu_start_stop.set_state(0)

        await xp_ac.ACState.wait_until_parameter_condition(APU_N1, lambda p: p > 99)
        await asyncio.sleep(5)
        await xp.set_param(xp.Params["sim/operation/failures/rel_apu_fire"], 6)
        await fpw.master_warning_lh.set_state(1)
        await fpw.master_warning_rh.set_state(1)
        await cas.show_message(cas.FIRE_APU)

        await overhead_engines.apu_start_stop.set_state(0)
        await asyncio.sleep(1)
        engine.ApuStart.kill_self()

        # Apu fire protection system automatically closes apu fsov
        await xp.set_param(xp.Params["sim/cockpit/engine/APU_switch"], 0)

        blink = util.blink_anim(0.5)
        def blink_master(n1):
            if n1 > 1 and n1 < 6: 
                overhead_engines.apu_master.set_override_indication(next(blink))
            
            if n1 < 1:
                return True

            return False
            
        await xp_ac.ACState.wait_until_parameter_condition(APU_N1, lambda p: blink_master(p), timeout=60)

        await asyncio.sleep(25)
        await fp.apu_disch.set_state(1)

        await fp.apu_disch.wait_state(1)

        await asyncio.sleep(3)
    finally:
        # fire has been succesfully extinguished
        failure = xp.Params["sim/operation/failures/rel_apu_fire"]
        await xp.set_param(failure, 0)
        await cas.remove_message(cas.FIRE_APU)
        await fpw.master_warning_lh.set_state(0)
        await fpw.master_warning_rh.set_state(0)


@scenario("EMERGENCY", "FIRE", "74 FIRE: ENG 1")
async def _74_fire_eng_1(ac_state: xp_ac.ACState):
    try:
        await xp.set_param(xp.Params["sim/operation/failures/rel_engfir0"], 0)
        await fpw.master_warning_lh.set_state(0)
        await fpw.master_warning_rh.set_state(0)

        await engine_panel.en_fuel_1.wait_state(1)
        await asyncio.sleep(3)

        await cas.show_message(cas.FIRE_ENG_1)
        await xp.set_param(xp.Params["sim/operation/failures/rel_engfir0"], 6)

        await fpw.master_warning_lh.set_state(1)
        await fpw.master_warning_rh.set_state(1)
        await pc.pc_thrust_red_light_1.set_state(1)

        await engine_panel.en_fuel_1.wait_state(0)

        # pilot clicks shut off
        await fp.firebutton_1.wait_state(1)

        await fp.disch1_eng1.wait_state(1)
    finally:
        await xp.set_param(xp.Params["sim/operation/failures/rel_engfir0"], 0)
        await pc.pc_thrust_red_light_1.set_state(0)
        await fpw.master_warning_lh.set_state(0)
        await fpw.master_warning_rh.set_state(0)
        await cas.remove_message(cas.FIRE_ENG_1)


@scenario("EMERGENCY", "FIRE", "75 FIRE: ENG 2")
async def _75_fire_eng_2(ac_state: xp_ac.ACState):
    try:
        await xp.set_param(xp.Params["sim/operation/failures/rel_engfir1"], 0)
        await fpw.master_warning_lh.set_state(0)
        await fpw.master_warning_rh.set_state(0)

        await engine_panel.en_fuel_2.wait_state(1)
        await asyncio.sleep(3)

        await cas.show_message(cas.FIRE_ENG_2)
        await xp.set_param(xp.Params["sim/operation/failures/rel_engfir1"], 6)

        await fpw.master_warning_lh.set_state(1)
        await fpw.master_warning_rh.set_state(1)
        await pc.pc_thrust_red_light_2.set_state(1)

        await engine_panel.en_fuel_2.wait_state(0)

        # pilot clicks shut off
        await fp.firebutton_2.wait_state(1)

        await fp.disch1_eng2.wait_state(1)
    finally:
        await xp.set_param(xp.Params["sim/operation/failures/rel_engfir1"], 0)
        await pc.pc_thrust_red_light_2.set_state(0)
        await fpw.master_warning_lh.set_state(0)
        await fpw.master_warning_rh.set_state(0)
        await cas.remove_message(cas.FIRE_ENG_2)


@scenario("EMERGENCY", "FIRE", "76 FIRE: ENG 3")
async def _75_fire_eng_2(ac_state: xp_ac.ACState):
    try:
        await xp.set_param(xp.Params["sim/operation/failures/rel_engfir2"], 0)
        await fpw.master_warning_lh.set_state(0)
        await fpw.master_warning_rh.set_state(0)

        await engine_panel.en_fuel_3.wait_state(1)
        await asyncio.sleep(3)

        await cas.show_message(cas.FIRE_ENG_3)
        await xp.set_param(xp.Params["sim/operation/failures/rel_engfir2"], 6)

        await fpw.master_warning_lh.set_state(1)
        await fpw.master_warning_rh.set_state(1)
        await pc.pc_thrust_red_light_3.set_state(1)

        await engine_panel.en_fuel_3.wait_state(0)

        # pilot clicks shut off
        await fp.firebutton_3.wait_state(1)

        await fp.disch1_eng3.wait_state(1)
    finally:
        await xp.set_param(xp.Params["sim/operation/failures/rel_engfir2"], 0)
        await pc.pc_thrust_red_light_3.set_state(0)
        await fpw.master_warning_lh.set_state(0)
        await fpw.master_warning_rh.set_state(0)
        await cas.remove_message(cas.FIRE_ENG_3)


@scenario("EMERGENCY", "FIRE", "78 FIRE: REAR COMP")
async def _78_fire_rear_comp(ac_state: xp_ac.ACState):
    await cas.show_message(cas.FIRE_REAR_COMP)


@scenario("EMERGENCY", "FIRE", "80 FIRE: LH WHEEL OVHT")
async def _80_fire_lh_wheel_ovht(ac_state: xp_ac.ACState):
    await cas.show_message(cas.FIRE_LH_RH_WHEEL_OVHT)


@scenario("EMERGENCY", "HYDRAULIC", "84 HYD: A OVHT")
async def _84_hyd_a_ovht(ac_state: xp_ac.ACState):
    await cas.show_message(cas.HYD_A_OVHT)


@scenario("EMERGENCY", "PRESSURIZATION", "90 PRESS: CABIN ALT TOO HI")
async def _90_press_cabin_alt_too_hi(ac_state: xp_ac.ACState):
    await cas.show_message(cas.PRESS_CABIN_ALT_TOO_HI)


@scenario("EMERGENCY", "SPECIFIC EMERGENCY SITUATIONS", "AFCS: ADS1 MISCOMPARE AND AFCS: IRS2 MISCOMPARE")
async def afcs_ads1_miscompare_and_afcs_is2_miscompare(ac_state: xp_ac.ACState):
    await cas.show_message(cas.AFCS_ADS_MISCOMPARE)


@scenario("EMERGENCY", "OPERATING TECHNIQUES", "AIRBRAKE AUTO EXTEND FAIL")
async def airbrake_auto_extend_fail(ac_state: xp_ac.ACState):
    await cas.show_message(cas.FCS_A_B_AUTO_EXTEND_FAIL)


@scenario("EMERGENCY", "OPERATING TECHNIQUES", "AIRBRAKE AUTO RETRACT FAIL")
async def airbrake_auto_retract_fail(ac_state: xp_ac.ACState):
    await cas.show_message(cas.FCS_A_B_AUTO_RETRACT_FAIL)


@scenario("EMERGENCY", "OPERATING TECHNIQUES", "DIRECT LAWS")
async def direct_laws(ac_state: xp_ac.ACState):
    # "DIRECT LAWS" voice warning 
    pass


@scenario("EMERGENCY", "OPERATING TECHNIQUES", "INCONSISTENT OR UNRELIABLE FLIGHT DATA IN IPFD AND/OR HUD")
async def inconsistent_or_unrealiable_flight_data_in_ipfd_and_or_hud(ac_state: xp_ac.ACState):
    pass


@scenario("EMERGENCY", "OPERATING TECHNIQUES", "INCREASED SPEED ALERT")
async def increased_speed(ac_state: xp_ac.ACState):
    pass


@scenario("EMERGENCY", "LOSS OF INFORMATION", "INTERMITTENT LOSS OF ADI AND HSI DATA ON PDU")
async def intermittent_loss_of_adi_and_hsi_data_on_pdu(ac_state: xp_ac.ACState):
    pass


@scenario("EMERGENCY", "ATA 32", "LOSS OF WEIGHT ON WHEEL INFORMATION")
async def loss_of_weight_on_wheel_information(ac_state: xp_ac.ACState):
    # possible on ground
    await cas.show_message(cas.AFCS_ADS_MISCOMPARE)

    # in flight
    await cas.show_message(cas.FCS_A_B_AUTO_EXTEND_FAIL)


@scenario("EMERGENCY", "OPERATING TECHNIQUES", "OVERSPEED ALERT")
async def overspeed_alert(ac_state: xp_ac.ACState):
    pass


@scenario("EMERGENCY", "MEMORY ITEMS", "OXY PAX SUPPLY FAIL")
async def oxy_pax_supply_fail(ac_state: xp_ac.ACState):
    await cas.show_message(cas.OXY_PAX_SUPPLY_FAIL)


@scenario("EMERGENCY", "OPERATING TECHNIQUES", "SIDESTICK PRIORITY")
async def sidestick_priority(ac_state: xp_ac.ACState):
    await cas.show_message_alarm(cas.FCS_LH_SIDESTICKS_FAIL)


@scenario("EMERGENCY", "OPERATING TECHNIQUES", "TCAS ALERT")
async def tcas_alert(ac_state: xp_ac.ACState):
    # TCAS RA voice warning
    pass


@scenario("EMERGENCY", "OPERATING TECHNIQUES", "TOTAL LOSS OF NORMAL BRAKING")
async def total_loss_of_normal_braking(ac_state: xp_ac.ACState):
    await cas.show_message(cas.BRAKE_BOTH_SYSTEMS_FAIL)


@scenario("EMERGENCY", "OPERATING TECHNIQUES", "TOTAL LOSS OF NORMAL BRAKING")
async def total_loss_of_normal_braking(ac_state: xp_ac.ACState):
    await cas.show_message(cas.BRAKE_BOTH_SYSTEMS_FAIL)


@scenario("EMERGENCY", "SPECIFIC EMERGENCY SITUATIONS", "UNRELIABLE AIRSPEED")
async def unreliable_airspeed(ac_state: xp_ac.ACState):
    await cas.show_message(cas.ADS_1_2_3_4_FAIL)
    await cas.show_message(cas.FCS_DIRECT_LAWS_ACTIVE)
    await cas.show_message(cas.FCS_SLATS_M_O_AUTO_FAIL)


@scenario("EMERGENCY", "OPERATING TECHNIQUES", "UNRELIABLE AIRSPEED_OP_TECH")
async def undreliable_airspeed_op_tech(ac_state: xp_ac.ACState):
    await cas.show_message(cas.ADS_1_2_3_4_FAIL)
    await cas.show_message(cas.FCS_DIRECT_LAWS_ACTIVE)
    await cas.show_message(cas.FCS_SLATS_M_O_AUTO_FAIL)


@scenario("EMERGENCY", "OPERATING TECHNIQUES", "UNWANTED DISCONNECTION OF AUTOPILOT")
async def unwanted_desconnection_of_autopilot(ac_state: xp_ac.ACState):
    # AUTOPILOT voice warning, 
    # PDU ADI window: AP symbol flashing. 
    pass


@scenario("EMERGENCY", "OPERATING TECHNIQUES", "UNWANTED DISCONNECTION OF AUTOTHROTTLE")
async def unwanted_disconnection_of_autothrottle(ac_state: xp_ac.ACState):
    # AUTOTHROTTLE voice warning
    # PDU ADI: A/T amber flashing.
    pass
