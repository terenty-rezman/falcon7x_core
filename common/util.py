import time
import asyncio
import inspect
import math

from common.xp_aircraft_state import ACState
import xplane.master as xp
from xplane.params import Params, Commands
import common.simulation as sim


async def load_sit(sit_name: str):
    time_param_sec = Params["sim/time/total_running_time_sec"]

    await xp.load_sit(sit_name)
    await asyncio.sleep(3)

    # NOTE: wait while sit is loaded
    # await ACState.wait_until_param_available(time_param_sec)
    await ACState.wait_until_parameter_condition(time_param_sec, lambda secs_since_situation_start: secs_since_situation_start > 3)

    await xp.run_command_once(Commands["sim/operation/reload_aircraft"])

    await xp.run_command_once(Commands["sim/operation/fix_all_systems"])

    # set view
    await xp.run_command_once(Commands["sim/view/forward_with_nothing"])


async def subscribe_to_time_param():
    await xp.subscribe_to_param(Params["sim/time/total_running_time_sec"])


async def wait_condition(condition: callable, timeout=None, sleep_sec=0.5):
    started = sim.time()
    while True:
        if condition():
            break
        await asyncio.sleep(sleep_sec)
        if timeout:
            elapsed = sim.time() - started
            if elapsed > timeout:
                break


# async def request_all_data():
#     """ получить актуальное значения всех параметров """
#     for p in Params:
#         await xp.subscribe_to_param(p)

#     await ACState.wait_until_param_available("sim/time/total_running_time_sec")

class Timer():
    started = None

    def start(self):
        self.started = time.time()
    
    def stop(self):
        self.started = None
    
    def elapsed(self):
        return time.time() - self.started


def blink_anim(every_period_sec: float):
    start = time.time()
    on = True
    while True:
        end = time.time()
        if end - start >= every_period_sec:
            start = time.time()
            on = not on
        
        yield on


def dont_await(async_f):
    """ schedule an async function to run without awaiting for the result """
    loop = asyncio.get_event_loop()
    loop.create_task(async_f)


async def in_sequence(*tasks):
    for index, task in enumerate(tasks):
        try:
            await task
        except Exception as e:
            for task in tasks[index + 1:]:
                task.close()
            raise e


def dead_zone(x, left, right, dead_zone):
    """ Зона нечувствительности """

    if math.fabs(x) < dead_zone:
        y = 0
    else:
        if x > 0:
            y = right/(right - dead_zone)*(x - dead_zone)
        else:
            y = left/(left + dead_zone)*(x + dead_zone)
    
    return y


def linear_map(val, left_min, left_max, right_min, right_max):
    # map [left_min, left_max] -> [0, 1]
    val_10 = (val - left_min) / (left_max - left_min)

    # map [0, 1] -> [right_min, right_max]
    val_r = right_min + (right_max - right_min) * val_10
    return val_r
