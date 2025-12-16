import asyncio

import enum

import common.xp_aircraft_state as xp_ac
import xplane.master as xp
import common.sane_tasks as sane_tasks
import overhead_panel.dc_supply as dc
import overhead_panel.engines_apu as eng_apu
import overhead_panel.hydraulics as hyd

from aircraft_systems.system_base import System
import aircraft_systems.engine as engine_sys
import xplane.master as xp
import aircraft_systems.elec as elec_sys


class HydAllValves(System):
    next_wake_sleep_delay = 0.5

    PUMP_A1 = xp.Params["sim/custom/7x/z_hyd_pump_a1"]
    PUMP_A1 = xp.Params["sim/custom/7x/z_hyd_pump_a3"]
    PUMP_BU = xp.Params["sim/custom/7x/z_hyd_pump_bu"]
    PUMP_B2 = xp.Params["sim/custom/7x/z_hyd_pump_b2"]
    PUMP_B3 = xp.Params["sim/custom/7x/z_hyd_pump_b3"]
    PUMP_C2 = xp.Params["sim/custom/7x/z_hyd_pump_c2"]

    PUMP_A1_TEXT = xp.Params["sim/custom/7x/z_hyd_pump_a1_text"]
    PUMP_A3_TEXT = xp.Params["sim/custom/7x/z_hyd_pump_a3_text"]
    PUMP_BU_TEXT = xp.Params["sim/custom/7x/z_hyd_pump_bu_text"]
    PUMP_B2_TEXT = xp.Params["sim/custom/7x/z_hyd_pump_b2_text"]
    PUMP_B3_TEXT = xp.Params["sim/custom/7x/z_hyd_pump_b3_text"]
    PUMP_C2_TEXT = xp.Params["sim/custom/7x/z_hyd_pump_c2_text"]

    PIPE_A1 = xp.Params["sim/custom/7x/z_hyd_pipe_a1"]
    PIPE_A3 = xp.Params["sim/custom/7x/z_hyd_pipe_a3"]
    PIPE_A1A3 = xp.Params["sim/custom/7x/z_hyd_pipe_a1a3"]
    PIPE_B2 = xp.Params["sim/custom/7x/z_hyd_pipe_b2"]
    PIPE_B3 = xp.Params["sim/custom/7x/z_hyd_pipe_b3"]
    PIPE_B2B3 = xp.Params["sim/custom/7x/z_hyd_pipe_b2b3"]
    PIPE_C2 = xp.Params["sim/custom/7x/z_hyd_pipe_c2"]
    PIPE_EBHA = xp.Params["sim/custom/7x/z_hyd_pipe_ebha"]
    PIPE_BRAKE2 = xp.Params["sim/custom/7x/z_hyd_pipe_brake2"]
    PIPE_BU = xp.Params["sim/custom/7x/z_hyd_pipe_bu"]

    old_state = []

    @classmethod
    def start_condition(cls):
        return True

    @classmethod
    async def system_logic_task(cls):
        shutoff_a1_state = 0
        if hyd.shutoff_a1.get_state() == 0:
            shutoff_a1_state = 1
        
        shutoff_a3_state = 0
        if hyd.shutoff_a3.get_state() == 0:
            shutoff_a3_state = 1

        shutoff_b2_state = 0
        if hyd.shutoff_b2.get_state() == 0:
            shutoff_b2_state = 1

        shutoff_b3_state = 0
        if hyd.shutoff_b3.get_state() == 0:
            shutoff_b3_state = 1

        shutoff_c2_state = 0
        if hyd.shutoff_c2.get_state() == 0:
            shutoff_c2_state = 1

        bu_state_text = 0
        match hyd.backup_pump.get_state():
            case 0:
                bu_state_text = 1
            case 1:
                bu_state_text = 2
            case 2:
                bu_state_text = 0
        
        new_state = [
            shutoff_a1_state,
            shutoff_a3_state,
            shutoff_b2_state,
            shutoff_b3_state,
            shutoff_c2_state,
            bu_state_text,
        ]

        if new_state != cls.old_state:
            cls.old_state = new_state
        
            await xp.set_param(cls.PUMP_A1_TEXT, int(shutoff_a1_state))
            await xp.set_param(cls.PUMP_A3_TEXT, int(shutoff_a3_state))
            await xp.set_param(cls.PUMP_B2_TEXT, int(shutoff_b2_state))
            await xp.set_param(cls.PUMP_B3_TEXT, int(shutoff_b3_state))
            await xp.set_param(cls.PUMP_C2_TEXT, int(shutoff_c2_state))
            await xp.set_param(cls.PUMP_BU_TEXT, int(bu_state_text))
