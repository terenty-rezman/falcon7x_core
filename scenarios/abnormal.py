
import asyncio
import math

import xplane.master as xp
import common.xp_aircraft_state as xp_ac
from cas import cas
from common.scenario import scenario
import overhead_panel.dc_supply as elec
import middle_pedestal.emergency as emergency
import overhead_panel.exterior_lights as exterior_lights
import overhead_panel.windshield_heat as windshield
import overhead_panel.air_conditioning as air_condition
import middle_pedestal.wings_config as wc
import middle_pedestal.reversion as rev
import front_panel.autopilot as ap
import common.external_sound as sounds
import common.simulation as sim
import overhead_panel.anti_ice as ai
import synoptic_remote.param_overrides as synoptic_overrides
import aircraft_systems.engine as engine_system
import middle_pedestal.engine as engine_panel
import common.util as util
import front_panel.warning as fpw
import aircraft_systems.elec as elec_sys


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
    try:
        await xp.set_param(xp.Params["sim/custom/7x/z_ads_fail"], 1)
        await cas.show_message(cas.ADS_1_FAIL)
        await sounds.play_sound(sounds.Sound.GONG)
        await fpw.master_caution_lh.set_state(1)
        await fpw.master_caution_rh.set_state(1)
        await rev.rev_ads_lh.wait_state(2)
        await rev.rev_irs_lh.wait_state(2)
        await sim.sleep(3)
    finally:
        await xp.set_param(xp.Params["sim/custom/7x/z_ads_fail"], 0)
        # await xp.set_param(xp.Params["sim/custom/7x/z_ads_pilot"], 1)
        # await xp.set_param(xp.Params["sim/custom/7x/z_ads_copilot"], 2)
        # await xp.set_param(xp.Params["sim/custom/7x/z_irs_pilot"], 1)
        # await xp.set_param(xp.Params["sim/custom/7x/z_irs_copilot"], 2)
        await fpw.master_caution_lh.set_state(0)
        await fpw.master_caution_rh.set_state(0)
        await cas.remove_message(cas.ADS_1_FAIL)


@scenario("ABNORMAL", "NAVIGATION", "ADS: 2 FAIL")
async def ads_2_fail(ac_state: xp_ac.ACState):
    try:
        await xp.set_param(xp.Params["sim/custom/7x/z_ads_fail"], 2)
        await cas.show_message(cas.ADS_2_FAIL)
        await sounds.play_sound(sounds.Sound.GONG)
        await fpw.master_caution_lh.set_state(1)
        await fpw.master_caution_rh.set_state(1)
        await rev.rev_ads_rh.wait_state(2)
        await rev.rev_irs_rh.wait_state(2)
    finally:
        await cas.remove_message(cas.ADS_2_FAIL)
        await xp.set_param(xp.Params["sim/custom/7x/z_ads_fail"], 0)
        # await xp.set_param(xp.Params["sim/custom/7x/z_ads_pilot"], 1)
        # await xp.set_param(xp.Params["sim/custom/7x/z_ads_copilot"], 2)
        # await xp.set_param(xp.Params["sim/custom/7x/z_irs_pilot"], 1)
        # await xp.set_param(xp.Params["sim/custom/7x/z_irs_copilot"], 2)
        await fpw.master_caution_lh.set_state(0)
        await fpw.master_caution_rh.set_state(0)


@scenario("ABNORMAL", "NAVIGATION", "ADS: 1 NO SLIP COMPL")
async def ads_1_no_slip_comp(ac_state: xp_ac.ACState):
    NO_SLIP_ADS_ID = xp.Params["sim/custom/7x/z_no_slip_comp"]
    try:
        await cas.show_message(cas.ADS_1_NO_SLIP_COMP)
        await fpw.master_caution_lh.set_state(1)
        await fpw.master_caution_rh.set_state(1)
        await sounds.play_sound(sounds.Sound.GONG)
        await xp.set_param(NO_SLIP_ADS_ID, 1)
        await rev.rev_ads_lh.wait_state(2)
    finally:
        await cas.remove_message(cas.ADS_1_NO_SLIP_COMP)
        await xp.set_param(NO_SLIP_ADS_ID, 0)
        await fpw.master_caution_lh.set_state(0)
        await fpw.master_caution_rh.set_state(0)


