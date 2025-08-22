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
import aircraft_systems.engine as engine_system
import common.external_sound as sounds

from common import plane_control as pc
from aircraft_systems import engine
import common.util as util
import synoptic_remote.param_overrides as synoptic_overrides

APU_N1 = xp.Params["sim/cockpit2/electrical/APU_N1_percent"]


@scenario("MAINTENANCE", "NORMAL ENGINE START, RUNNING, SHUTDOWN", "NORMAL ENGINE START, RUNNING, SHUTDOWN")
async def m_normal_eng_start_run_shutdown(ac_state: xp_ac.ACState):
    print("NOT IMPLEMENTED")


@scenario("MAINTENANCE", "FIRE", "72 FIRE: APU")
async def m_72_fire_apu(ac_state: xp_ac.ACState):
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

        await fp.apu_disch.wait_state(1)

        await asyncio.sleep(3)
    finally:
        # fire has been succesfully extinguished
        failure = xp.Params["sim/operation/failures/rel_apu_fire"]
        await xp.set_param(failure, 0)
        await cas.remove_message(cas.FIRE_APU)
        await fpw.master_warning_lh.set_state(0)
        await fpw.master_warning_rh.set_state(0)


@scenario("MAINTENANCE", "FIRE", "74 FIRE: ENG 1")
@scenario("MAINTENANCE", "TAXI", "74 FIRE: ENG 1")
async def m_74_fire_eng_1(ac_state: xp_ac.ACState):
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


@scenario("MAINTENANCE", "FIRE", "75 FIRE: ENG 2")
@scenario("MAINTENANCE", "TAXI", "75 FIRE: ENG 2")
async def m_75_fire_eng_2(ac_state: xp_ac.ACState):
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


@scenario("MAINTENANCE", "FIRE", "76 FIRE: ENG 3")
@scenario("MAINTENANCE", "TAXI", "76 FIRE: ENG 3")
async def m_75_fire_eng_2(ac_state: xp_ac.ACState):
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


@scenario("MAINTENANCE", "N2/N1", "ENG 1: AUTO SHUTDOWN N1")
async def auto_shutdown_eng1_n1(ac_state: xp_ac.ACState):
    engine = engine_system.EngineStart1 
    fuel_flow_digital = engine_panel.en_fuel_digital_1
    cas_msg = cas.ENG_1_AUTO_SHUTDOWN
    try:
        await fuel_flow_digital.set_state(1)
        engine.broken_start = engine_system.BrokenStart.N1_BROKEN_START
        await util.wait_condition(lambda: engine.broken_start_finished == True, timeout=60)

    finally:
        await fuel_flow_digital.set_state(1)
        engine.broken_start = engine_system.BrokenStart.NORMAL_START
        await cas.remove_message(cas_msg)


@scenario("MAINTENANCE", "N2/N1", "ENG 2: AUTO SHUTDOWN N1")
async def auto_shutdown_eng2_n1(ac_state: xp_ac.ACState):
    engine = engine_system.EngineStart2 
    fuel_flow_digital = engine_panel.en_fuel_digital_2
    cas_msg = cas.ENG_2_AUTO_SHUTDOWN
    try:
        await fuel_flow_digital.set_state(1)
        engine.broken_start = engine_system.BrokenStart.N1_BROKEN_START
        await util.wait_condition(lambda: engine.broken_start_finished == True, timeout=60)

    finally:
        await fuel_flow_digital.set_state(1)
        engine.broken_start = engine_system.BrokenStart.NORMAL_START
        await cas.remove_message(cas_msg)


@scenario("MAINTENANCE", "N2/N1", "ENG 3: AUTO SHUTDOWN N1")
async def auto_shutdown_eng3_n1(ac_state: xp_ac.ACState):
    engine = engine_system.EngineStart3 
    fuel_flow_digital = engine_panel.en_fuel_digital_3
    cas_msg = cas.ENG_3_AUTO_SHUTDOWN
    try:
        await fuel_flow_digital.set_state(1)
        engine.broken_start = engine_system.BrokenStart.N1_BROKEN_START
        await util.wait_condition(lambda: engine.broken_start_finished == True, timeout=60)

    finally:
        await fuel_flow_digital.set_state(1)
        engine.broken_start = engine_system.BrokenStart.NORMAL_START
        await cas.remove_message(cas_msg)


@scenario("MAINTENANCE", "N2/N1", "ENG 1: AUTO SHUTDOWN N2")
async def auto_shutdown_eng1_n1(ac_state: xp_ac.ACState):
    engine = engine_system.EngineStart1 
    fuel_flow_digital = engine_panel.en_fuel_digital_1
    cas_msg = cas.ENG_1_AUTO_SHUTDOWN
    try:
        await fuel_flow_digital.set_state(1)
        engine.broken_start = engine_system.BrokenStart.N2_BROKEN_START
        await util.wait_condition(lambda: engine.broken_start_finished == True, timeout=60)

    finally:
        await fuel_flow_digital.set_state(1)
        engine.broken_start = engine_system.BrokenStart.NORMAL_START
        await cas.remove_message(cas_msg)


