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

from common.util import LineColor


class HydAllValves(System):
    next_wake_sleep_delay = 1

    PUMP_A1 = xp.Params["sim/custom/7x/z_hyd_pump_a1"]
    PUMP_A3 = xp.Params["sim/custom/7x/z_hyd_pump_a3"]
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

    N2_ENG1 = xp.Params["sim/cockpit2/engine/indicators/N2_percent[0]"]
    N2_ENG2 = xp.Params["sim/cockpit2/engine/indicators/N2_percent[1]"]
    N2_ENG3 = xp.Params["sim/cockpit2/engine/indicators/N2_percent[2]"]

    OM_SLATS_TEXT = xp.Params["sim/custom/7x/z_hyd_text_om_slats"]
    RH_AIL_TEXT = xp.Params["sim/custom/7x/z_hyd_text_rh_ail"]
    RH_ELEV_TEXT = xp.Params["sim/custom/7x/z_hyd_text_rh_elev"]
    SPOILERS_TEXT = xp.Params["sim/custom/7x/z_hyd_text_spoilers"]

    ENG_WORKING_THRESHOLD_N2 = 45

    BU_PUMP_XP = xp.Params["sim/cockpit2/switches/electric_hydraulic_pump_on"]

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

        pump_a1_state = 0
        if (xp_ac.ACState.get_curr_param(cls.N2_ENG1) or 0) > cls.ENG_WORKING_THRESHOLD_N2: 
            pump_a1_state = 1

        pump_a3_state = 0
        if (xp_ac.ACState.get_curr_param(cls.N2_ENG3) or 0) > cls.ENG_WORKING_THRESHOLD_N2: 
            pump_a3_state = 1

        pump_b2_state = 0
        if (xp_ac.ACState.get_curr_param(cls.N2_ENG2) or 0) > cls.ENG_WORKING_THRESHOLD_N2:
            pump_b2_state = 1

        pump_b3_state = 0
        if (xp_ac.ACState.get_curr_param(cls.N2_ENG3) or 0) > cls.ENG_WORKING_THRESHOLD_N2: 
            pump_b3_state = 1

        pump_c2_state = 0
        if (xp_ac.ACState.get_curr_param(cls.N2_ENG2) or 0) > 14: 
            pump_c2_state = 1

        pump_bu_state = 0
        if (xp_ac.ACState.get_curr_param(cls.BU_PUMP_XP) or 0) == 1: 
            pump_bu_state = 1
        
        pipe_a1_state = LineColor.BLACK
        if pump_a1_state == 1:
            pipe_a1_state = LineColor.YELLOW

            if shutoff_a1_state == 1:
                pipe_a1_state = LineColor.GREEN

        pipe_a3_state = LineColor.BLACK
        if pump_a3_state == 1:
                pipe_a3_state = LineColor.YELLOW

                if shutoff_a3_state == 1:
                    pipe_a3_state = LineColor.GREEN
        
        pipe_a1a3_state = LineColor.BLACK
        pipe_a1a3_state = pipe_a1_state + pipe_a3_state

        pipe_b2_state = LineColor.BLACK
        if pump_b2_state == 1:
            pipe_b2_state = LineColor.YELLOW

            if shutoff_b2_state == 1:
                pipe_b2_state = LineColor.GREEN
        
        pipe_b3_state = LineColor.BLACK
        if pump_b3_state == 1:
            pipe_b3_state = LineColor.YELLOW

            if shutoff_b3_state == 1:
                pipe_b3_state = LineColor.GREEN
        
        pipe_bu_state = LineColor.BLACK
        if pump_bu_state == 1:
            pipe_bu_state = LineColor.GREEN
        
        pipe_b2b3_state = LineColor.BLACK
        pipe_b2b3_state = pipe_bu_state + pipe_b2_state + pipe_b3_state
    
        pipe_c2_state = LineColor.BLACK
        if pump_c2_state == 1:
            pipe_c2_state = LineColor.YELLOW
            
            if shutoff_c2_state == 1:
                pipe_c2_state = LineColor.GREEN
        
        hyd_accum_state = LineColor.GREEN
        pipe_brake2 = LineColor.BLACK
        pipe_brake2 = hyd_accum_state + pipe_b2b3_state

        om_slats_text_state = LineColor.BLACK
        om_slats_text_state = pipe_a1a3_state + pipe_b2b3_state

        rh_ail_text_state = LineColor.BLACK
        rh_ail_text_state = pipe_b2b3_state + pipe_c2_state

        rh_elev_text_state = LineColor.BLACK
        rh_elev_text_state = pipe_a1a3_state + pipe_c2_state

        ebha_pump_state = LineColor.BLACK
        spoilers_text_state = LineColor.BLACK
        spoilers_text_state = ebha_pump_state + pipe_c2_state

        new_state = [
            shutoff_a1_state,
            shutoff_a3_state,
            shutoff_b2_state,
            shutoff_b3_state,
            shutoff_c2_state,
            bu_state_text,
            pump_a1_state,
            pump_a3_state,
            pump_b2_state,
            pump_b3_state,
            pump_c2_state,
            pump_bu_state,
            pipe_a1_state,
            pipe_a3_state,
            pipe_a1a3_state,
            pipe_b2_state,
            pipe_b3_state,
            pipe_bu_state,
            pipe_b2b3_state,
            pipe_c2_state,
            pipe_brake2,
            om_slats_text_state,
            rh_ail_text_state,
            rh_elev_text_state,
            spoilers_text_state
        ]

        if new_state != cls.old_state:
            cls.old_state = new_state
        
            await xp.set_param(cls.PUMP_A1_TEXT, int(shutoff_a1_state))
            await xp.set_param(cls.PUMP_A3_TEXT, int(shutoff_a3_state))
            await xp.set_param(cls.PUMP_B2_TEXT, int(shutoff_b2_state))
            await xp.set_param(cls.PUMP_B3_TEXT, int(shutoff_b3_state))
            await xp.set_param(cls.PUMP_C2_TEXT, int(shutoff_c2_state))
            await xp.set_param(cls.PUMP_BU_TEXT, int(bu_state_text))

            await xp.set_param(cls.PUMP_A1, int(pump_a1_state))
            await xp.set_param(cls.PUMP_A3, int(pump_a3_state))
            await xp.set_param(cls.PUMP_B2, int(pump_b2_state))
            await xp.set_param(cls.PUMP_B3, int(pump_b3_state))
            await xp.set_param(cls.PUMP_C2, int(pump_c2_state))
            await xp.set_param(cls.PUMP_BU, int(pump_bu_state))

            await xp.set_param(cls.PIPE_A1, int(pipe_a1_state))
            await xp.set_param(cls.PIPE_A3, int(pipe_a3_state))
            await xp.set_param(cls.PIPE_A1A3, int(pipe_a1a3_state))
            await xp.set_param(cls.PIPE_B2, int(pipe_b2_state))
            await xp.set_param(cls.PIPE_B3, int(pipe_b3_state))
            await xp.set_param(cls.PIPE_BU, int(pipe_bu_state))
            await xp.set_param(cls.PIPE_B2B3, int(pipe_b2b3_state))
            await xp.set_param(cls.PIPE_C2, int(pipe_c2_state))
            await xp.set_param(cls.PIPE_BRAKE2, int(pipe_brake2))

            await xp.set_param(cls.OM_SLATS_TEXT, int(om_slats_text_state))
            await xp.set_param(cls.RH_AIL_TEXT, int(rh_ail_text_state))
            await xp.set_param(cls.RH_ELEV_TEXT, int(rh_elev_text_state))
            await xp.set_param(cls.SPOILERS_TEXT, int(spoilers_text_state))
