"""""
drefs that can be overriden by core logic and sent to qml synoptic
"""

import time
from contextlib import asynccontextmanager
import asyncio
from typing import List
import bisect

import numpy as np

from xplane.params import Params
import synoptic_remote.synoptic_connection as synoptic_connection
import common.sane_tasks as sane_tasks
import common.xp_aircraft_state as xp_ac


overrides_values = dict()


async def enable_param_overrides(params_list: List[Params]):
    xp_ac.ACState.enable_param_overrides(params_list)
    params_list = [str(p) for p in params_list]
    await synoptic_connection.enable_param_overrides(params_list)


async def disable_param_overrides(params_list: List[Params]):
    xp_ac.ACState.disable_param_overrides(params_list)
    params_list = [str(p) for p in params_list if p not in xp_ac.ACState.enabled_overrides]
    await synoptic_connection.disable_param_overrides(params_list)


@asynccontextmanager
async def override_params(*args, **kwds):
    await enable_param_overrides(*args, **kwds)
    try:
        yield None
    except Exception as e:
        raise e
    finally:
        await disable_param_overrides(*args, **kwds)


def set_override_value(param: Params, value):
    global overrides_values

    if param in xp_ac.ACState.enabled_overrides:
        xp_ac.ACState.set_curr_param(param, value)
        overrides_values[str(param)] = value
    else:
        raise Exception(f"param {param} is not enabled for override!")


def linear_anim(param: Params, start_val, finish_val, interval_sec: float, sleep_sec: float = 0.1):
    async def linear_anim_task():
        start_time = time.time()

        speed = (finish_val - start_val) / interval_sec;
        value = start_val

        while True: 
            curr_time = time.time()
            dt = curr_time - start_time

            value = start_val + speed * dt

            set_override_value(param, value)

            if dt >= interval_sec:
                break

            await asyncio.sleep(sleep_sec)
    
    return sane_tasks.spawn(linear_anim_task())


def _1d_table_anim(param: Params, t_values, y_values, sleep_sec: float = 0.1):
    async def _1d_table_anim_task():
        start_time = time.time()
        end_time = t_values[-1]

        while True: 
            curr_time = time.time()
            dt = curr_time - start_time

            value = np.interp(dt, t_values, y_values)

            set_override_value(param, value)

            if dt > end_time:
                break

            await asyncio.sleep(sleep_sec)
    
    return sane_tasks.spawn(_1d_table_anim_task())


def _1d_table_start_from_curr_val_anim(param: Params, t_values, y_values, sleep_sec: float = 0.1):
    async def _1d_table_anim_task():
        # find time from which we start interpolation
        start_value = xp_ac.ACState.get_curr_param(param) 
        interp_from_idx = bisect.bisect_left(y_values, start_value)

        if interp_from_idx == len(y_values):
            interp_from_idx = interp_from_idx - 1

        interp_from_time = t_values[interp_from_idx] 

        start_time = time.time()
        end_time = t_values[-1]

        while True: 
            curr_time = time.time()
            dt = curr_time - start_time

            if dt >= interp_from_time:
                value = np.interp(dt, t_values, y_values)
            else:
                value = start_value

            set_override_value(param, value)

            if dt > end_time:
                break

            await asyncio.sleep(sleep_sec)
    
    return sane_tasks.spawn(_1d_table_anim_task())


def clear_override_values():
    global overrides_values
    overrides_values = dict()
