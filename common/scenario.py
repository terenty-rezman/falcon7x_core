import asyncio
import traceback

import common.xp_aircraft_state as xp_ac
import xplane.master as xp
from xplane.master import Params, Commands
import common.sane_tasks as sane_tasks
from cas import cas


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
    current_scenario_name = None

    @classmethod
    async def kill_current_scenario(cls):
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
            cls.current_scenario_name = None

    @classmethod
    async def run_scenario_task(cls, name, ac_state: xp_ac.ACState):
        await cls.kill_current_scenario()
        
        await pre_scenario_task(ac_state) 

        task = sane_tasks.spawn(scenarios[name](ac_state))
        task.add_done_callback(Scenario.on_scenario_done)
        cls.current_scenario_task = task
        cls.current_scenario_name = name
        print(f"run task {name}")
    
    @classmethod
    def on_scenario_done(cls, task):
        print(f"task finished {task}")
        cls.current_scenario_task = None
        cls.current_scenario_name = None


async def pre_scenario_task(ac_state: xp_ac.ACState):
    await cas.remove_all_messages()
    await xp.run_command_once(Commands["sim/operation/fix_all_systems"])


@scenario("TEST", "TEST", "test_scenario_1")
async def test_scenario_1(ac_state: xp_ac.ACState):
    from overhead_panel.fire_panel import fire_test

    await asyncio.sleep(5)

    await fire_test.set_state(1)
    await asyncio.sleep(5)
    await fire_test.set_state(0)

    # def fly_height_200m(ac_state: xp_ac.ACState):
    #     elevation = "sim/flightmodel/position/elevation"
    #     if not ac_state.param_available(elevation):
    #         return False

    #     if ac_state.curr_params[elevation] - ac_state.initial_params[elevation] > 200:
    #         return True
    
    # await ac_state.data_condition(fly_height_200m)

    # print("fire the engine")
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
from scenarios import maintenance
