import asyncio

import common.xp_aircraft_state as xp_ac
import xplane.master as xp
import common.sane_tasks as sane_tasks
import overhead_panel.fire_panel as fp 

from aircraft_systems.system_base import System
from xplane.params import Params
import middle_pedestal.engine as engine_panel
import overhead_panel.engines_apu as overhead_engines
import synoptic_remote.param_overrides as synoptic_overrides


class EngineStart1(System):
    N2 = xp.Params["sim/cockpit2/engine/indicators/N2_percent[0]"]
    ITT = Params["sim/cockpit2/engine/indicators/ITT_deg_C[0]"] 
    IGN = xp.Params["sim/custom/7x/z_syn_eng_ign1"]
    OIL = Params["sim/cockpit2/engine/indicators/oil_pressure_psi[0]"] 
    FUEL = Params["sim/cockpit2/engine/indicators/fuel_flow_kg_sec[0]"]
    START = xp.Params["sim/custom/7x/z_syn_eng_start1"]
    AB = xp.Params["sim/custom/7x/z_syn_eng_ab1"]
    APU_N1 = xp.Params["sim/cockpit2/electrical/APU_N1_percent"]
    fuel_flow_switch = engine_panel.en_fuel_1

    logic_task = None

    @classmethod
    def start_condition(cls):
        avail = [
            xp_ac.ACState.param_available(cls.N2),
            xp_ac.ACState.param_available(cls.APU_N1)
        ]
        if not all(avail):
            return False

        cond = [
            cls.fuel_flow_switch.get_state() == 1,
            xp_ac.ACState.get_curr_param(cls.N2) < 5,
            overhead_engines.apu_master.get_state() == 1,
            xp_ac.ACState.get_curr_param(cls.APU_N1) > 90,
            engine_panel.en_start.get_state() == 1
        ]

        return all(cond)

    @classmethod
    async def system_logic_task(cls):
        async with synoptic_overrides.override_params([cls.ITT, cls.N2, cls.FUEL, cls.OIL]):
            # after engine start
            # start appears in 1 sec after engine start
            async def ff():
                await synoptic_overrides._1d_table_anim(
                    cls.FUEL,
                    [0, 20, 36], # time
                    [0, 0.001, 0.0377386] # 
                )

            async def N2_anim():
                await synoptic_overrides._1d_table_anim(
                    cls.N2,
                    [0, 1, 8, 32], # time
                    [1, 1, 2, 52] # N2
                )

                await synoptic_overrides.disable_param_overrides([cls.N2])

            async def itt():
                await xp_ac.ACState.wait_until_parameter_condition(cls.IGN, lambda p: p == 1)
                itt_curr = xp_ac.ACState.get_curr_param(cls.ITT)
                await synoptic_overrides._1d_table_anim(
                    cls.ITT,
                    [0, 10], # time
                    [itt_curr, 700] # itt
                )

                await synoptic_overrides.disable_param_overrides([cls.ITT])

            async def oil():
                curr_oil = xp_ac.ACState.get_curr_param(cls.OIL)
                if curr_oil > 69:
                    synoptic_overrides.disable_param_overrides([cls.OIL])
                    return

                await synoptic_overrides._1d_table_anim(
                    cls.OIL,
                    [0, 19, 35], # time
                    [curr_oil, curr_oil + 5, 69] # 
                )
            
            async def ign():
                # show ign
                await asyncio.sleep(1)
                await xp_ac.ACState.wait_until_parameter_condition(cls.N2, lambda p: p > 16)
                await xp.set_param(cls.IGN, 1)
                # hide ign
                await xp_ac.ACState.wait_until_parameter_condition(cls.N2, lambda p: p > 51, timeout=20)
                await xp.set_param(cls.IGN, 0)
            
            async def start():
                # show start
                await asyncio.sleep(1)
                await xp.set_param(cls.START, 1)
                # hide start
                await xp_ac.ACState.wait_until_parameter_condition(cls.N2, lambda p: p > 51, timeout=30)
                await xp.set_param(cls.START, 0)
            
            async def ab():
                await xp_ac.ACState.wait_until_parameter_condition(cls.N2, lambda p: p > 40)
                await xp.set_param(cls.AB, 1)
                await asyncio.sleep(2)
                await xp.set_param(cls.AB, 0)
            
            await asyncio.gather(ff(), N2_anim(), oil(), itt(), start(), ign(), ab())


class EngineStart2(EngineStart1):
    N2 = xp.Params["sim/cockpit2/engine/indicators/N2_percent[1]"]
    ITT = Params["sim/cockpit2/engine/indicators/ITT_deg_C[1]"] 
    IGN = xp.Params["sim/custom/7x/z_syn_eng_ign2"]
    OIL = Params["sim/cockpit2/engine/indicators/oil_pressure_psi[1]"] 
    FUEL = Params["sim/cockpit2/engine/indicators/fuel_flow_kg_sec[1]"]
    START = xp.Params["sim/custom/7x/z_syn_eng_start2"]
    AB = xp.Params["sim/custom/7x/z_syn_eng_ab2"]
    APU_N1 = xp.Params["sim/cockpit2/electrical/APU_N1_percent"]
    fuel_flow_switch = engine_panel.en_fuel_2

    logic_task = None


class EngineStart3(EngineStart1):
    N2 = xp.Params["sim/cockpit2/engine/indicators/N2_percent[2]"]
    ITT = Params["sim/cockpit2/engine/indicators/ITT_deg_C[2]"] 
    IGN = xp.Params["sim/custom/7x/z_syn_eng_ign3"]
    OIL = Params["sim/cockpit2/engine/indicators/oil_pressure_psi[2]"] 
    FUEL = Params["sim/cockpit2/engine/indicators/fuel_flow_kg_sec[2]"]
    START = xp.Params["sim/custom/7x/z_syn_eng_start3"]
    AB = xp.Params["sim/custom/7x/z_syn_eng_ab3"]
    APU_N1 = xp.Params["sim/cockpit2/electrical/APU_N1_percent"]
    fuel_flow_switch = engine_panel.en_fuel_3

    logic_task = None
