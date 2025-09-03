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
import common.simulation as sim

APU_N1 = xp.Params["sim/cockpit2/electrical/APU_N1_percent"]


@scenario("MAINTENANCE", "NORMAL ENGINE START, RUNNING, SHUTDOWN", "NORMAL ENGINE START, RUNNING, SHUTDOWN")
async def m_normal_eng_start_run_shutdown(ac_state: xp_ac.ACState):
    N1_1 = xp.Params["sim/cockpit2/engine/indicators/N1_percent[0]"]
    N2_1 = xp.Params["sim/cockpit2/engine/indicators/N2_percent[0]"]
    ITT_1 = xp.Params["sim/cockpit2/engine/indicators/ITT_deg_C[0]"] 
    OIL_PSI_1 = xp.Params["sim/cockpit2/engine/indicators/oil_pressure_psi[0]"] 
    OIL_TEMP_1 = xp.Params["sim/cockpit2/engine/indicators/oil_temperature_deg_C[0]"]
    FF_1 = xp.Params["sim/cockpit2/engine/indicators/fuel_flow_kg_sec[0]"]

    N1_2 = xp.Params["sim/cockpit2/engine/indicators/N1_percent[1]"]
    N2_2 = xp.Params["sim/cockpit2/engine/indicators/N2_percent[1]"]
    ITT_2 = xp.Params["sim/cockpit2/engine/indicators/ITT_deg_C[1]"] 
    OIL_PSI_2 = xp.Params["sim/cockpit2/engine/indicators/oil_pressure_psi[1]"] 
    OIL_TEMP_2 = xp.Params["sim/cockpit2/engine/indicators/oil_temperature_deg_C[1]"]
    FF_2 = xp.Params["sim/cockpit2/engine/indicators/fuel_flow_kg_sec[1]"]

    N1_3 = xp.Params["sim/cockpit2/engine/indicators/N1_percent[2]"]
    N2_3 = xp.Params["sim/cockpit2/engine/indicators/N2_percent[2]"]
    ITT_3 = xp.Params["sim/cockpit2/engine/indicators/ITT_deg_C[2]"] 
    OIL_PSI_3 = xp.Params["sim/cockpit2/engine/indicators/oil_pressure_psi[2]"] 
    OIL_TEMP_3 = xp.Params["sim/cockpit2/engine/indicators/oil_temperature_deg_C[2]"]
    FF_3 = xp.Params["sim/cockpit2/engine/indicators/fuel_flow_kg_sec[2]"]
    MAX_THRUST_1 = xp.Params["sim/custom/7x/z_thrust_purple_max_deg_1"]
    MAX_THRUST_2 = xp.Params["sim/custom/7x/z_thrust_purple_max_deg_2"]
    MAX_THRUST_3 = xp.Params["sim/custom/7x/z_thrust_purple_max_deg_3"]

    await xp.set_param(MAX_THRUST_1, 30)
    await xp.set_param(MAX_THRUST_2, 30)
    await xp.set_param(MAX_THRUST_3, 30)

    async with synoptic_overrides.override_params([
            ITT_1, N1_1, N2_1, FF_1, OIL_PSI_1, OIL_TEMP_1,
            ITT_2, N1_2, N2_2, FF_2, OIL_PSI_2, OIL_TEMP_2,
            ITT_3, N1_3, N2_3, FF_3, OIL_PSI_3, OIL_TEMP_3
        ]):
        while True:
            await sim.sleep(2)


@scenario("MAINTENANCE", "FIRE", "72 FIRE: APU")
async def m_72_fire_apu(ac_state: xp_ac.ACState):
    try:
        await xp.set_param(xp.Params["sim/operation/failures/rel_apu_fire"], 0)
        await fpw.master_warning_lh.set_state(0)
        await fpw.master_warning_rh.set_state(0)
        await fp.apu_disch.set_state(0)
        # await overhead_engines.apu_start_stop.set_state(0)

        await xp_ac.ACState.wait_until_parameter_condition(APU_N1, lambda p: p > 99)
        await sim.sleep(5)
        await xp.set_param(xp.Params["sim/operation/failures/rel_apu_fire"], 6)
        await fpw.master_warning_lh.set_state(1)
        await fpw.master_warning_rh.set_state(1)
        await cas.show_message(cas.FIRE_APU)

        await overhead_engines.apu_start_stop.set_state(0)
        await sim.sleep(1)
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

        await sim.sleep(3)
    finally:
        # fire has been succesfully extinguished
        failure = xp.Params["sim/operation/failures/rel_apu_fire"]
        await xp.set_param(failure, 0)
        await cas.remove_message(cas.FIRE_APU)
        await fpw.master_warning_lh.set_state(0)
        await fpw.master_warning_rh.set_state(0)


