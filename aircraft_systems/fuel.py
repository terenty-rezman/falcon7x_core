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
