import time as sys_time
import traceback
import asyncio
from dataclasses import dataclass
from typing import List

import common.sane_tasks as sane_tasks


simulation_time = 0
simulation_paused = False

last_real_time = None
sleep_delay = 0.1


@dataclass
class Sleep():
    future: asyncio.Future
    end_time: float


sleeps_list: List[Sleep] = []


def run_time_update_task():
    sane_tasks.spawn(_sim_time_update_task())


async def _sim_time_update_task():
    global simulation_time
    global simulation_paused
    global last_real_time

    last_real_time = sys_time.time()

    while True:
        if not simulation_paused:
            curr_real_time = sys_time.time()
            delta = curr_real_time - last_real_time
            simulation_time += delta
            last_real_time = curr_real_time

            update_sleep_timers()
        
        await asyncio.sleep(sleep_delay)


def sleep(sleep_time_sec):
    f = asyncio.Future()
    sleeps_list.append(
        Sleep(
            f, simulation_time + sleep_time_sec
        )
    )
    return f


def update_sleep_timers():
    global sleeps_list

    for s in sleeps_list:
        if simulation_time >= s.end_time:
            try:
                s.future.set_result(None)
            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)

    sleeps_list = [s for s in sleeps_list if s.future.done() == False]


def time():
    return simulation_time