@scenario("ABNORMAL", "NAVIGATION", "ADS: 1 PROBE HEAT FAIL")
async def ads_1_probe_heat_fail(ac_state: xp_ac.ACState):
    PILOT_SPEED = xp.Params["sim/cockpit2/gauges/indicators/airspeed_kts_pilot"]
    try:
        await cas.show_message(cas.ADS_1_PROBE_HEAT_FAIL)
        await sounds.play_sound(sounds.Sound.GONG)
        await fpw.master_caution_lh.set_state(1)
        await fpw.master_caution_rh.set_state(1)

        async with synoptic_overrides.override_params([PILOT_SPEED]):
            speed_curr = xp_ac.ACState.get_curr_param(PILOT_SPEED)
            speed_drop_task = synoptic_overrides.linear_anim(PILOT_SPEED, speed_curr, 60, 60)
            await rev.rev_ads_lh.wait_state(2)
            speed_drop_task.cancel()

        await rev.rev_irs_lh.wait_state(2)
    finally:
        await cas.remove_message(cas.ADS_1_PROBE_HEAT_FAIL)
        await fpw.master_caution_lh.set_state(0)
        await fpw.master_caution_rh.set_state(0)


@scenario("ABNORMAL", "AUTOFLIGHT", "AFCS: ADS ALL MISCOMPARE")
async def afcs_ads_all_miscompare(ac_state: xp_ac.ACState):
    PILOT_SPEED = xp.Params["sim/cockpit2/gauges/indicators/airspeed_kts_pilot"]
    COPILOT_SPEED = xp.Params["sim/cockpit2/gauges/indicators/airspeed_kts_copilot"]

    PILOT_ALT = xp.Params["sim/cockpit2/gauges/indicators/altitude_ft_pilot"]
    COPILOT_ALT = xp.Params["sim/cockpit2/gauges/indicators/altitude_ft_copilot"]
    try:
        await cas.show_message(cas.AFCS_ADS_ALL_MISCOMPARE)
        await sounds.play_sound(sounds.Sound.GONG)
        await fpw.master_caution_lh.set_state(1)
        await fpw.master_caution_rh.set_state(1)

        async with synoptic_overrides.override_params([PILOT_SPEED, COPILOT_SPEED, PILOT_ALT, COPILOT_ALT]):

            async def wrong_speed_pilot():
                modify_speed_pilot_task = synoptic_overrides.modify_original_value(PILOT_SPEED, lambda origin_speed, _: origin_speed + 50)
                modify_alt_pilot_task = synoptic_overrides.modify_original_value(PILOT_ALT, lambda origin_alt, _: origin_alt + 500)
                await rev.rev_ads_lh.wait_state(2)
                modify_speed_pilot_task.cancel()
                modify_alt_pilot_task.cancel()

            async def wrong_speed_copilot():
                modify_speed_copilot_task = synoptic_overrides.modify_original_value(COPILOT_SPEED, lambda origin_speed, _: origin_speed - 40)
                modify_alt_copilot_task = synoptic_overrides.modify_original_value(COPILOT_ALT, lambda origin_alt, _: origin_alt - 400)
                await rev.rev_ads_rh.wait_state(2)
                modify_speed_copilot_task.cancel()
                modify_alt_copilot_task.cancel()
            
            await asyncio.gather(wrong_speed_pilot(), wrong_speed_copilot())
    finally:
        await cas.remove_message(cas.AFCS_ADS_ALL_MISCOMPARE)
        await fpw.master_caution_lh.set_state(0)
        await fpw.master_caution_rh.set_state(0)


