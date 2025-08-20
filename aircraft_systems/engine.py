import enum
import asyncio
import time

import numpy as np
import simple_pid

import common.xp_aircraft_state as xp_ac
import common.util as util
import xplane.master as xp
import common.sane_tasks as sane_tasks
import overhead_panel.fire_panel as fp 

from aircraft_systems.system_base import System
from xplane.params import Params
import middle_pedestal.engine as engine_panel
import overhead_panel.engines_apu as overhead_engines
import overhead_panel.fuel as fuel
import synoptic_remote.param_overrides as synoptic_overrides
import front_panel.warning as warning
from cas import cas


class ApuStart(System):
    APU_N1 = xp.Params["sim/cockpit2/electrical/APU_N1_percent"]
    APU_TEMP = xp.Params["sim/cockpit2/electrical/APU_EGT_c"]
    APU_STRATUP_STAGE = xp.Params["sim/custom/7x/z_apu_startup_stage"]
    BATTERY_1 = xp.Params["sim/cockpit2/electrical/battery_on[0]"]
    BAT_1_AMPS = xp.Params["sim/cockpit2/electrical/battery_amps[0]"]
    BAT_2_AMPS = xp.Params["sim/cockpit2/electrical/battery_amps[1]"]
    APU_AMPS = xp.Params["sim/cockpit2/electrical/APU_generator_amps"]

    TIME_SAMPLE = [0, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 37, 40, 43, 44, 45, 46, 47, 48, 49, 30] # time
    N1_SAMPLE = [0, 3, 6, 17, 26, 30, 37, 39, 44, 47, 53, 57, 63, 68, 71, 78, 82, 90, 93, 95, 96, 97, 98, 99, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100] # n1
    TEMP_SAMPLE = [10, 10, 10, 39, 145, 154, 170, 191, 256, 279, 293, 294, 288, 276, 268, 247, 239, 220, 216, 212, 207, 212, 218, 228, 234, 245, 247, 245, 243, 240, 240, 240, 240, 240, 240] # apu temp
    BAT_1_AMPS_SAMPLE = [450, 522, 450, 380, 322, 240, 182, 162, 100, 82, 74.4, 66.8, 59.2, 51.6, 44, 44, 44, 44, 44, 44, 44, 44, 44, 44, 44, 44, 44, -118, -96, -70, -58, -50, -42, -30, -35]
    BAT_2_AMPS_SAMPLE = [86, 86, 86, 86, 86, 86, 86, 86, 80, 62, 56, 50, 44, 38, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, -50, -48, -40, -30, -34, -28, -24, -24]
    APU_AMPS_SAMPLE = [-610, -516, -459.514, -389.492, -322, -249.448, -180, -143, -56, -52, -41.6, -31.2, -20.8, -10.4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 238, 214, 182, 168, 152, 142, 134, 130]

    logic_task = None

    @classmethod
    def start_condition(cls):
        avail = [
            xp_ac.ACState.param_available(cls.APU_N1),
            xp_ac.ACState.param_available(cls.APU_TEMP),
        ]

        if not all(avail):
            return False

        cond = [
            overhead_engines.apu_master.get_state() == 1,
            xp_ac.ACState.get_curr_param(cls.APU_N1) < 15,
            overhead_engines.apu_start_stop.get_state() == 1
        ]

        return all(cond)

    @classmethod
    async def system_logic_task(cls):
        async with synoptic_overrides.override_params([cls.APU_N1, cls.APU_TEMP, cls.BAT_1_AMPS, cls.BAT_2_AMPS, cls.APU_AMPS]):
            async def n1():
                await synoptic_overrides._1d_table_anim(
                    cls.APU_N1, cls.TIME_SAMPLE, cls.N1_SAMPLE
                )

            async def temp():
                await synoptic_overrides._1d_table_anim(
                    cls.APU_TEMP, cls.TIME_SAMPLE, cls.TEMP_SAMPLE)
            
            async def elec_tab():
                await asyncio.sleep(1)
                await xp.set_param(cls.APU_STRATUP_STAGE, 1)

                await xp_ac.ACState.wait_until_parameter_condition(cls.APU_N1, lambda p: p > 50, timeout=60)
                await xp.set_param(cls.APU_STRATUP_STAGE, 2)
                
                await xp_ac.ACState.wait_until_parameter_condition(cls.APU_N1, lambda p: p > 94, timeout=60)
                await xp.set_param(cls.APU_STRATUP_STAGE, 3)

                await xp_ac.ACState.wait_until_parameter_condition(cls.APU_N1, lambda p: p > 99, timeout=60)
                await asyncio.sleep(3)
                await xp.set_param(cls.APU_STRATUP_STAGE, 4)

                await asyncio.sleep(2)
                await xp.set_param(cls.APU_STRATUP_STAGE, 0)

            async def bat1():
                async with synoptic_overrides.override_params([cls.BATTERY_1]):
                    synoptic_overrides.set_override_value(cls.BATTERY_1, 0)
                    await xp_ac.ACState.wait_until_parameter_condition(cls.APU_N1, lambda p: p > 15, timeout=60)
                    synoptic_overrides.set_override_value(cls.BATTERY_1, 2)
                    await xp_ac.ACState.wait_until_parameter_condition(cls.APU_N1, lambda p: p > 50, timeout=60)

            async def apu_amps():
                amps = [-1 * i for i in cls.APU_AMPS_SAMPLE]
                await synoptic_overrides._1d_table_anim(
                    cls.APU_AMPS, cls.TIME_SAMPLE, amps
                )

            async def bat_1_amps():
                amps = [-1 * i for i in cls.BAT_1_AMPS_SAMPLE]
                await synoptic_overrides._1d_table_anim(
                    cls.BAT_1_AMPS, cls.TIME_SAMPLE, amps
                )

            async def bat_2_amps():
                amps = [-1 * i for i in cls.BAT_2_AMPS_SAMPLE]
                await synoptic_overrides._1d_table_anim(
                    cls.BAT_2_AMPS, cls.TIME_SAMPLE, amps
                )
            
            await asyncio.gather(n1(), temp(), elec_tab(), bat1(), apu_amps(), bat_1_amps(), bat_2_amps())
            # await asyncio.sleep(30)


