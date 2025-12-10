from common.instrument_panel import add_to_panel, TwoStateButton, FloatStepper, NLocalStateButton, PushButton
from xplane.params import Params, Commands
import xplane.master as xp
import common.xp_aircraft_state as xp_ac
import common.util as util
import common.simulation as sim
import common.sane_tasks as sane_tasks
import math

import cas.cas as cas


# "O12_c31",  # Дым [K4 Верхний пульт] [Зона освещения] [Пульт инструктора]
@add_to_panel
class misc_smoke(NLocalStateButton):
    states = [0, 1]
    state = 0


# "O12_c29",  # Подача [K4 Верхний пульт] [Зона освещения] [Пульт инструктора]
@add_to_panel
class misc_supply(NLocalStateButton):
    states = [0, 1]
    state = 0


# "O12_c30",  # Вытяжка [K4 Верхний пульт] [Зона освещения] [Пульт инструктора]
@add_to_panel
class misc_extract(NLocalStateButton):
    states = [0, 1]
    state = 0


@add_to_panel
class misc_et_timer_left(NLocalStateButton):
    dataref = xp.Params["sim/custom/7x/z_et_timer_left"]
    states = [0, 1, 2]
    state = 0

    timer_task = None
    timer_stop = False

    @classmethod
    async def timer_task_fcn(cls):
        while not cls.timer_stop:
            curr_secs = xp.ACState.get_curr_param(cls.dataref)
            curr_secs += 1
            await xp.set_param(cls.dataref, curr_secs)
            await sim.sleep(1)

    @classmethod
    async def set_state(cls, state):
        if state == 0:
            cls.timer_stop = True
            await xp.set_param(cls.dataref, 0)
        elif state == 1:
            await xp.set_param(cls.dataref, 0)
            cls.timer_stop = False
            cls.timer_task = sane_tasks.spawn(cls.timer_task_fcn)
        elif state == 2:
            cls.timer_stop = True
            
        return await super().set_state(state)
    

@add_to_panel
class misc_et_timer_right(misc_et_timer_left):
    dataref = xp.Params["sim/custom/7x/z_et_timer_right"]

    states = [0, 1, 2]
    state = 0

    timer_task = None
    timer_stop = False
