import asyncio
import traceback

import common.xp_aircraft_state as xp_ac
import common.sane_tasks as sane_tasks


scenarios = {}
# scenario = lambda f: scenarios.setdefault(f.__name__, f)

def scenario(procedure_type: str, path: str, procedure_name: str):
    def wrapper(fcn):
        key = (procedure_type, path, procedure_name)
        scenarios[key] = fcn
        return fcn
    return wrapper


class Scenario:
    current_scenario_task = None

    @classmethod
    async def clear_all(cls):
        # clear current task
        if cls.current_scenario_task:
            cls.current_scenario_task.cancel()
            print(f"stoped task {cls.current_scenario_task}")
            try:
                await cls.current_scenario_task
            # except Exception as ex: #asyncio.CancelledError:
            except BaseException as ex:
                print(traceback.format_exc())
                print(f"stoped task {cls.current_scenario_task}")

            cls.current_scenario_task = None

    @classmethod
    async def run_scenario_task(cls, task_name, ac_state: xp_ac.ACState):
        await cls.clear_all()

        task = sane_tasks.spawn(scenarios[task_name](ac_state))
        task.add_done_callback(Scenario.on_scenario_done)
        cls.current_scenario_task = task
        print(f"run task {task_name}")
    
    @classmethod
    def on_scenario_done(cls, task):
        print(f"task finished {task}")
        cls.current_scenario_task = None


@scenario("TEST", "TEST", "test_scenrio_1")
async def test_scenario_1(ac_state: xp_ac.ACState):
    def fly_height_200m(ac_state: xp_ac.ACState):
        elevation = "sim/flightmodel/position/elevation"
        if not ac_state.param_available(elevation):
            return False

        if ac_state.curr_params[elevation] - ac_state.initial_params[elevation] > 200:
            return True
    
    await ac_state.data_condition(fly_height_200m)

    print("fire the engine")
    #await xp.set_param(xp.Failures["sim/operation/failures/rel_engfir0"], 6)
    # await xp.set_param(xp.Failures["sim/operation/failures/rel_engfla0"], 6)

    # await asyncio.sleep(10)

    # press engine 1 shutoff button on overhead panel
    # await OverheadPanel["Fireclosed 0"].set_enabled(True)
    # await asyncio.sleep(5)

    # await OverheadPanel["dish 2 2 2 2"].set_enabled(True)
    # roll control, left control column jammed
    # await xp.set_param(xp.Failures["sim/operation/failures/rel_ail_L_jam"], 6)

# abnormal 47
# emergency 38
# normal 13

# from scenarios import *
# from scenarios import _26_elec_aft_dist_box_ovht 

from scenarios import abnormal
from scenarios import emergency
from scenarios import normal