class EngineStatus(enum.IntEnum):
    STOPPED = 0
    RUNNING = 1


class EngineStart1(System):
    N1 = xp.Params["sim/cockpit2/engine/indicators/N1_percent[0]"]
    N2 = xp.Params["sim/cockpit2/engine/indicators/N2_percent[0]"]
    ITT = Params["sim/cockpit2/engine/indicators/ITT_deg_C[0]"] 
    IGN = xp.Params["sim/custom/7x/z_syn_eng_ign1"]
    OIL_PSI = Params["sim/cockpit2/engine/indicators/oil_pressure_psi[0]"] 
    OIL_TEMP = Params["sim/cockpit2/engine/indicators/oil_temperature_deg_C[0]"]
    FF = Params["sim/cockpit2/engine/indicators/fuel_flow_kg_sec[0]"]
    START = xp.Params["sim/custom/7x/z_syn_eng_start1"]
    AB = xp.Params["sim/custom/7x/z_syn_eng_ab1"]
    APU_N1 = xp.Params["sim/cockpit2/electrical/APU_N1_percent"]
    N1_MAX = xp.Params["sim/custom/xap/maxin1"]
    APU_TEMP = xp.Params["sim/cockpit2/electrical/APU_EGT_c"]
    MIN_OIL_LEVEL = xp.Params["sim/custom/7x/z_oil_min_height_1"]
    fuel_flow_switch = engine_panel.en_fuel_1
    fuel_digital = engine_panel.en_fuel_digital_1

    broken_start = False
    broken_start_finished = False
    cas_eng_shutdown_msg = cas.ENG_1_AUTO_SHUTDOWN

    TIME_SAMPLE = [0, 1, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 40, 43, 47, 50 ]
    N1_SAMPLE = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9.7, 11.4, 12.1, 13.7, 15.8, 16.7, 18.4, 19.5, 21, 21.8, 22.3, 23, 23.6, 23.9, 23.8, 24, 24.1, 24.2, 24.2] # time
    N2_SAMPLE = [0, 0, 3.6, 5.5, 9.2, 12.2, 14.3, 16.4, 17.7, 18.9, 19.5, 21.4, 22.8, 23.5, 24, 24.7, 27.8, 30.1, 30.8, 34.1, 34.8, 37.6, 39, 41.9, 44.5, 46.6, 49.1, 50.5, 50.1, 49.9, 50.3, 51.2, 51.6, 51.7, 51.7, 51.9, 52, 52, 52]
    FF_SAMPLE = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 75, 120, 120, 215, 215, 225, 225, 225, 240, 250, 265, 280, 300, 305, 310, 325, 340, 350, 350, 365, 355, 350, 350]
    ITT_SAMPLE = [13, 13, 13, 13, 13, 14, 14, 14, 14, 15, 15, 29, 35, 52, 60, 70, 115, 161, 174, 222, 232, 267, 283, 313, 338, 353, 371, 378, 378, 383, 394, 409, 418, 423, 422, 432, 439, 448, 453]
    #OIL_PSI_SAMPLE = [1, 2, 1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 7, 8, 11, 11, 11, 11, 22, 28, 28, 34, 34, 41, 44, 46, 50, 55, 60, 63, 67, 69, 71, 71, 71, 75, 77, 76, 76]

    # TIME_OIL_TEMP_SAMPLE = [0, 1, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 40, 43, 47, 50]
    # OIL_TEMP_SAMPLE = [18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 19]

    TIME_OIL_TEMP_SAMPLE = [0, 1, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 40, 43, 47, 50, 66, 71, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 118, 119, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 156, 157, 158, 160, 162, 164, 166, 172, 210, 218, 223]
    OIL_TEMP_SAMPLE = [18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 19, 21, 21, 22, 22, 22, 22, 22, 22, 23, 23, 23, 23, 23, 23, 24, 24, 24, 24, 24, 24, 24, 24, 25, 25, 25, 25, 25, 25, 26, 26, 26, 26, 26, 26, 26, 26, 27, 29, 27, 27, 28, 29, 29, 29, 29, 29, 29, 30, 30, 30, 30, 30, 30, 30, 31, 31, 31, 31, 31, 31, 32, 32, 32, 32, 32, 32, 32, 32, 33, 33, 33, 33, 33, 33, 33, 34, 34, 34, 34, 35, 39, 40, 40]
    OIL_PSI_SAMPLE = [1, 2, 1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 7, 8, 11, 11, 11, 11, 22, 28, 28, 34, 34, 41, 44, 46, 50, 55, 60, 63, 67, 69, 71, 71, 71, 75, 77, 76, 76, 72, 70, 70, 70, 70, 70, 70, 70, 69, 69, 69, 69, 69, 69, 68, 68, 68, 68, 68, 68, 67, 67, 67, 68, 68, 66, 68, 66, 66, 66, 67, 67, 66, 67, 66, 66, 66, 66, 65, 64, 63, 66, 63, 62, 62, 62, 62, 62, 62, 62, 62, 62, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 59, 59, 59, 57, 57, 57]

    APU_TEMP_TIME_SAMPLE = [0, 12, 13, 38]
    APU_TEMP_SAMPLE = [280, 500, 500, 280] # apu temp

    logic_task = None
    is_killing = False

    status = EngineStatus.RUNNING

    @classmethod
    def start_condition(cls):
        avail = [
            xp_ac.ACState.param_available(cls.N1),
            xp_ac.ACState.param_available(cls.N2),
            xp_ac.ACState.param_available(cls.APU_N1)
        ]
        if not all(avail):
            return False

        cond = [
            cls.fuel_flow_switch.get_state() == 1,
            cls.fuel_digital.get_state() == 1,
            xp_ac.ACState.get_curr_param(cls.N1) < 1,
            xp_ac.ACState.get_curr_param(cls.N2) < 5,
            overhead_engines.apu_master.get_state() == 1,
            xp_ac.ACState.get_curr_param(cls.APU_N1) > 90,
            engine_panel.en_start.get_state() == 1
        ]

        if xp_ac.ACState.get_curr_param(cls.N1) < 10:
            cls.broken_start_finished = False
            cls.status = EngineStatus.STOPPED
        elif cls.logic_task is None:
            cls.status = EngineStatus.RUNNING

        return all(cond)

    @classmethod
    def kill_condition(cls):
        cond = [
            cls.logic_task is not None,
            cls.fuel_flow_switch.get_state() == 0,
        ]

        return all(cond)

    @classmethod
    async def system_logic_task(cls):
        if cls.broken_start:
            await cls.run_broken_start()
        else:
            await cls.run_normal_start()

    @classmethod
    async def run_normal_start(cls):
        async with synoptic_overrides.override_params([cls.ITT, cls.N1, cls.N2, cls.FF, cls.OIL_PSI, cls.OIL_TEMP, cls.N1_MAX, cls.APU_TEMP]):
            # after engine start
            # start appears in 1 sec after engine start
            async def n1():
                await synoptic_overrides._1d_table_anim(
                    cls.N1, cls.TIME_SAMPLE, cls.N1_SAMPLE
                )
                cls.status = EngineStatus.RUNNING

            async def n1_max():
                synoptic_overrides.set_override_value(cls.N1_MAX, 88)

            async def ff():
                ff_sample = [0.00012589 * x for x in cls.FF_SAMPLE]
                await synoptic_overrides._1d_table_anim(
                    cls.FF, cls.TIME_SAMPLE, ff_sample
                )

            async def N2_anim():
                await synoptic_overrides._1d_table_anim(
                    cls.N2, cls.TIME_SAMPLE, cls.N2_SAMPLE
                )

            async def itt():
                await synoptic_overrides._1d_table_anim(
                    cls.ITT, cls.TIME_SAMPLE, cls.ITT_SAMPLE
                )

            async def oil_psi():
                await synoptic_overrides._1d_table_anim(
                    cls.OIL_PSI, cls.TIME_OIL_TEMP_SAMPLE, cls.OIL_PSI_SAMPLE
                )

            async def oil_temp():
                await synoptic_overrides._1d_table_anim(
                    cls.OIL_TEMP, cls.TIME_OIL_TEMP_SAMPLE, cls.OIL_TEMP_SAMPLE
                )
            
            async def ign():
                # show ign
                await asyncio.sleep(1)
                await xp_ac.ACState.wait_until_parameter_condition(cls.N2, lambda p: p > 16)
                await xp.set_param(cls.IGN, 1)
                # hide ign
                await xp_ac.ACState.wait_until_parameter_condition(cls.N2, lambda p: p > 35, timeout=60)
                await xp.set_param(cls.IGN, 0)
            
            async def start():
                # show start
                await xp.set_param(cls.MIN_OIL_LEVEL, 5)
                await asyncio.sleep(1)
                await xp.set_param(cls.START, 1)
                # hide start
                await xp_ac.ACState.wait_until_parameter_condition(cls.N2, lambda p: p > 51, timeout=60)
                await asyncio.sleep(1)
                await xp.set_param(cls.START, 0)
                await xp.set_param(cls.MIN_OIL_LEVEL, 24)
            
            async def ab():
                await xp_ac.ACState.wait_until_parameter_condition(cls.N2, lambda p: p > 40)
                await xp.set_param(cls.AB, 1)
                await asyncio.sleep(2)
                await xp.set_param(cls.AB, 0)

            async def apu_temp():
                await synoptic_overrides._1d_table_anim(
                    cls.APU_TEMP, cls.APU_TEMP_TIME_SAMPLE, cls.APU_TEMP_SAMPLE
                )
            
            await asyncio.gather(n1(), n1_max(), ff(), N2_anim(), oil_psi(), oil_temp(), itt(), start(), ign(), ab(), apu_temp())
            cls.broken_start_finished = True
            # await asyncio.sleep(30)

    TIME_BROKEN_N1_SAMPLE = [0, 1, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 56 ]
    N2_BROKEN_N1_SAMPLE = [0, 0, 3.6, 5.5, 9.2, 12.2, 14.3, 16.4, 17.7, 18.9, 19.5, 21.4, 22.8, 23.5, 24, 24.7, 27.8, 30.1, 30.8, 34.1, 34.8, 37.6, 39, 41.9, 44.5, 46.6, 49.1, 50.5, 50.1, 49.9, 50.3, 51.2, 51.5, 0]
    FF_BROKEN_N1_SAMPLE = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 75, 120, 120, 215, 215, 225, 225, 225, 240, 250, 265, 280, 300, 305, 310, 325, 330, 0]
    ITT_BROKEN_N1_SAMPLE = [13, 13, 13, 13, 13, 14, 14, 14, 14, 15, 15, 29, 35, 52, 60, 70, 115, 161, 174, 222, 232, 267, 283, 313, 338, 353, 371, 378, 378, 383, 394, 409, 410, 150]

    OIL_TEMP_BROKEN_N1_SAMPLE = [18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18]
    OIL_PSI_BROKEN_N1_SAMPLE = [1, 2, 1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 7, 8, 11, 11, 11, 11, 22, 28, 28, 34, 34, 41, 44, 46, 50, 55, 60, 63, 67, 68, 69, 2]

    @classmethod
    async def run_broken_start(cls):
        async with synoptic_overrides.override_params([cls.ITT, cls.N1, cls.N2, cls.FF, cls.OIL_PSI, cls.OIL_TEMP, cls.N1_MAX, cls.APU_TEMP]):
            # broken start
            async def n1():
                synoptic_overrides.set_override_value(cls.N1, 0)

            async def n1_max():
                synoptic_overrides.set_override_value(cls.N1_MAX, 88)

            async def ff():
                ff_sample = [0.00012589 * x for x in cls.FF_BROKEN_N1_SAMPLE]
                await synoptic_overrides._1d_table_anim(
                    cls.FF, cls.TIME_BROKEN_N1_SAMPLE, ff_sample
                )

            async def N2_anim():
                await synoptic_overrides._1d_table_anim(
                    cls.N2, cls.TIME_BROKEN_N1_SAMPLE, cls.N2_BROKEN_N1_SAMPLE
                )

            async def itt():
                await synoptic_overrides._1d_table_anim(
                    cls.ITT, cls.TIME_BROKEN_N1_SAMPLE, cls.ITT_BROKEN_N1_SAMPLE
                )

            async def oil_psi():
                await synoptic_overrides._1d_table_anim(
                    cls.OIL_PSI, cls.TIME_BROKEN_N1_SAMPLE, cls.OIL_PSI_BROKEN_N1_SAMPLE
                )

            async def oil_temp():
                await synoptic_overrides._1d_table_anim(
                    cls.OIL_TEMP, cls.TIME_BROKEN_N1_SAMPLE, cls.OIL_TEMP_BROKEN_N1_SAMPLE
                )
            
            async def ign():
                # show ign
                await asyncio.sleep(1)
                await xp_ac.ACState.wait_until_parameter_condition(cls.N2, lambda p: p > 16)
                await xp.set_param(cls.IGN, 1)
                # hide ign
                await xp_ac.ACState.wait_until_parameter_condition(cls.N2, lambda p: p > 35, timeout=60)
                await xp.set_param(cls.IGN, 0)
            
            async def start():
                # show start
                await xp.set_param(cls.MIN_OIL_LEVEL, 5)
                await asyncio.sleep(1)
                await xp.set_param(cls.START, 1)
                # hide start
                await xp_ac.ACState.wait_until_parameter_condition(cls.N2, lambda p: p > 51, timeout=60)
                await asyncio.sleep(1)
                await xp.set_param(cls.START, 0)
                await xp.set_param(cls.MIN_OIL_LEVEL, 24)
            
            async def ab():
                await xp_ac.ACState.wait_until_parameter_condition(cls.N2, lambda p: p > 40)
                await xp.set_param(cls.AB, 1)
                await asyncio.sleep(2)
                await xp.set_param(cls.AB, 0)

            async def auto_stop():
                await cls.fuel_digital.set_state(0)
                await xp_ac.ACState.wait_until_parameter_condition(cls.N2, lambda p: p > 50)
                await cas.show_message(cls.cas_eng_shutdown_msg)
                await warning.master_caution_lh.set_state(1)
                await warning.master_caution_rh.set_state(1)
            
            await asyncio.gather(auto_stop(), n1(), n1_max(), ff(), N2_anim(), oil_psi(), oil_temp(), itt(), start(), ign(), ab())
            await cls.fuel_digital.set_state(1)

    @classmethod
    async def killing_task(cls):
        await xp.set_param(cls.START, 0)
        await xp.set_param(cls.MIN_OIL_LEVEL, 5)
        await xp.set_param(cls.IGN, 0)
        await xp.set_param(cls.AB, 0)
        cls.status = EngineStatus.STOPPED