@scenario("ABNORMAL", "AUTOFLIGHT", "AFCS: AP FAIL")
async def afcs_ap_fail(ac_state: xp_ac.ACState):
    try:
        await cas.show_message(cas.AFCS_AP_FAIL)

        # autopilot voice warning
        await sounds.play_sound(sounds.Sound.GONG)
        await fpw.master_caution_lh.set_state(1)
        await fpw.master_caution_rh.set_state(1)

        await ap.fp_autopilot.wait_state(0)
    finally:
        await sounds.stop_all_sounds()
        await cas.remove_message(cas.AFCS_ADS_ALL_MISCOMPARE)
        await fpw.master_caution_lh.set_state(0)
        await fpw.master_caution_rh.set_state(0)


@scenario("ABNORMAL", "AUTOFLIGHT", "AFCS: IRS .. MISCOMPARE")
async def afcs_irs_miscompare(ac_state: xp_ac.ACState):
    PILOT_HEADING = xp.Params["sim/cockpit2/gauges/indicators/heading_AHARS_deg_mag_pilot"]
    try:
        await cas.show_message(cas.AFCS_IRS_1_MISCOMPARE)
        await sounds.play_sound(sounds.Sound.GONG)
        await fpw.master_caution_lh.set_state(1)
        await fpw.master_caution_rh.set_state(1)
        async with synoptic_overrides.override_params([PILOT_HEADING]):
            modify_heading_pilot_task = synoptic_overrides.modify_original_value(PILOT_HEADING, lambda origin_heading, _: origin_heading - 8)
            await rev.rev_irs_lh.wait_state(2)
            modify_heading_pilot_task.cancel()
            await cas.remove_message(cas.AFCS_IRS_1_MISCOMPARE)
    finally:
        await fpw.master_caution_lh.set_state(0)
        await fpw.master_caution_rh.set_state(0)
        await cas.remove_message(cas.AFCS_IRS_1_MISCOMPARE)


@scenario("ABNORMAL", "AUTOFLIGHT", "AFCS: IRS ALL MISCOMPARE")
async def afcs_irs_all_miscompare(ac_state: xp_ac.ACState):
    PILOT_HEADING = xp.Params["sim/cockpit2/gauges/indicators/heading_AHARS_deg_mag_pilot"]
    COPILOT_HEADING = xp.Params["sim/cockpit2/gauges/indicators/heading_AHARS_deg_mag_copilot"]

    try:
        await cas.show_message(cas.AFCS_IRS_ALL_MISCOMPARE)
        await sounds.play_sound(sounds.Sound.GONG)
        await fpw.master_caution_lh.set_state(1)
        await fpw.master_caution_rh.set_state(1)
        async with synoptic_overrides.override_params([PILOT_HEADING, COPILOT_HEADING]):

            async def wrong_heading_pilot():
                modify_heading_pilot_task = synoptic_overrides.modify_original_value(PILOT_HEADING, lambda origin_heading, _: origin_heading + 10)
                await rev.rev_irs_lh.wait_state(2)
                modify_heading_pilot_task.cancel()

            async def wrong_heading_copilot():
                modify_heading_copilot_task = synoptic_overrides.modify_original_value(COPILOT_HEADING, lambda origin_heading, _: origin_heading - 5)
                await rev.rev_irs_rh.wait_state(2)
                modify_heading_copilot_task.cancel()
            
            await asyncio.gather(wrong_heading_pilot(), wrong_heading_copilot())
    finally:
        await cas.remove_message(cas.AFCS_IRS_ALL_MISCOMPARE)
        await fpw.master_caution_lh.set_state(0)
        await fpw.master_caution_rh.set_state(0)


@scenario("ABNORMAL", "AUTOFLIGHT", "A/I: ENG.. RESID PRESS")
async def a_i_eng_1_2_3_resid_press(ac_state: xp_ac.ACState):
    try:
        await cas.show_message(cas.A_I_ENG_1_2_3_RESID_PRESS)
        await ai.ice_eng1.wait_state(1)
    finally:
        pass


