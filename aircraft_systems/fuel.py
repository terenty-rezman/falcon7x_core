import asyncio

import enum

import common.xp_aircraft_state as xp_ac
import xplane.master as xp
import common.sane_tasks as sane_tasks
import overhead_panel.dc_supply as dc
import overhead_panel.engines_apu as eng_apu
import overhead_panel.fuel as fuel_overhead

from aircraft_systems.system_base import System
import aircraft_systems.engine as engine_sys
import xplane.master as xp
import aircraft_systems.elec as elec_sys


class BoostStatus(enum.IntEnum):
    UNDEFINED = -1
    BATTERY_OFF = 0
    OFF = 1
    STBY = 2
    POWER_ON = 3


class BoostStart2(System):
    power_status = BoostStatus.UNDEFINED

    @classmethod
    def start_condition(cls):
        if cls.power_status == BoostStatus.UNDEFINED:
            if fuel_overhead.boost2.get_state() == 0:
                cls.power_status = BoostStatus.POWER_ON
            elif fuel_overhead.boost2.get_state() == 1:
                cls.power_status = BoostStatus.OFF
            elif fuel_overhead.boost2.get_state() == 2:
                cls.power_status = BoostStatus.STBY

        if dc.bat1.get_state() == 0:
            cls.power_status = BoostStatus.BATTERY_OFF

        return True

    @classmethod
    async def system_logic_task(cls):
        match cls.power_status:
            case BoostStatus.BATTERY_OFF:
                if dc.bat1.get_state() == 1:
                    cls.power_status = BoostStatus.OFF
                    await fuel_overhead.boost2.set_state(1)
            case BoostStatus.OFF:
                if eng_apu.apu_master.get_state() == 1:
                    cls.power_status = BoostStatus.STBY
                    await fuel_overhead.boost2.set_state(2)
            case BoostStatus.STBY:
                if engine_sys.EngineStart2.status == engine_sys.EngineStatus.RUNNING:
                    cls.power_status = BoostStatus.POWER_ON
                    await fuel_overhead.boost2.set_state(0)