class EngineStart2(EngineStart1):
    N1 = xp.Params["sim/cockpit2/engine/indicators/N1_percent[1]"]
    N2 = xp.Params["sim/cockpit2/engine/indicators/N2_percent[1]"]
    ITT = Params["sim/cockpit2/engine/indicators/ITT_deg_C[1]"] 
    IGN = xp.Params["sim/custom/7x/z_syn_eng_ign2"]
    OIL_PSI = Params["sim/cockpit2/engine/indicators/oil_pressure_psi[1]"] 
    OIL_TEMP = Params["sim/cockpit2/engine/indicators/oil_temperature_deg_C[1]"]
    FF = Params["sim/cockpit2/engine/indicators/fuel_flow_kg_sec[1]"]
    START = xp.Params["sim/custom/7x/z_syn_eng_start2"]
    AB = xp.Params["sim/custom/7x/z_syn_eng_ab2"]
    APU_N1 = xp.Params["sim/cockpit2/electrical/APU_N1_percent"]
    MIN_OIL_LEVEL = xp.Params["sim/custom/7x/z_oil_min_height_2"]
    fuel_flow_switch = engine_panel.en_fuel_2
    fuel_digital = engine_panel.en_fuel_digital_2

    broken_start = False
    broken_start_finished = False
    cas_eng_shutdown_msg = cas.ENG_2_AUTO_SHUTDOWN

    # otherwise logic_task will be shared between all derived classes
    logic_task = None
    is_killing = False

    working_state = EngineStatus.RUNNING


