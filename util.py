import time

from xp_aircraft_state import ACState
import xplane as xp


async def load_sit(sit_name: str):
    await ACState.wait_until_param_available("sim/time/total_running_time_sec")
    old_time = ACState.curr_params["sim/time/total_running_time_sec"]

    await xp.run_command_once(xp.Commands["sim/operation/reload_aircraft"])
    await xp.load_sit(sit_name)

    def sim_time_reset(ac_state: ACState):
        if ac_state.curr_params["sim/time/total_running_time_sec"] < old_time:
            return True
    
    # NOTE: wait while sit is loaded
    await ACState.data_condition(sim_time_reset)
    
    # await run_command_once(writer, xp.Commands["sim/operation/toggle_main_menu"])
    await xp.run_command_once(xp.Commands["sim/operation/fix_all_systems"])

    # set view
    await xp.run_command_once(xp.Commands["sim/view/forward_with_nothing"])


async def subscribe_to_all_data():
    for p in xp.Params:
        await xp.subscribe_to_param(p)

    for f in xp.Params:
        await xp.subscribe_to_param(f)

    await ACState.wait_until_param_available(xp.Params["sim/time/total_running_time_sec"])


async def request_all_data():
    """ получить актуальное значения всех параметров """
    for p in xp.Params:
        await xp.subscribe_to_param(p)

    for f in xp.Params:
        await xp.subscribe_to_param(f)

    await ACState.wait_until_param_available("sim/time/total_running_time_sec")


def blink_anim(every_period_sec: float):
    start = time.time()
    on = True
    while True:
        end = time.time()
        if end - start >= every_period_sec:
            start = time.time()
            on = not on
        
        yield on
