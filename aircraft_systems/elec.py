import asyncio

import enum

import common.xp_aircraft_state as xp_ac
import xplane.master as xp
import common.sane_tasks as sane_tasks
import overhead_panel.dc_supply as dc
import overhead_panel.engines_apu as eng_apu
import overhead_panel.fuel as fuel_overhead

from aircraft_systems.system_base import System


class PowerStatus(enum.IntEnum):
    NO_POWER = 0
    POWER_ON = 1


class Gen1(System):
    WORKING_THRESHOLD_N1 = 51.9
    N1 = xp.Params["sim/cockpit2/engine/indicators/N1_percent[0]"]

    power_state = PowerStatus.POWER_ON
    gen_switch = dc.gen1

    fail = False

    @classmethod
    def start_condition(cls):
        eng_n1 = xp_ac.ACState.get_curr_param(cls.N1) or 0
        if cls.gen_switch.get_state() == 1 and eng_n1 >= cls.WORKING_THRESHOLD_N1 and cls.fail == False:
            cls.power_state = PowerStatus.POWER_ON
        else:
            cls.power_state = PowerStatus.NO_POWER

        return False

    @classmethod
    async def system_logic_task(cls):
        pass


class Gen2(Gen1):
    N1 = xp.Params["sim/cockpit2/engine/indicators/N1_percent[1]"]

    power_state = PowerStatus.POWER_ON
    gen_switch = dc.gen2
    fail = False


class Gen3(Gen1):
    N1 = xp.Params["sim/cockpit2/engine/indicators/N1_percent[2]"]

    power_state = PowerStatus.POWER_ON
    gen_switch = dc.gen3
    fail = False


class Apu(System):
    state = PowerStatus.POWER_ON

    @classmethod
    def start_condition(cls):
        apu_n1 = xp_ac.ACState.get_curr_param(xp.Params["sim/cockpit2/electrical/APU_N1_percent"]) or 0
        if eng_apu.apu_master.get_state() == 1 and apu_n1 > 50:
            cls.state = PowerStatus.POWER_ON
        else:
            cls.state = PowerStatus.NO_POWER

        return False

    @classmethod
    async def system_logic_task(cls):
        pass


class ElecLinePower(System):
    @classmethod
    def start_condition(cls):
        # run every time
        return True

    @classmethod
    async def system_logic_task(cls):
        line_gen2_on = False

        if Gen2.power_state == PowerStatus.POWER_ON:
            line_gen2_on |= True

        line_bat2_ratgen_on = False
        if dc.bat2.get_state() == 1: # or dc.rat_get.get_state() == 1
            line_bat2_ratgen_on |= True

        line_apu_bat1_on = False
        if dc.bat1.get_state() == 1 or Apu.state == PowerStatus.POWER_ON:
            line_apu_bat1_on |= True
        
        line_gen1_gen3_on = False
        if Gen1.power_state == PowerStatus.POWER_ON or Gen3.power_state == PowerStatus.POWER_ON:
            line_gen1_gen3_on |= True
        
        if dc.rh_isol.get_state() == 0:
            line_gen2_on |= line_bat2_ratgen_on
            line_bat2_ratgen_on |= line_gen2_on

        if dc.bus_tie.get_state() == 1:
            line_bat2_ratgen_on |= line_apu_bat1_on 
            line_apu_bat1_on |= line_bat2_ratgen_on
        
        if dc.lh_isol.get_state() == 0:
            line_apu_bat1_on |= line_gen1_gen3_on
            line_gen1_gen3_on |= line_apu_bat1_on
        
        await xp.set_param(xp.Params["sim/custom/7x/z_line_gen2_on"], int(line_gen2_on))
        await xp.set_param(xp.Params["sim/custom/7x/z_line_bat2_ratgen_on"], int(line_bat2_ratgen_on))
        await xp.set_param(xp.Params["sim/custom/7x/z_line_apu_bat1_on"], int(line_apu_bat1_on))
        await xp.set_param(xp.Params["sim/custom/7x/z_line_gen1_gen3_on"], int(line_gen1_gen3_on))
