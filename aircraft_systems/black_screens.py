import asyncio

import common.xp_aircraft_state as xp_ac
import xplane.master as xp
import common.sane_tasks as sane_tasks
import common.simulation as sim
import overhead_panel.fire_panel as fp 

from aircraft_systems.system_base import System
from xplane.params import Params
import middle_pedestal.engine as engine_panel
import overhead_panel.engines_apu as overhead_engines
import synoptic_remote.param_overrides as synoptic_overrides

import overhead_panel.dc_supply as dc


class LeftBlackScreen(System):
    next_wake_sleep_delay = 2

    LEFT = xp.Params["sim/custom/7x/z_left_black_screen"]

    logic_task = None
    is_killing = False

    prev_state = None

    @classmethod
    def start_condition(cls):
        return True

    @classmethod
    async def system_logic_task(cls):
        new_state = None

        if dc.bat1.get_state() == 0:  
            new_state = 1
        else:
            if dc.rh_init.get_state() == 1: 
                new_state = 2
            else:
                new_state = 0
        
        if new_state != cls.prev_state:
            cls.prev_state = new_state
            await xp.set_param(cls.LEFT, new_state)


class MiddleUpBlackScreen(System):
    next_wake_sleep_delay = 2

    MIDDLE_UP = xp.Params["sim/custom/7x/z_middle_up_black_screen"]

    logic_task = None
    is_killing = False

    prev_state = None

    @classmethod
    def start_condition(cls):
        return True

    @classmethod
    async def system_logic_task(cls):
        new_state = None

        if dc.bat1.get_state() == 0:  
            new_state = 1
        else:
            if dc.rh_init.get_state() == 1:
                new_state = 2
            elif dc.rh_init.get_state() == 0 and dc.lh_master.get_state() == 0 and dc.rh_master.get_state() == 1: 
                new_state = 2
            else:
                new_state = 0

        if new_state != cls.prev_state:
            cls.prev_state = new_state
            await xp.set_param(cls.MIDDLE_UP, new_state)


class RightBlackScreen(System):
    next_wake_sleep_delay = 2

    RIGHT = xp.Params["sim/custom/7x/z_right_black_screen"]

    logic_task = None
    is_killing = False

    prev_state = None

    @classmethod
    def start_condition(cls):
        return True

    @classmethod
    async def system_logic_task(cls):
        new_state = None

        if dc.bat2.get_state() == 0:  
            new_state = 1
        else:
            if dc.lh_master.get_state() == 1 and dc.rh_master.get_state() == 1: 
                new_state = 2
            else:
                new_state = 0

        if new_state != cls.prev_state:
            cls.prev_state = new_state
            await xp.set_param(cls.RIGHT, new_state)
            

class MiddleDownBlackScreen(System):
    next_wake_sleep_delay = 2

    MIDDLE_DOWN = xp.Params["sim/custom/7x/z_middle_down_black_screen"]

    logic_task = None
    is_killing = False

    prev_state = None

    @classmethod
    def start_condition(cls):
        return True

    @classmethod
    async def system_logic_task(cls):
        new_state = None

        if dc.bat1.get_state() == 0:  
            new_state = 1
        else:
            if dc.rh_init.get_state() == 0 and dc.lh_master.get_state() == 0 and dc.rh_master.get_state() == 0: 
                new_state = 0
            elif dc.rh_isol.get_state() == 0:
                new_state = 2
            else:
                new_state = 1

        if new_state != cls.prev_state:
            cls.prev_state = new_state
            await xp.set_param(cls.MIDDLE_DOWN, new_state)


class MiniBlackScreen(System):
    next_wake_sleep_delay = 2

    MINI = xp.Params["sim/custom/7x/z_mini_black_screen"]

    logic_task = None
    is_killing = False

    prev_state = None

    @classmethod
    def start_condition(cls):
        return True

    @classmethod
    async def system_logic_task(cls):
        new_state = None

        if dc.bat1.get_state() == 0:  
            new_state = 1
        else:
            if dc.lh_init.get_state() == 0:
                new_state = 0 
            else:
                new_state = 1

        if new_state != cls.prev_state:
            cls.prev_state = new_state
            await xp.set_param(cls.MINI, new_state)
