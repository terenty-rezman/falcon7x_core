import time
import asyncio

from common.xp_aircraft_state import ACState
import xplane.master as xp
from xplane.params import Params, Commands


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


# async def request_all_data():
#     """ получить актуальное значения всех параметров """
#     for p in Params:
#         await xp.subscribe_to_param(p)

#     await ACState.wait_until_param_available("sim/time/total_running_time_sec")


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


