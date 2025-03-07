import asyncio

import enum

import common.xp_aircraft_state as xp_ac
import xplane.master as xp
import common.sane_tasks as sane_tasks
import overhead_panel.dc_supply as dc
import overhead_panel.engines_apu as eng_apu

from aircraft_systems.system_base import System


class GenStatus(enum.IntEnum):
    NOT_WORKING = 0
    WORKING = 1


class Gen1(System):
    state = GenStatus.WORKING

    @classmethod
    def start_condition(cls):
        # run every time
        return True

    @classmethod
    async def system_logic_task(cls):
        eng1_n1 = xp_ac.ACState.get_curr_param(xp.Params["sim/cockpit2/engine/indicators/N1_percent[0]"]) or 0
        if dc.gen1.get_state() == 1 and eng1_n1 > 10:
            cls.state = GenStatus.WORKING
        else:
            cls.state = GenStatus.NOT_WORKING


class Gen2(System):
    state = GenStatus.WORKING

    @classmethod
    def start_condition(cls):
        # run every time
        return True

    @classmethod
    async def system_logic_task(cls):
        eng2_n1 = xp_ac.ACState.get_curr_param(xp.Params["sim/cockpit2/engine/indicators/N1_percent[1]"]) or 0
        if dc.gen2.get_state() == 1 and eng2_n1 > 10:
            cls.state = GenStatus.WORKING
        else:
            cls.state = GenStatus.NOT_WORKING


class Gen3(System):
    state = GenStatus.WORKING

    @classmethod
    def start_condition(cls):
        # run every time
        return True

    @classmethod
    async def system_logic_task(cls):
        eng3_n1 = xp_ac.ACState.get_curr_param(xp.Params["sim/cockpit2/engine/indicators/N1_percent[2]"]) or 0
        if dc.gen3.get_state() == 1 and eng3_n1 > 10:
            cls.state = GenStatus.WORKING
        else:
            cls.state = GenStatus.NOT_WORKING


class Apu(System):
    state = GenStatus.WORKING

    @classmethod
    def start_condition(cls):
        # run every time
        return True

    @classmethod
    async def system_logic_task(cls):
        apu_n1 = xp_ac.ACState.get_curr_param(xp.Params["sim/cockpit2/electrical/APU_N1_percent"]) or 0
        if eng_apu.apu_master.get_state() == 1 and apu_n1 > 50:
            cls.state = GenStatus.WORKING
        else:
            cls.state = GenStatus.NOT_WORKING


class ElecLinePower(System):
    @classmethod
    def start_condition(cls):
        # run every time
        return True

    @classmethod
    async def system_logic_task(cls):
        line_gen2_on = False

        if Gen2.state == GenStatus.WORKING:
            line_gen2_on |= True

        line_bat2_ratgen_on = False
        if dc.bat2.get_state() == 1: # or dc.rat_get.get_state() == 1
            line_bat2_ratgen_on |= True

        line_apu_bat1_on = False
        if dc.bat1.get_state() == 1 or Apu.state == GenStatus.WORKING:
            line_apu_bat1_on |= True
        
        line_gen1_gen3_on = False
        if Gen1.state == GenStatus.WORKING or Gen3.state == GenStatus.WORKING:
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
        