@scenario("MAINTENANCE", "FIRE", "74 FIRE: ENG 1")
@scenario("MAINTENANCE", "TAXI", "74 FIRE: ENG 1")
class m_fire_eng_1:
    fire_failure = xp.Params["sim/operation/failures/rel_engfir0"]
    engine_fuel_switch = engine_panel.en_fuel_1
    cas_fire_msg = cas.FIRE_ENG_1 
    thrust_red_light = pc.pc_thrust_red_light_1
    firebutton = fp.firebutton_1
    disch = fp.disch1_eng1

    @classmethod
    async def procedure(cls, ac_state: xp_ac.ACState):
        try:
            await xp.set_param(cls.fire_failure, 0)
            await fpw.master_warning_lh.set_state(0)
            await fpw.master_warning_rh.set_state(0)

            await cls.engine_fuel_switch.wait_state(1)
            await sim.sleep(3)

            await cas.show_message(cls.cas_fire_msg)
            await xp.set_param(cls.fire_failure, 6)

            await sounds.play_sound(sounds.Sound.FIRE_BELL, looped=True)

            await fpw.master_warning_lh.set_state(1)
            await fpw.master_warning_rh.set_state(1)
            await cls.thrust_red_light.set_state(1)

            await cls.engine_fuel_switch.wait_state(0)

            # pilot clicks shut off
            await cls.firebutton.wait_state(1)

            await cls.disch.wait_state(1)
        finally:
            await xp.set_param(cls.fire_failure, 0)
            await sounds.stop_sound(sounds.Sound.FIRE_BELL)
            await cls.thrust_red_light.set_state(0)
            await fpw.master_warning_lh.set_state(0)
            await fpw.master_warning_rh.set_state(0)
            await cas.remove_message(cls.cas_fire_msg)


@scenario("MAINTENANCE", "FIRE", "75 FIRE: ENG 2")
@scenario("MAINTENANCE", "TAXI", "75 FIRE: ENG 2")
class m_fire_eng_2(m_fire_eng_1):
    fire_failure = xp.Params["sim/operation/failures/rel_engfir1"]
    engine_fuel_switch = engine_panel.en_fuel_2
    cas_fire_msg = cas.FIRE_ENG_2 
    thrust_red_light = pc.pc_thrust_red_light_2
    firebutton = fp.firebutton_2
    disch = fp.disch1_eng2


@scenario("MAINTENANCE", "FIRE", "76 FIRE: ENG 3")
@scenario("MAINTENANCE", "TAXI", "76 FIRE: ENG 3")
class m_fire_eng_3(m_fire_eng_1):
    fire_failure = xp.Params["sim/operation/failures/rel_engfir2"]
    engine_fuel_switch = engine_panel.en_fuel_3
    cas_fire_msg = cas.FIRE_ENG_3 
    thrust_red_light = pc.pc_thrust_red_light_3
    firebutton = fp.firebutton_3
    disch = fp.disch1_eng3


@scenario("MAINTENANCE", "N2/N1", "ENG 1: AUTO SHUTDOWN N1")
class m_auto_shutdown_eng1_n1:
    engine = engine_system.EngineStart1 
    fuel_flow_digital = engine_panel.en_fuel_digital_1
    cas_msg = cas.ENG_1_AUTO_SHUTDOWN

    @classmethod
    async def procedure(cls):
        try:
            engine.broken_start_finished = False
            await cls.fuel_flow_digital.set_state(1)
            engine.broken_start = engine_system.BrokenStart.N1_BROKEN_START
            await util.wait_condition(lambda: engine.broken_start_finished == True, timeout=60)

        finally:
            await cls.fuel_flow_digital.set_state(1)
            engine.broken_start = engine_system.BrokenStart.NORMAL_START
            await cas.remove_message(cls.cas_msg)


@scenario("MAINTENANCE", "N2/N1", "ENG 2: AUTO SHUTDOWN N1")
class m_auto_shutdown_eng2_n1(m_auto_shutdown_eng1_n1):
    engine = engine_system.EngineStart2 
    fuel_flow_digital = engine_panel.en_fuel_digital_2
    cas_msg = cas.ENG_2_AUTO_SHUTDOWN