@scenario("MAINTENANCE", "N2/N1", "ENG 2: AUTO SHUTDOWN N2")
async def auto_shutdown_eng2_n1(ac_state: xp_ac.ACState):
    engine = engine_system.EngineStart2 
    fuel_flow_digital = engine_panel.en_fuel_digital_2
    cas_msg = cas.ENG_2_AUTO_SHUTDOWN
    try:
        await fuel_flow_digital.set_state(1)
        engine.broken_start = engine_system.BrokenStart.N2_BROKEN_START
        await util.wait_condition(lambda: engine.broken_start_finished == True, timeout=60)

    finally:
        await fuel_flow_digital.set_state(1)
        engine.broken_start = engine_system.BrokenStart.NORMAL_START
        await cas.remove_message(cas_msg)


@scenario("MAINTENANCE", "N2/N1", "ENG 3: AUTO SHUTDOWN N2")
async def auto_shutdown_eng3_n1(ac_state: xp_ac.ACState):
    engine = engine_system.EngineStart3 
    fuel_flow_digital = engine_panel.en_fuel_digital_3
    cas_msg = cas.ENG_3_AUTO_SHUTDOWN
    try:
        await fuel_flow_digital.set_state(1)
        engine.broken_start = engine_system.BrokenStart.N2_BROKEN_START
        await util.wait_condition(lambda: engine.broken_start_finished == True, timeout=60)

    finally:
        await fuel_flow_digital.set_state(1)
        engine.broken_start = engine_system.BrokenStart.NORMAL_START
        await cas.remove_message(cas_msg)


@scenario("MAINTENANCE", "ITT", "ENG 1: PARAM EXCEED")
async def param_exceed_eng1(ac_state: xp_ac.ACState):
    engine = engine_system.EngineStart1 
    cas_msg = cas.ENG_1_PARAM_EXCEED
    try:
        engine.broken_start = engine_system.BrokenStart.ITT_BROKEN_START
        await asyncio.sleep(60)

    finally:
        engine.broken_start = engine_system.BrokenStart.NORMAL_START
        await cas.remove_message(cas_msg)


@scenario("MAINTENANCE", "ITT", "ENG 2: PARAM EXCEED")
async def param_exceed_eng2(ac_state: xp_ac.ACState):
    engine = engine_system.EngineStart2 
    cas_msg = cas.ENG_2_PARAM_EXCEED
    try:
        engine.broken_start = engine_system.BrokenStart.ITT_BROKEN_START
        await asyncio.sleep(60)

    finally:
        engine.broken_start = engine_system.BrokenStart.NORMAL_START
        await cas.remove_message(cas_msg)


@scenario("MAINTENANCE", "ITT", "ENG 3: PARAM EXCEED")
async def param_exceed_eng3(ac_state: xp_ac.ACState):
    engine = engine_system.EngineStart3 
    cas_msg = cas.ENG_3_PARAM_EXCEED
    try:
        engine.broken_start = engine_system.BrokenStart.ITT_BROKEN_START
        await asyncio.sleep(60)

    finally:
        engine.broken_start = engine_system.BrokenStart.NORMAL_START
        await cas.remove_message(cas_msg)


@scenario("MAINTENANCE", "ITT", "ENG 1: AUTO SHUTDOWN")
async def auto_shutdown_itt_eng1(ac_state: xp_ac.ACState):
    engine = engine_system.EngineStart1 
    fuel_flow_digital = engine_panel.en_fuel_digital_1
    cas_msg_exceed = cas.ENG_1_PARAM_EXCEED
    cas_msg_shutdown = cas.ENG_1_AUTO_SHUTDOWN
    try:
        await fuel_flow_digital.set_state(1)
        engine.broken_start = engine_system.BrokenStart.ITT_BROKEN_START_AUTO_SHUTDOWN
        await util.wait_condition(lambda: engine.broken_start_finished == True, timeout=60)
        await asyncio.sleep(60)

    finally:
        await fuel_flow_digital.set_state(1)
        engine.broken_start = engine_system.BrokenStart.NORMAL_START
        await cas.remove_message(cas_msg_exceed)
        await cas.remove_message(cas_msg_shutdown)


