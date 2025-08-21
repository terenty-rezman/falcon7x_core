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


@scenario("MAINTENANCE", "ENGINE", "AUTO SHUTDOWN ENG1 N1")
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


@scenario("MAINTENANCE", "ENGINE", "AUTO SHUTDOWN ENG2 N1")
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


@scenario("MAINTENANCE", "ENGINE", "AUTO SHUTDOWN ENG3 N1")
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


@scenario("MAINTENANCE", "ENGINE", "AUTO SHUTDOWN ENG1 N2")
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


@scenario("MAINTENANCE", "ENGINE", "AUTO SHUTDOWN ENG2 N2")
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


@scenario("MAINTENANCE", "ENGINE", "AUTO SHUTDOWN ENG3 N2")
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


@scenario("MAINTENANCE", "ENGINE", "ENG1 PARAM EXCEED")
async def param_exceed_eng1(ac_state: xp_ac.ACState):
    engine = engine_system.EngineStart1 
    cas_msg = cas.ENG_1_PARAM_EXCEED
    try:
        engine.broken_start = engine_system.BrokenStart.ITT_BROKEN_START
        await asyncio.sleep(60)

    finally:
        engine.broken_start = engine_system.BrokenStart.NORMAL_START
        await cas.remove_message(cas_msg)


@scenario("MAINTENANCE", "ENGINE", "ENG2 PARAM EXCEED")
async def param_exceed_eng2(ac_state: xp_ac.ACState):
    engine = engine_system.EngineStart2 
    cas_msg = cas.ENG_2_PARAM_EXCEED
    try:
        engine.broken_start = engine_system.BrokenStart.ITT_BROKEN_START
        await asyncio.sleep(60)

    finally:
        engine.broken_start = engine_system.BrokenStart.NORMAL_START
        await cas.remove_message(cas_msg)


@scenario("MAINTENANCE", "ENGINE", "ENG3 PARAM EXCEED")
async def param_exceed_eng3(ac_state: xp_ac.ACState):
    engine = engine_system.EngineStart3 
    cas_msg = cas.ENG_3_PARAM_EXCEED
    try:
        engine.broken_start = engine_system.BrokenStart.ITT_BROKEN_START
        await asyncio.sleep(60)

    finally:
        engine.broken_start = engine_system.BrokenStart.NORMAL_START
        await cas.remove_message(cas_msg)


@scenario("MAINTENANCE", "ENGINE", "ENG1 AUTO SHUTDOWN ITT")
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


@scenario("MAINTENANCE", "ENGINE", "ENG2 AUTO SHUTDOWN ITT")
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


@scenario("MAINTENANCE", "ENGINE", "ENG3 AUTO SHUTDOWN ITT")
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


@scenario("MAINTENANCE", "ENGINE", "ENG1 OIL TOO LOW PRESS")
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
