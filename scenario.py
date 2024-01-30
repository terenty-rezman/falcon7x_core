import asyncio

import aircraft as ac
import xplane as xp
from overhead_panel import OverheadPanel


scenarios = {}
scenario = lambda f: scenarios.setdefault(f.__name__, f)


class Scenario:
    current_scenario_task = None

    @classmethod
    async def clear_all(cls):
        # clear current task
        if cls.current_scenario_task:
            cls.current_scenario_task.cancel()
            try:
                await cls.current_scenario_task
            except asyncio.CancelledError:
                print(f"stoped task {cls.current_scenario_task.__name__}")

    @classmethod
    async def run_scenario_task(cls, task_name, ac_state: ac.ACState):
        await cls.clear_all()
        
        task = asyncio.get_event_loop().create_task(scenarios[task_name](ac_state))
        cls.current_scenario_task = task
        print(f"run task {task_name}")


@scenario
async def test_scenario_1(ac_state: ac.ACState):
    def fly_height_200m(ac_state: ac.ACState):
        elevation = "sim/flightmodel/position/elevation"
        if not ac_state.param_available(elevation):
            return False

        if ac_state.curr_xplane_state[elevation] - ac_state.initial_xplane_state[elevation] > 200:
            return True
    
    await ac_state.data_condition(fly_height_200m)

    print("fire the engine")
    # await xp.set_param(xp.Failures["sim/operation/failures/rel_engfir0"], 6)
    # await xp.set_param(xp.Failures["sim/operation/failures/rel_engfla0"], 6)

    # await asyncio.sleep(10)

    # press engine 1 shutoff button on overhead panel
    # await OverheadPanel["Fireclosed 0"].set_enabled(True)
    # await asyncio.sleep(5)

    # await OverheadPanel["dish 2 2 2 2"].set_enabled(True)
    # roll control, left control column jammed
    # await xp.set_param(xp.Failures["sim/operation/failures/rel_ail_L_jam"], 6)