@scenario("MAINTENANCE", "N2/N1", "ENG 3: AUTO SHUTDOWN N1")
class m_auto_shutdown_eng3_n1(m_auto_shutdown_eng1_n1):
    engine = engine_system.EngineStart3 
    fuel_flow_digital = engine_panel.en_fuel_digital_3
    cas_msg = cas.ENG_3_AUTO_SHUTDOWN


@scenario("MAINTENANCE", "N2/N1", "ENG 1: AUTO SHUTDOWN N2")
class m_auto_shutdown_eng1_n2:
    engine = engine_system.EngineStart1 
    fuel_flow_digital = engine_panel.en_fuel_digital_1
    cas_msg = cas.ENG_1_AUTO_SHUTDOWN

    @classmethod
    async def procedure(cls):
        try:
            engine.broken_start_finished = False
            await cls.fuel_flow_digital.set_state(1)
            engine.broken_start = engine_system.BrokenStart.N2_BROKEN_START
            await util.wait_condition(lambda: engine.broken_start_finished == True, timeout=60)

        finally:
            await cls.fuel_flow_digital.set_state(1)
            engine.broken_start = engine_system.BrokenStart.NORMAL_START
            await cas.remove_message(cls.cas_msg)


@scenario("MAINTENANCE", "N2/N1", "ENG 2: AUTO SHUTDOWN N2")
class m_auto_shutdown_eng2_n2(m_auto_shutdown_eng1_n2):
    engine = engine_system.EngineStart2 
    fuel_flow_digital = engine_panel.en_fuel_digital_2
    cas_msg = cas.ENG_2_AUTO_SHUTDOWN


@scenario("MAINTENANCE", "N2/N1", "ENG 3: AUTO SHUTDOWN N2")
class m_auto_shutdown_eng3_n2(m_auto_shutdown_eng1_n2):
    engine = engine_system.EngineStart3 
    fuel_flow_digital = engine_panel.en_fuel_digital_3
    cas_msg = cas.ENG_3_AUTO_SHUTDOWN


@scenario("MAINTENANCE", "ITT", "ENG 1: PARAM EXCEED")
class m_param_exceed_eng1:
    engine = engine_system.EngineStart1 
    cas_msg = cas.ENG_1_PARAM_EXCEED

    @classmethod
    async def procedure(cls):
        try:
            cls.engine.broken_start_finished = False
            cls.engine.broken_start = engine_system.BrokenStart.ITT_BROKEN_START
            await sim.sleep(60)

        finally:
            cls.engine.broken_start = engine_system.BrokenStart.NORMAL_START
            await cas.remove_message(cls.cas_msg)


@scenario("MAINTENANCE", "ITT", "ENG 2: PARAM EXCEED")
class m_param_exceed_eng2(m_param_exceed_eng1):
    engine = engine_system.EngineStart2 
    cas_msg = cas.ENG_2_PARAM_EXCEED


@scenario("MAINTENANCE", "ITT", "ENG 3: PARAM EXCEED")
class m_param_exceed_eng3(m_param_exceed_eng1):
    engine = engine_system.EngineStart3 
    cas_msg = cas.ENG_3_PARAM_EXCEED


@scenario("MAINTENANCE", "ITT", "ENG 1: AUTO SHUTDOWN")
class m_auto_shutdown_itt_eng1:
    engine = engine_system.EngineStart1 
    fuel_flow_digital = engine_panel.en_fuel_digital_1
    cas_msg_exceed = cas.ENG_1_PARAM_EXCEED
    cas_msg_shutdown = cas.ENG_1_AUTO_SHUTDOWN

    @classmethod
    async def procedure(cls):
        try:
            cls.engine.broken_start_finished = False
            await cls.fuel_flow_digital.set_state(1)
            cls.engine.broken_start = engine_system.BrokenStart.ITT_BROKEN_START_AUTO_SHUTDOWN
            await util.wait_condition(lambda: cls.engine.broken_start_finished == True, timeout=60)
            await sim.sleep(60)

        finally:
            await cls.fuel_flow_digital.set_state(1)
            cls.engine.broken_start = engine_system.BrokenStart.NORMAL_START
            await cas.remove_message(cls.cas_msg_exceed)
            await cas.remove_message(cls.cas_msg_shutdown)