@scenario("ABNORMAL", "APU", "APU: AUTO SHUTDOWN")
async def apu_auto_shutdown(ac_state: xp_ac.ACState):
    await cas.show_message(cas.APU_AUTO_SHUTDOWN)


@scenario("ABNORMAL", "INDICATING AND RECORDING SYSTEM", "AVC: DU LH HI TEMP")
async def avc_du_lh_hi_temp(ac_state: xp_ac.ACState):
    try:
        await cas.show_message(cas.AVC_DU_LH_HI_TEMP)
        await sounds.play_sound(sounds.Sound.GONG)
        await fpw.master_caution_lh.set_state(1)
        await fpw.master_caution_rh.set_state(1)

        await elec.gen2.wait_state(0)
        await elec.rh_isol.wait_state(1)
        await elec.bus_tie.wait_state(1)
    finally:
        await cas.remove_message(cas.AVC_DU_LH_HI_TEMP)
        await fpw.master_caution_lh.set_state(0)
        await fpw.master_caution_rh.set_state(0)


@scenario("ABNORMAL", "INDICATING AND RECORDING SYSTEM", "AVC: DU LW HI TEMP")
async def avc_du_lw_hi_temp(ac_state: xp_ac.ACState):
    try:
        await cas.show_message(cas.AVC_DU_LW_HI_TEMP)
        await sounds.play_sound(sounds.Sound.GONG)
        await fpw.master_caution_lh.set_state(1)
        await fpw.master_caution_rh.set_state(1)

        await elec.gen2.wait_state(0)
        await elec.rh_isol.wait_state(1)
        await elec.bus_tie.wait_state(1)
    finally:
        await fpw.master_caution_lh.set_state(0)
        await fpw.master_caution_rh.set_state(0)
        await cas.remove_message(cas.AVC_DU_LW_HI_TEMP)


@scenario("ABNORMAL", "INDICATING AND RECORDING SYSTEM", "AVC: MAU 1A FAIL")
async def avc_mau_1a_fail(ac_state: xp_ac.ACState):
    await cas.show_message(cas.AVC_MAU_1A_FAIL)


@scenario("ABNORMAL", "INDICATING AND RECORDING SYSTEM", "AVC: MAU 1A HI TEMP")
async def avc_mau_1a_hi_temp(ac_state: xp_ac.ACState):
    await cas.show_message(cas.AVC_MAU_1A_HI_TEMP)


@scenario("ABNORMAL", "BLEED AIR", "BLEED: 1 FAIL")
async def bleed_1_fail(ac_state: xp_ac.ACState):
    await cas.show_message(cas.BLEED_1_FAIL)


@scenario("ABNORMAL", "BLEED AIR", "BLEED: 1 HI TEMP")
async def bleed_1_hi_temp(ac_state: xp_ac.ACState):
    await cas.show_message(cas.BLEED_1_HI_TEMP)


@scenario("ABNORMAL", "BLEED AIR", "BLEED: XBLEED FAULT")
async def bleed_xbleed_fault(ac_state: xp_ac.ACState):
    await cas.show_message(cas.BLEED_XBLEED_FAULT)


@scenario("ABNORMAL", "BLEED AIR", "COM: AUDIO 1+2 FAIL")
async def com_audio_1_2_fail(ac_state: xp_ac.ACState):
    await cas.show_message(cas.COM_AUDIO_1_2_FAIL)


@scenario("ABNORMAL", "COMMUNICATIONS", "COM: AUDIO 1+2 FAIL")
async def com_audio_1_2_fail(ac_state: xp_ac.ACState):
    await cas.show_message(cas.COM_AUDIO_1_2_FAIL)


@scenario("ABNORMAL", "COMMUNICATIONS", "COM: VHF 1 HI TEMP")
async def com_vhf_1_hi_temp(ac_state: xp_ac.ACState):
    await cas.show_message(cas.COM_VHF_1_HI_TEMP)