class EngineStart3(EngineStart1):
    N1 = xp.Params["sim/cockpit2/engine/indicators/N1_percent[2]"]
    N2 = xp.Params["sim/cockpit2/engine/indicators/N2_percent[2]"]
    ITT = Params["sim/cockpit2/engine/indicators/ITT_deg_C[2]"] 
    IGN = xp.Params["sim/custom/7x/z_syn_eng_ign3"]
    OIL_PSI = Params["sim/cockpit2/engine/indicators/oil_pressure_psi[2]"] 
    OIL_TEMP = Params["sim/cockpit2/engine/indicators/oil_temperature_deg_C[2]"]
    FF = Params["sim/cockpit2/engine/indicators/fuel_flow_kg_sec[2]"]
    START = xp.Params["sim/custom/7x/z_syn_eng_start3"]
    AB = xp.Params["sim/custom/7x/z_syn_eng_ab3"]
    APU_N1 = xp.Params["sim/cockpit2/electrical/APU_N1_percent"]
    MIN_OIL_LEVEL = xp.Params["sim/custom/7x/z_oil_min_height_3"]
    fuel_flow_switch = engine_panel.en_fuel_3
    fuel_digital = engine_panel.en_fuel_digital_3

    broken_start = False
    broken_start_finished = False
    cas_eng_shutdown_msg = cas.ENG_3_AUTO_SHUTDOWN

    # otherwise logic_task will be shared between all derived classes
    logic_task = None
    is_killing = False

    working_state = EngineStatus.RUNNING