@scenario("MAINTENANCE", "ITT", "ENG 2: AUTO SHUTDOWN")
class m_auto_shutdown_itt_eng2(m_auto_shutdown_itt_eng1):
    engine = engine_system.EngineStart2 
    fuel_flow_digital = engine_panel.en_fuel_digital_2
    cas_msg_exceed = cas.ENG_2_PARAM_EXCEED
    cas_msg_shutdown = cas.ENG_2_AUTO_SHUTDOWN


@scenario("MAINTENANCE", "ITT", "ENG 3: AUTO SHUTDOWN")
class m_auto_shutdown_itt_eng3(m_auto_shutdown_itt_eng1):
    engine = engine_system.EngineStart3 
    fuel_flow_digital = engine_panel.en_fuel_digital_3
    cas_msg_exceed = cas.ENG_3_PARAM_EXCEED
    cas_msg_shutdown = cas.ENG_3_AUTO_SHUTDOWN


@scenario("MAINTENANCE", "OIL", "54 ENG 1 OIL TOO LO PRESS")
class m_oil_too_low_press_eng1:
    OIL_PSI = xp.Params["sim/cockpit2/engine/indicators/oil_pressure_psi[0]"] 
    fuel_flow_switch = engine_panel.en_fuel_1
    cas_too_low_press = cas.ENG_1_OIL_TOO_LO_PRESS
    engine_custom_specs = engine.Engine1CustomSpecs

    @classmethod
    async def procedure(cls):
        try:
            await xp_ac.ACState.wait_until_parameter_condition(cls.OIL_PSI, lambda p: p > 43, timeout=60)
            async with synoptic_overrides.override_params([cls.OIL_PSI]):
                oil_psi_curr = xp_ac.ACState.get_curr_param(cls.OIL_PSI)
                cls.engine_custom_specs.emulate_oil_psi = False
                await synoptic_overrides.linear_anim(cls.OIL_PSI, oil_psi_curr, 10, 30)

                if cls.fuel_flow_switch.get_state() == 1:
                    await cas.show_message(cls.cas_too_low_press)
                    await fpw.master_warning_lh.set_state(1)
                    await fpw.master_warning_rh.set_state(1)
                    await sounds.play_sound(sounds.Sound.GONG, looped=True)
                    oil_psi_curr = xp_ac.ACState.get_curr_param(cls.OIL_PSI)
                    await synoptic_overrides.linear_anim(cls.OIL_PSI, oil_psi_curr, 5, 15)
                await sim.sleep(5)
        finally:
            await cas.remove_message(cls.cas_too_low_press)
            await fpw.master_warning_lh.set_state(0)
            await fpw.master_warning_rh.set_state(0)
            cls.engine_custom_specs.emulate_oil_psi = True


@scenario("MAINTENANCE", "OIL", "55 ENG 2 OIL TOO LO PRESS")
class m_oil_too_low_press_eng2(m_oil_too_low_press_eng1):
    OIL_PSI = xp.Params["sim/cockpit2/engine/indicators/oil_pressure_psi[1]"] 
    fuel_flow_switch = engine_panel.en_fuel_2
    cas_too_low_press = cas.ENG_2_OIL_TOO_LO_PRESS
    engine_custom_specs = engine.Engine2CustomSpecs


@scenario("MAINTENANCE", "OIL", "56 ENG 3 OIL TOO LO PRESS")
class m_oil_too_low_press_eng3(m_oil_too_low_press_eng1):
    OIL_PSI = xp.Params["sim/cockpit2/engine/indicators/oil_pressure_psi[2]"] 
    fuel_flow_switch = engine_panel.en_fuel_3
    cas_too_low_press = cas.ENG_3_OIL_TOO_LO_PRESS
    engine_custom_specs = engine.Engine3CustomSpecs