@scenario("ABNORMAL", "AIR CONDITIONING AND PRESSURIZATION", "COND: BAG COMP HI TEMP")
async def cond_bag_comp_hi_temp(ac_state: xp_ac.ACState):
    await cas.show_message(cas.COND_BAG_COMP_HI_TEMP)


@scenario("ABNORMAL", "AIR CONDITIONING AND PRESSURIZATION", "COND: EMERG PACK HI TEMP")
async def cond_emerg_pack_hi_temp(ac_state: xp_ac.ACState):
    await cas.show_message(cas.COND_EMERG_PACK_HI_TEMP)


@scenario("ABNORMAL", "ELECTRICAL POWER", "ELEC: AFT DIST BOX HI TEMP")
async def elec_aft_dist_box_hi_temp(ac_state: xp_ac.ACState):
    try:
        await cas.show_message(cas.ELEC_AFT_DIST_BOX_HI_TEMP)
        await sounds.play_sound(sounds.Sound.GONG)

        air_condition.crew_temp.get_state()

        await fpw.master_caution_lh.set_state(1)
        await fpw.master_caution_rh.set_state(1)

        await emergency.ep_bag_fan.wait_state(1)

        await elec.cabin_master.wait_state(1)

        await windshield.windshield_lh.wait_state(2)
        await windshield.windshield_rh.wait_state(2)

        await air_condition.crew_temp.wait_state(lambda v: v < 0.05)
        await air_condition.fwd_temp.wait_state(lambda v: v < 0.05)
    finally: 
        await cas.remove_message(cas.ELEC_AFT_DIST_BOX_HI_TEMP)
        await fpw.master_caution_lh.set_state(0)
        await fpw.master_caution_rh.set_state(0)
        await sounds.stop_sound(sounds.Sound.GONG)


@scenario("ABNORMAL", "ELECTRICAL POWER", "ELEC: GEN 2 FAULT")
async def elec_gen_2_fault(ac_state: xp_ac.ACState):
    BAT_2_AMPS = xp.Params["sim/cockpit2/electrical/battery_amps[1]"]

    try:
        await sounds.play_sound(sounds.Sound.GONG)
        await cas.show_message(cas.ELEC_GEN_2_FAULT_A)
        await fpw.master_caution_lh.set_state(1)
        await fpw.master_caution_rh.set_state(1)

        await xp.set_param(xp.Params["sim/operation/failures/rel_genera1"], 6)
        async with synoptic_overrides.override_params([BAT_2_AMPS]):
            cur_amps = xp_ac.ACState.get_curr_param(BAT_2_AMPS) or 0
            bat_2_amps = synoptic_overrides.linear_anim(BAT_2_AMPS, cur_amps, -32, 3)

            # light gen2 off
            await elec.gen2.set_state(0)
            await elec.gen2.wait_state(0)

            await elec.gen2.wait_state(1)
            bat_2_amps.cancel()
    finally:
        await xp.set_param(xp.Params["sim/operation/failures/rel_genera1"], 0)
        await cas.remove_message(cas.ELEC_GEN_2_FAULT_A)
        await fpw.master_caution_lh.set_state(0)
        await fpw.master_caution_rh.set_state(0)


