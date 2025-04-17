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

import overhead_panel.dc_supply as dc


class LeftBlackScreen(System):
    LEFT = xp.Params["sim/custom/7x/z_left_black_screen"]

    logic_task = None
    is_killing = False

    @classmethod
    def start_condition(cls):
        return True

    @classmethod
    async def system_logic_task(cls):
        if dc.bat1.get_state() == 0:  
            await xp.set_param(cls.LEFT, 1)
        
        else:
            if dc.rh_init.get_state() == 0: 
                await xp.set_param(cls.LEFT, 2)
            else:
                await asyncio.sleep(3)
                await xp.set_param(cls.LEFT, 0)


class MiddleUpBlackScreen(System):
    MIDDLE_UP = xp.Params["sim/custom/7x/z_middle_up_black_screen"]

    logic_task = None
    is_killing = False

    @classmethod
    def start_condition(cls):
        return True

    @classmethod
    async def system_logic_task(cls):
        if dc.bat1.get_state() == 0:  
            await xp.set_param(cls.MIDDLE_UP, 1)
        
        else:
            if dc.rh_init.get_state() == 0: 
                await xp.set_param(cls.MIDDLE_UP, 2)
            else:
                await asyncio.sleep(3)
                await xp.set_param(cls.MIDDLE_UP, 0)



class RightBlackScreen(System):
    RIGHT = xp.Params["sim/custom/7x/z_right_black_screen"]

    logic_task = None
    is_killing = False

    @classmethod
    def start_condition(cls):
        return True

    @classmethod
    async def system_logic_task(cls):
        if dc.bat2.get_state() == 0:  
            await xp.set_param(cls.RIGHT, 1)
        else:
            if dc.lh_master.get_state() == 0: 
                await xp.set_param(cls.RIGHT, 2)
            else:
                await xp.set_param(cls.RIGHT, 0)
            
            if dc.rh_master.get_state() == 0:
                await xp.set_param(cls.RIGHT, 2)
                await asyncio.sleep(3)
                await xp.set_param(cls.RIGHT, 0)
            else:
                await xp.set_param(cls.RIGHT, 0)