@scenario("MAINTENANCE", "OIL", "ENG 1: OIL PARAM ABNORM (TEMP)")
class m_oil_param_abnorm_temp_eng1:
    OIL_TEMP = xp.Params["sim/cockpit2/engine/indicators/oil_temperature_deg_C[0]"]
    cas_msg_oil_abnormal = cas.ENG_1_OIL_PARAM_ABNORM
    N1 = xp.Params["sim/cockpit2/engine/indicators/N1_percent[0]"]
    engine_custom_specs = engine.Engine1CustomSpecs

    @classmethod
    async def procedure(cls, ac_state: xp_ac.ACState):
        try:
            await xp_ac.ACState.wait_until_parameter_condition(cls.N1, lambda p: p > 67, timeout=60)
            # await xp_ac.ACState.wait_until_parameter_condition(cls.OIL_TEMP, lambda p: p > 25, timeout=60)
            async with synoptic_overrides.override_params([cls.OIL_TEMP]):
                oil_temp_curr = xp_ac.ACState.get_curr_param(cls.OIL_TEMP)
                cls.engine_custom_specs.emulate_oil_temp = False
                temp_grow_coro = synoptic_overrides.linear_anim(cls.OIL_TEMP, oil_temp_curr, 147, 60)
                n1_pilot_decrease = xp_ac.ACState.wait_until_parameter_condition(cls.N1, lambda p: p < 40, timeout=60)

                done, pending = await asyncio.wait([temp_grow_coro, n1_pilot_decrease], return_when=asyncio.FIRST_COMPLETED)

                if temp_grow_coro in done:
                    [p.cancel() for p in pending]
                    await cas.show_message(cls.cas_msg_oil_abnormal)

                    await fpw.master_caution_lh.set_state(1)
                    await fpw.master_caution_rh.set_state(1)
                    await sounds.play_sound(sounds.Sound.GONG, looped=True)

                    await xp_ac.ACState.wait_until_parameter_condition(cls.N1, lambda p: p < 67, timeout=60)
                    temp_drop_coro = synoptic_overrides.linear_anim(cls.OIL_TEMP, 147, 95, 180)

                    async def on_temp_drop():
                        await xp_ac.ACState.wait_until_parameter_condition(cls.OIL_TEMP, lambda p: p < 145, timeout=60)
                        await cas.remove_message(cls.cas_msg_oil_abnormal)
                        await fpw.master_caution_lh.set_state(0)
                        await fpw.master_caution_rh.set_state(0)
                        await sounds.stop_sound(sounds.Sound.GONG)

                    await asyncio.gather(temp_drop_coro, on_temp_drop())
                    cls.engine_custom_specs.emulate_oil_temp = True
                else:
                    [p.cancel() for p in pending]
                    cls.engine_custom_specs.emulate_oil_temp = True
                    await sim.sleep(5)
        finally:
            await sounds.stop_sound(sounds.Sound.GONG)
            await cas.remove_message(cls.cas_msg_oil_abnormal)
            await fpw.master_caution_lh.set_state(0)
            await fpw.master_caution_rh.set_state(0)
            cls.engine_custom_specs.emulate_oil_temp = True


@scenario("MAINTENANCE", "OIL", "ENG 2: OIL PARAM ABNORM (TEMP)")
class m_oil_param_abnorm_temp_eng2(m_oil_param_abnorm_temp_eng1):
    OIL_TEMP = xp.Params["sim/cockpit2/engine/indicators/oil_temperature_deg_C[1]"]
    cas_msg_oil_abnormal = cas.ENG_2_OIL_PARAM_ABNORM
    N1 = xp.Params["sim/cockpit2/engine/indicators/N1_percent[1]"]
    engine_custom_specs = engine.Engine2CustomSpecs


@scenario("MAINTENANCE", "OIL", "ENG 3: OIL PARAM ABNORM (TEMP)")
class m_oil_param_abnorm_temp_eng3(m_oil_too_low_press_eng1):
    OIL_TEMP = xp.Params["sim/cockpit2/engine/indicators/oil_temperature_deg_C[2]"]
    cas_msg_oil_abnormal = cas.ENG_3_OIL_PARAM_ABNORM
    N1 = xp.Params["sim/cockpit2/engine/indicators/N1_percent[2]"]
    engine_custom_specs = engine.Engine3CustomSpecs


@scenario("MAINTENANCE", "OIL", "ENG 1: OIL PARAM ABNORM (PRESS)")
async def oil_too_low_press_eng1(ac_state: xp_ac.ACState):
    print("NOT IMPLEMENTED")


@scenario("MAINTENANCE", "OIL", "ENG 2: OIL PARAM ABNORM (PRESS)")
async def oil_too_low_press_eng2(ac_state: xp_ac.ACState):
    print("NOT IMPLEMENTED")


@scenario("MAINTENANCE", "OIL", "ENG 3: OIL PARAM ABNORM (PRESS)")
async def oil_too_low_press_eng2(ac_state: xp_ac.ACState):
    print("NOT IMPLEMENTED")