@scenario("ABNORMAL", "ELECTRICAL POWER LH SIDE", "ELEC: LH ESS PWR LO")
async def elec_lh_ess_pwr_lo(ac_state: xp_ac.ACState):
    BAT_1_AMPS = xp.Params["sim/cockpit2/electrical/battery_amps[0]"]

    try:
        await cas.show_message(cas.ELEC_LH_ESS_PWR_LO)
        await sounds.play_sound(sounds.Sound.GONG)

        await fpw.master_caution_lh.set_state(1)
        await fpw.master_caution_rh.set_state(1)

        await elec.lh_isol.set_state(3)

        await cas.show_message(cas.ELEC_GEN_1_FAULT_A)

        await xp.set_param(xp.Params["sim/operation/failures/rel_genera0"], 6)

        elec_sys.Gen1.fail = True

        async with synoptic_overrides.override_params([BAT_1_AMPS]):
            cur_amps = xp_ac.ACState.get_curr_param(BAT_1_AMPS) or 0
            bat_1_amps = synoptic_overrides.linear_anim(BAT_1_AMPS, cur_amps, -32, 3)

            async def left():
                await elec.gen1.wait_state(0)
                elec_sys.Gen1.fail = False
                await xp.set_param(xp.Params["sim/operation/failures/rel_genera0"], 0)
                await elec.gen1.wait_state(1)
                await cas.remove_message(cas.ELEC_GEN_1_FAULT_A)
                bat_1_amps.cancel()
                await synoptic_overrides.linear_anim(BAT_1_AMPS, 32, 0, 2)
            
            await elec.lh_isol.wait_state(0)
            await cas.remove_message(cas.ELEC_LH_ESS_PWR_LO)

            await left()
    finally:
        await cas.remove_message(cas.ELEC_LH_ESS_PWR_LO)
        await cas.remove_message(cas.ELEC_GEN_1_FAULT)
        await fpw.master_caution_lh.set_state(0)
        await fpw.master_caution_rh.set_state(0)
        elec_sys.Gen1.fail = False
        await xp.set_param(xp.Params["sim/operation/failures/rel_genera0"], 0)


@scenario("ABNORMAL", "ELECTRICAL POWER LH SIDE", "ELEC: LH MAIN FAULT")
async def elec_lh_main_fault(ac_state: xp_ac.ACState):
    await cas.show_message(cas.ELEC_LH_MAIN_FAULT)


@scenario("ABNORMAL", "ELECTRICAL POWER RH SIDE", "ELEC: RH ESS PWR LO")
async def elec_rh_ess_pwr_lo(ac_state: xp_ac.ACState):
    BAT_2_AMPS = xp.Params["sim/cockpit2/electrical/battery_amps[1]"]

    try:
        await cas.show_message(cas.ELEC_RH_ESS_PWR_LO)
        await sounds.play_sound(sounds.Sound.GONG)

        await fpw.master_caution_lh.set_state(1)
        await fpw.master_caution_rh.set_state(1)

        await elec.rh_isol.set_state(3)

        await cas.show_message(cas.ELEC_GEN_2_FAULT_A)

        await xp.set_param(xp.Params["sim/operation/failures/rel_genera1"], 6)

        elec_sys.Gen2.fail = True

        async with synoptic_overrides.override_params([BAT_2_AMPS]):
            cur_amps = xp_ac.ACState.get_curr_param(BAT_2_AMPS) or 0
            bat_2_amps = synoptic_overrides.linear_anim(BAT_2_AMPS, cur_amps, -32, 3)

            async def right():
                await elec.gen2.wait_state(0)
                elec_sys.Gen2.fail = False
                await xp.set_param(xp.Params["sim/operation/failures/rel_genera1"], 0)
                await elec.gen2.wait_state(1)
                await cas.remove_message(cas.ELEC_GEN_2_FAULT_A)
                bat_2_amps.cancel()
                await synoptic_overrides.linear_anim(BAT_2_AMPS, 32, 0, 2)
            
            await elec.rh_isol.wait_state(0)
            await cas.remove_message(cas.ELEC_RH_ESS_PWR_LO)

            await right()
            await fpw.master_caution_lh.set_state(0)
            await fpw.master_caution_rh.set_state(0)

    finally:
        await cas.remove_message(cas.ELEC_RH_ESS_PWR_LO)
        await cas.remove_message(cas.ELEC_GEN_2_FAULT)
        await fpw.master_caution_lh.set_state(0)
        await fpw.master_caution_rh.set_state(0)
        elec_sys.Gen2.fail = False
        await xp.set_param(xp.Params["sim/operation/failures/rel_genera1"], 0)


@scenario("ABNORMAL", "ENGINES", "ENG 2: OUT")
async def eng_2_out(ac_state: xp_ac.ACState):
    await cas.show_message(cas.ENG_2_OUT)