@scenario("MAINTENANCE", "ITT", "ENG 2: AUTO SHUTDOWN")
async def auto_shutdown_itt_eng2(ac_state: xp_ac.ACState):
    engine = engine_system.EngineStart2 
    fuel_flow_digital = engine_panel.en_fuel_digital_2
    cas_msg_exceed = cas.ENG_2_PARAM_EXCEED
    cas_msg_shutdown = cas.ENG_2_AUTO_SHUTDOWN
    try:
        await fuel_flow_digital.set_state(1)
        engine.broken_start = engine_system.BrokenStart.ITT_BROKEN_START_AUTO_SHUTDOWN
        await util.wait_condition(lambda: engine.broken_start_finished == True, timeout=60)
        await asyncio.sleep(60)

    finally:
        await fuel_flow_digital.set_state(1)
        engine.broken_start = engine_system.BrokenStart.NORMAL_START
        await cas.remove_message(cas_msg_exceed)
        await cas.remove_message(cas_msg_shutdown)


@scenario("MAINTENANCE", "ITT", "ENG 3: AUTO SHUTDOWN")
async def auto_shutdown_itt_eng2(ac_state: xp_ac.ACState):
    engine = engine_system.EngineStart3 
    fuel_flow_digital = engine_panel.en_fuel_digital_3
    cas_msg_exceed = cas.ENG_3_PARAM_EXCEED
    cas_msg_shutdown = cas.ENG_3_AUTO_SHUTDOWN
    try:
        await fuel_flow_digital.set_state(1)
        engine.broken_start = engine_system.BrokenStart.ITT_BROKEN_START_AUTO_SHUTDOWN
        await util.wait_condition(lambda: engine.broken_start_finished == True, timeout=60)
        await asyncio.sleep(60)

    finally:
        await fuel_flow_digital.set_state(1)
        engine.broken_start = engine_system.BrokenStart.NORMAL_START
        await cas.remove_message(cas_msg_exceed)
        await cas.remove_message(cas_msg_shutdown)


@scenario("MAINTENANCE", "OIL", "54 ENG 1 OIL TOO LO PRESS")
async def oil_too_low_press_eng1(ac_state: xp_ac.ACState):
    OIL_PSI = xp.Params["sim/cockpit2/engine/indicators/oil_pressure_psi[0]"] 
    fuel_flow_switch = engine_panel.en_fuel_1
    cas_too_low_press = cas.ENG_1_OIL_TOO_LO_PRESS
    try:
        await xp_ac.ACState.wait_until_parameter_condition(OIL_PSI, lambda p: p > 60, timeout=60)
        async with synoptic_overrides.override_params([OIL_PSI]):
            oil_psi_curr = xp_ac.ACState.get_curr_param(OIL_PSI)
            await synoptic_overrides.linear_anim(OIL_PSI, oil_psi_curr, 10, 30)

            if fuel_flow_switch.get_state() == 1:
                await cas.show_message(cas_too_low_press)
                await fpw.master_warning_lh.set_state(1)
                await fpw.master_warning_rh.set_state(1)
                await sounds.play_sound(sounds.Sound.GONG)
                oil_psi_curr = xp_ac.ACState.get_curr_param(OIL_PSI)
                await synoptic_overrides.linear_anim(OIL_PSI, oil_psi_curr, 5, 15)
    finally:
        await cas.remove_message(cas_too_low_press)
        await fpw.master_warning_lh.set_state(0)
        await fpw.master_warning_rh.set_state(0)


@scenario("MAINTENANCE", "OIL", "55 ENG 2 OIL TOO LO PRESS")
async def oil_too_low_press_eng2(ac_state: xp_ac.ACState):
    print("NOT IMPLEMENTED")


@scenario("MAINTENANCE", "OIL", "56 ENG 3 OIL TOO LO PRESS")
async def oil_too_low_press_eng3(ac_state: xp_ac.ACState):
    print("NOT IMPLEMENTED")


@scenario("MAINTENANCE", "OIL", "ENG 1: OIL PARAM ABNORM (TEMP)")
async def oil_too_low_temp_eng1(ac_state: xp_ac.ACState):
    print("NOT IMPLEMENTED")


@scenario("MAINTENANCE", "OIL", "ENG 2: OIL PARAM ABNORM (TEMP)")
async def oil_too_low_temp_eng2(ac_state: xp_ac.ACState):
    print("NOT IMPLEMENTED")


@scenario("MAINTENANCE", "OIL", "ENG 3: OIL PARAM ABNORM (TEMP)")
async def oil_too_low_temp_eng2(ac_state: xp_ac.ACState):
    print("NOT IMPLEMENTED")


@scenario("MAINTENANCE", "OIL", "ENG 1: OIL PARAM ABNORM (PRESS)")
async def oil_too_low_press_eng1(ac_state: xp_ac.ACState):
    print("NOT IMPLEMENTED")


@scenario("MAINTENANCE", "OIL", "ENG 2: OIL PARAM ABNORM (PRESS)")
async def oil_too_low_press_eng2(ac_state: xp_ac.ACState):
    print("NOT IMPLEMENTED")


@scenario("MAINTENANCE", "OIL", "ENG 3: OIL PARAM ABNORM (PRESS)")
async def oil_too_low_press_eng2(ac_state: xp_ac.ACState):
    print("NOT IMPLEMENTED")