class FuelAllValves(System):
    next_wake_sleep_delay = 0.5

    VALVE_XTK_13 = xp.Params["sim/custom/7x/z_fuel_xtk_13"]
    VALVE_XTK_23 = xp.Params["sim/custom/7x/z_fuel_xtk_23"]
    VALVE_XTK_12 = xp.Params["sim/custom/7x/z_fuel_xtk_12"]
    VALVE_XBP_12 = xp.Params["sim/custom/7x/z_fuel_xbp_12"]
    VALVE_XBP_13 = xp.Params["sim/custom/7x/z_fuel_xbp_13"]
    VALVE_XBP_23 = xp.Params["sim/custom/7x/z_fuel_xbp_23"]

    PIPE_t1t3 = xp.Params["sim/custom/7x/z_fuel_pipe_t1t3"]
    PIPE_t1t2 = xp.Params["sim/custom/7x/z_fuel_pipe_t1t2"]
    PIPE_t2t3 = xp.Params["sim/custom/7x/z_fuel_pipe_t2t3"]
    PIPE_t2apu = xp.Params["sim/custom/7x/z_fuel_pipe_t2apu"]
    PIPE_xbp12 = xp.Params["sim/custom/7x/z_fuel_pipe_xbp12"]
    PIPE_xbp23 = xp.Params["sim/custom/7x/z_fuel_pipe_xbp23"]
    PIPE_xbp13 = xp.Params["sim/custom/7x/z_fuel_pipe_xbp13"]
    PIPE_t1e1 = xp.Params["sim/custom/7x/z_fuel_pipe_t1e1"]
    PIPE_t2e2 = xp.Params["sim/custom/7x/z_fuel_pipe_t2e2"]
    PIPE_t3e3 = xp.Params["sim/custom/7x/z_fuel_pipe_t3e3"]

    BOOST1 = xp.Params["sim/custom/7x/z_fuel_boost1"]
    BOOST2 = xp.Params["sim/custom/7x/z_fuel_boost2"]
    BOOST3 = xp.Params["sim/custom/7x/z_fuel_boost3"]

    ENG1 = xp.Params["sim/custom/7x/z_fuel_eng1"]
    ENG2 = xp.Params["sim/custom/7x/z_fuel_eng2"]
    ENG3 = xp.Params["sim/custom/7x/z_fuel_eng3"]
    APU = xp.Params["sim/custom/7x/z_fuel_apu"]

    N2_ENG1 = xp.Params["sim/cockpit2/engine/indicators/N2_percent[0]"]
    N2_ENG2 = xp.Params["sim/cockpit2/engine/indicators/N2_percent[1]"]
    N2_ENG3 = xp.Params["sim/cockpit2/engine/indicators/N2_percent[2]"]
    ENG_WORKING_THRESHOLD_N2 = 49

    old_state = []

    @classmethod
    def start_condition(cls):
        return True

    @classmethod
    async def system_logic_task(cls):
        xtk_13_state = 0 
        if fuel_overhead.xtk_right.get_state():
            xtk_13_state = 1

        if fuel_overhead.xtk_left.get_state():
            xtk_13_state = 2
        
        xtk_12_state = 0
        if fuel_overhead.xtk_down_1.get_state():
            xtk_12_state = 1
        
        if fuel_overhead.xtk_up_1.get_state():
            xtk_12_state = 2

        xtk_23_state = 0
        if fuel_overhead.xtk_down_2.get_state():
            xtk_23_state = 2
        
        if fuel_overhead.xtk_up_2.get_state():
            xtk_23_state = 1
        
        pipe_t1t3_state = 0
        if xtk_13_state:
            pipe_t1t3_state = 1

        pipe_t1t2_state = 0
        if xtk_12_state:
            pipe_t1t2_state = 1
        
        pipe_t2t3_state = 0
        if xtk_23_state:
            pipe_t2t3_state = 1
        
        xbp_13_state = 0
        if fuel_overhead.xbp_13.get_state():
            xbp_13_state = 1
        
        pipe_xbp13_state = 0
        if xbp_13_state:
            pipe_xbp13_state = 1

        xbp_12_state = 0
        if fuel_overhead.xbp_12.get_state():
            xbp_12_state = 1

        pipe_xbp12_state = 0
        if xbp_12_state:
            pipe_xbp12_state = 1

        xbp_23_state = 0
        if fuel_overhead.xbp_23.get_state():
            xbp_23_state = 1

        pipe_xbp23_state = 0
        if xbp_23_state:
            pipe_xbp23_state = 1

        pipe_xbp23_state = 0
        if xbp_23_state:
            pipe_xbp23_state = 1

        # BOOST 1
        boost1_state = 0
        boost1_xp_state = fuel_overhead.boost1.get_state()
        match boost1_xp_state:
            case 0:
                boost1_state = 1 # on
            case 1:
                boost1_state = 0 # off
            case 2:
                boost1_state = 2 # stby
        
        if xtk_12_state == 1 or xtk_13_state == 1 and fuel_overhead.backup_13.get_state() == 0:
            boost1_state = 3 # both
        
        pipe_t1e1_state = 0
        if boost1_state in [1, 2, 3]:
            pipe_t1e1_state = 1

        # BOOST 3
        boost3_state = 0
        boost3_xp_state = fuel_overhead.boost3.get_state()
        match boost3_xp_state:
            case 0:
                boost3_state = 1 # on
            case 1:
                boost3_state = 0 # off
            case 2:
                boost3_state = 2 # stby
        
        if xtk_23_state == 2 or xtk_13_state == 2 and fuel_overhead.backup_13.get_state() == 0:
            boost3_state = 3 # both
        
        pipe_t3e3_state = 0
        if boost3_state in [1, 2, 3]:
            pipe_t3e3_state = 1

        # BOOST 3
        boost2_state = 0
        boost2_xp_state = fuel_overhead.boost2.get_state()
        match boost2_xp_state:
            case 0:
                boost2_state = 1 # on
            case 1:
                boost2_state = 0 # off
            case 2:
                boost2_state = 2 # stby
        
        if xtk_12_state == 2 or xtk_23_state == 1:
            boost2_state = 3 # both
        
        pipe_t2e2_state = 0
        if boost2_state in [1, 2, 3]:
            pipe_t2e2_state = 1

        # special xbp logic

        # apu
        apu_state = 0
        if eng_apu.apu_master.get_state() == 1:
            apu_state = 1
        
        pipe_apu_state = apu_state
    
        # eng 1
        eng1_state = 0
        if (xp_ac.ACState.get_curr_param(cls.N2_ENG1) or 0) > cls.ENG_WORKING_THRESHOLD_N2: 
            eng1_state = 1

        # eng 2
        eng2_state = 0
        if (xp_ac.ACState.get_curr_param(cls.N2_ENG2) or 0) > cls.ENG_WORKING_THRESHOLD_N2: 
            eng2_state = 1

        # eng 2
        eng3_state = 0
        if (xp_ac.ACState.get_curr_param(cls.N2_ENG3) or 0) > cls.ENG_WORKING_THRESHOLD_N2: 
            eng3_state = 1
        
        new_state = [
            int(xtk_13_state),
            int(xtk_12_state),
            int(xtk_23_state),

            int(xbp_13_state),
            int(xbp_12_state),
            int(xbp_23_state),

            int(pipe_t1t3_state),
            int(pipe_t1t2_state),
            int(pipe_t2t3_state),

            int(pipe_xbp13_state),
            int(pipe_xbp12_state),
            int(pipe_xbp23_state),

            int(pipe_t1e1_state),
            int(pipe_t3e3_state),
            int(pipe_t2e2_state),

            int(pipe_apu_state),

            int(boost1_state),
            int(boost3_state),
            int(boost2_state),

            int(apu_state),
            int(eng1_state),
            int(eng2_state),
            int(eng3_state)
        ]

        if new_state != cls.old_state:
            cls.old_state = new_state
        
            await xp.set_param(cls.VALVE_XTK_13, int(xtk_13_state))
            await xp.set_param(cls.VALVE_XTK_12, int(xtk_12_state))
            await xp.set_param(cls.VALVE_XTK_23, int(xtk_23_state))

            await xp.set_param(cls.VALVE_XBP_13, int(xbp_13_state))
            await xp.set_param(cls.VALVE_XBP_12, int(xbp_12_state))
            await xp.set_param(cls.VALVE_XBP_23, int(xbp_23_state))

            await xp.set_param(cls.PIPE_t1t3, int(pipe_t1t3_state))
            await xp.set_param(cls.PIPE_t1t2, int(pipe_t1t2_state))
            await xp.set_param(cls.PIPE_t2t3, int(pipe_t2t3_state))

            await xp.set_param(cls.PIPE_xbp13, int(pipe_xbp13_state))
            await xp.set_param(cls.PIPE_xbp12, int(pipe_xbp12_state))
            await xp.set_param(cls.PIPE_xbp23, int(pipe_xbp23_state))

            await xp.set_param(cls.PIPE_t1e1, int(pipe_t1e1_state))
            await xp.set_param(cls.PIPE_t3e3, int(pipe_t3e3_state))
            await xp.set_param(cls.PIPE_t2e2, int(pipe_t2e2_state))

            await xp.set_param(cls.PIPE_t2apu, int(pipe_apu_state))

            await xp.set_param(cls.BOOST1, int(boost1_state))
            await xp.set_param(cls.BOOST3, int(boost3_state))
            await xp.set_param(cls.BOOST2, int(boost2_state))

            await xp.set_param(cls.APU, int(apu_state))
            await xp.set_param(cls.ENG1, int(eng1_state))
            await xp.set_param(cls.ENG2, int(eng2_state))
            await xp.set_param(cls.ENG3, int(eng3_state))