@scenario("ABNORMAL", "ENGINES", "ENG 2: STARTER FAIL")
async def eng_2_starter_fail(ac_state: xp_ac.ACState):
    engine = engine_system.EngineStart2 
    fuel_digital = engine_panel.en_fuel_digital_2
    fuel_switch = engine_panel.en_fuel_2
    START = xp.Params["sim/custom/7x/z_syn_eng_start2"]

    try:
        engine.broken_start = engine_system.BrokenStart.STARTER_BROKEN_START

        await sounds.play_sound(sounds.Sound.GONG)
        await fpw.master_caution_lh.set_state(1)
        await fpw.master_caution_rh.set_state(1)
        await cas.show_message(cas.ENG_2_STARTER_FAIL)
        await util.wait_condition(lambda: engine.broken_start_finished == True, timeout=60)
        await fuel_switch.wait_state(0)
    finally:
        await cas.remove_message(cas.ENG_2_STARTER_FAIL)
        await fuel_digital.set_state(1)
        await xp.set_param(START, 0)
        engine.broken_start = engine_system.BrokenStart.NORMAL_START
        await fpw.master_caution_lh.set_state(0)
        await fpw.master_caution_rh.set_state(0)


@scenario("ABNORMAL", "ENGINES", "ENGINE 1 SHUTDOWN")
async def engine_1_shutdown(ac_state: xp_ac.ACState):
    try:
        await cas.show_message(cas.ENGINE_1_SHUTDOWN)
        await sounds.play_sound(sounds.Sound.GONG, looped=True)

        await fpw.master_caution_lh.set_state(1)
        await fpw.master_caution_rh.set_state(1)

        # disable xplane engine
        await engine_panel.en_fuel_digital_1.set_state(0)

        # run our engine shutdown proc
        engine_system.Engine1ManualShutdown.manual_disable = True

        await engine_panel.en_fuel_1.wait_state(0)
    finally:
        engine_system.Engine1ManualShutdown.manual_disable = False
        await engine_panel.en_fuel_digital_1.set_state(1)
        await cas.remove_message(cas.ENGINE_1_SHUTDOWN)
        await sounds.stop_sound(sounds.Sound.GONG)
        await fpw.master_warning_lh.set_state(0)
        await fpw.master_warning_rh.set_state(0)


@scenario("ABNORMAL", "ENGINES", "ENGINE 2 SHUTDOWN")
async def engine_2_shutdown(ac_state: xp_ac.ACState):
    try:
        await cas.show_message(cas.ENGINE_2_SHUTDOWN)
        await sounds.play_sound(sounds.Sound.GONG, looped=True)

        await fpw.master_caution_lh.set_state(1)
        await fpw.master_caution_rh.set_state(1)

        # disable xplane engine
        await engine_panel.en_fuel_digital_2.set_state(0)

        # run our engine shutdown proc
        engine_system.Engine2ManualShutdown.manual_disable = True

        await engine_panel.en_fuel_2.wait_state(0)
    finally:
        engine_system.Engine2ManualShutdown.manual_disable = False
        await engine_panel.en_fuel_digital_2.set_state(1)
        await cas.remove_message(cas.ENGINE_2_SHUTDOWN)
        await sounds.stop_sound(sounds.Sound.GONG)
        await fpw.master_warning_lh.set_state(0)
        await fpw.master_warning_rh.set_state(0)


@scenario("ABNORMAL", "FLIGHT CONTROL: AILERONS", "FCS: AILERON DEGRAD")
async def fcs_aileron_degrad(ac_state: xp_ac.ACState):
    await cas.show_message(cas.FCS_AILERON_DEGRAD)


@scenario("ABNORMAL", "FLIGHT CONTROL: FLAPS", "FCS: FLAP ASYM")
async def fcs_flap_asym(ac_state: xp_ac.ACState):
    await cas.show_message(cas.FCS_FLAP_ASYM)


