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


class AllValves(System):
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
    PIPE_xpb12 = xp.Params["sim/custom/7x/z_fuel_pipe_xbp12"]
    PIPE_xbp23 = xp.Params["sim/custom/7x/z_fuel_pipe_xbp23"]
    PIPE_xpb13 = xp.Params["sim/custom/7x/z_fuel_pipe_xbp13"]
    PIPE_t1e1 = xp.Params["sim/custom/7x/z_fuel_pipe_t1e1"]
    PIPE_t2e2 = xp.Params["sim/custom/7x/z_fuel_pipe_t2e2"]
    PIPE_t3e3 = xp.Params["sim/custom/7x/z_fuel_pipe_t3e3"]

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
        
        pipe_t1t3 = 0
        if xtk_13_state:
            pipe_t1t3 = 1

        pipe_t1t2 = 0
        if xtk_12_state:
            pipe_t1t2 = 1
        
        await xp.set_param(cls.VALVE_XTK_13, int(xtk_13_state))
        await xp.set_param(cls.VALVE_XTK_12, int(xtk_12_state))
        await xp.set_param(cls.VALVE_XTK_23, int(xtk_23_state))

        await xp.set_param(cls.PIPE_t1t3, int(pipe_t1t3))
        await xp.set_param(cls.PIPE_t1t2, int(pipe_t1t2))