class Engine1CustomSpecs(System):
    ENGINE = EngineStart1

    TRHOTTLE_RATIO = xp.Params["sim/cockpit2/engine/actuators/throttle_ratio[0]"]
    N1 = xp.Params["sim/cockpit2/engine/indicators/N1_percent[0]"]

    THROTTLE_N1_MAP_ARGS = [0, 5, 15, 25, 35, 40]
    THROTTLE_N1_MAP_VALUES = [22, 28, 30, 48, 83, 90]

    N1_PID = simple_pid.PID(Kp=4.6, Ki=0.7, Kd=0)
    N1_PID_OUTPUT = 0

    fuel_flow_switch = engine_panel.en_fuel_1
    fuel_flow_digital = engine_panel.en_fuel_digital_1
    next_wake_sleep_delay = 0.05
    active = False

    @classmethod
    def start_condition(cls):
        avail = [
            xp_ac.ACState.param_available(cls.TRHOTTLE_RATIO),
            xp_ac.ACState.param_available(cls.N1),
        ]

        if not all(avail):
            return False

        enable = [
            cls.ENGINE.status == EngineStatus.RUNNING,
            cls.fuel_flow_switch.get_state() == 1,
            cls.fuel_flow_digital.get_state() == 1

        ]
        enable = all(enable)

        if enable and not cls.active:
            sane_tasks.spawn(synoptic_overrides.enable_param_overrides([cls.N1]))
            cls.active = True
        
        if not enable and cls.active:
            sane_tasks.spawn(synoptic_overrides.disable_param_overrides([cls.N1]))
            cls.active = False

        return enable

    @classmethod
    async def system_logic_task(cls):
        throttle_ratio = xp_ac.ACState.get_curr_param(cls.TRHOTTLE_RATIO)

        throttle_real = util.linear_map(throttle_ratio, 0, 1, 0, 40)

        n1_ref_val = np.interp(throttle_real, cls.THROTTLE_N1_MAP_ARGS, cls.THROTTLE_N1_MAP_VALUES)

        cls.N1_PID.setpoint = n1_ref_val
        dt = cls.next_wake_sleep_delay
        y1 = cls.N1_PID(cls.N1_PID_OUTPUT, dt)

        cls.N1_PID_OUTPUT += y1 * dt 

        synoptic_overrides.set_override_value(cls.N1, cls.N1_PID_OUTPUT)