@scenario("ABNORMAL", "FLIGHT CONTROL: FLAPS", "FCS: FLAP FAIL")
async def fcs_flap_fail(ac_state: xp_ac.ACState):
    await cas.show_message(cas.FCS_FLAP_FAIL)


@scenario("ABNORMAL", "FLIGHT CONTROL: SLATS", "FCS: SLATS M+O EXTEND FAIL")
async def fcs_slats_m_o_extend_fail(ac_state: xp_ac.ACState):
    await cas.show_message(cas.FCS_SLATS_M_O_EXTEND_FAIL)


@scenario("ABNORMAL", "FUEL", "FUEL: ENG 2 LO PRESS")
async def fcs_slats_m_o_extend_fail(ac_state: xp_ac.ACState):
    await cas.show_message(cas.FCS_SLATS_M_O_EXTEND_FAIL)


@scenario("ABNORMAL", "FUEL", "FUEL: ENG 2 LO PRESS")
async def fuel_eng_2_lo_press(ac_state: xp_ac.ACState):
    await cas.show_message(cas.FUEL_ENG_2_LO_PRESS)


@scenario("ABNORMAL", "FUEL", "FUEL: X-BP 1-3 FAULT")
async def fuel_x_bp_1_3_fault(ac_state: xp_ac.ACState):
    await cas.show_message(cas.FUEL_X_BP_1_3_FAULT)


@scenario("ABNORMAL", "LANDING GEAR AND BRAKES", "GEAR: DOOR NOT CLOSED")
async def gear_door_not_closed(ac_state: xp_ac.ACState):
    await cas.show_message(cas.GEAR_DOOR_NOT_CLOSED)


@scenario("ABNORMAL", "HYDRAULIC", "HYD: B HI TEMP")
async def hyd_b_hi_temp(ac_state: xp_ac.ACState):
    await cas.show_message(cas.HYD_B_HI_TEMP)


@scenario("ABNORMAL", "HYDRAULIC", "HYD: B HI TEMP")
async def hyd_b_lo_press(ac_state: xp_ac.ACState):
    await cas.show_message(cas.HYD_B_LO_PRESS)


@scenario("ABNORMAL", "ELECTRICAL POWER INOPERATIVE BUSES", "LH ESS BUS INOPERATIVE")
async def some_function(ac_state: xp_ac.ACState):
    pass


@scenario("ABNORMAL", "ELECTRICAL POWER INOPERATIVE BUSES", "LH MAIN + RH MAIN BUSES INOPERATIVE")
async def avc_mau_1a_2b_fail(ac_state: xp_ac.ACState):
    await cas.show_message(cas.AVC_MAU_1A_2B_FAIL)


async def fuel_eng_1_3_lo_press(ac_state: xp_ac.ACState):
    await cas.show_message(cas.FUEL_ENG_1_3_LO_PRESS)


@scenario("ABNORMAL", "ELECTRICAL POWER INOPERATIVE BUSES", "LH MAIN BUS INOPERATIVE")
async def some_function(ac_state: xp_ac.ACState):
    pass


@scenario("ABNORMAL", " AIR CONDITIONING AND PRESSURIZATION", "PRESS: BAG VENT LO")
async def press_bag_vent_lo(ac_state: xp_ac.ACState):
    await cas.show_message(cas.PRESS_BAG_VENT_LO)


@scenario("ABNORMAL", "ELECTRICAL POWER INOPERATIVE BUSES", "RH ESS BUS INOPERATIVE")
async def some_function(ac_state: xp_ac.ACState):
    pass


@scenario("ABNORMAL", "ELECTRICAL POWER INOPERATIVE BUSES", "RH MAIN BUS INOPERATIVE")
async def some_function(ac_state: xp_ac.ACState):
    pass


@scenario("ABNORMAL", "ENGINES", "STARTER ASSISTED RELIGHT")
async def some_function(ac_state: xp_ac.ACState):
    pass
