import asyncio
import traceback
import inspect

import common.xp_aircraft_state as xp_ac
import common.sane_tasks as sane_tasks
from common.reset_systems import reset_all_systems
import common.simulation as sim
import xplane.master as xp


scenarios = {}
# scenario = lambda f: scenarios.setdefault(f.__name__, f)

def scenario(procedure_type: str, path: str, procedure_name: str):
    def wrapper(fcn_or_class):
        key = (procedure_type, path, procedure_name)

        if inspect.isclass(fcn_or_class):
            # if class
            scenarios[key] = fcn_or_class.procedure 
        else:
            # if fcn
            scenarios[key] = fcn_or_class
        return fcn_or_class

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
    await reset_all_systems() 


@scenario("TEST", "TEST", "test_scenario_1")
async def test_scenario_1(ac_state: xp_ac.ACState):
    from overhead_panel.fire_panel import fire_test

    await sim.sleep(5)

    await xp.set_param(xp.Params["sim/weather/wind_altitude_msl_m[0]"], 1000)
    await xp.set_param(xp.Params["sim/weather/wind_direction_degt[0]"], 0)
    await xp.set_param(xp.Params["sim/weather/wind_speed_kt[0]"], 250)
    await xp.set_param(xp.Params["sim/weather/shear_speed_kt[0]"], 0)
    await xp.set_param(xp.Params["sim/weather/shear_direction_degt[0]"], 0)
    await xp.set_param(xp.Params["sim/weather/turbulence[0]"], 0.5)

    await xp.set_param(xp.Params["sim/weather/wind_altitude_msl_m[0]"], 2000)
    await xp.set_param(xp.Params["sim/weather/wind_direction_degt[0]"], 0)
    await xp.set_param(xp.Params["sim/weather/wind_speed_kt[0]"], 200)
    await xp.set_param(xp.Params["sim/weather/shear_speed_kt[0]"], 0)
    await xp.set_param(xp.Params["sim/weather/shear_direction_degt[0]"], 0)
    await xp.set_param(xp.Params["sim/weather/turbulence[0]"], 0.5)

    await xp.set_param(xp.Params["sim/weather/wind_altitude_msl_m[0]"], 3000)
    await xp.set_param(xp.Params["sim/weather/wind_direction_degt[0]"], 0)
    await xp.set_param(xp.Params["sim/weather/wind_speed_kt[0]"], 200)
    await xp.set_param(xp.Params["sim/weather/shear_speed_kt[0]"], 0)
    await xp.set_param(xp.Params["sim/weather/shear_direction_degt[0]"], 0)
    await xp.set_param(xp.Params["sim/weather/turbulence[0]"], 0.5)

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

    # await sim.sleep(10)

    # press engine 1 shutoff button on overhead panel
    # await OverheadPanel["Fireclosed 0"].set_enabled(True)
    # await sim.sleep(5)

    # await OverheadPanel["dish 2 2 2 2"].set_enabled(True)
    # roll control, left control column jammed
    # await xp.set_param(xp.Failures["sim/operation/failures/rel_ail_L_jam"], 6)


@scenario("TEST", "WIND", "TAILWIND")
async def test_wind_windshear(ac_state: xp_ac.ACState):
    try:
        # degrees
        wind_direction = 0 
        shear_direction = 0
        wind_speed_kts = 30

        my_direction = xp.ACState.get_curr_param(xp.Params["sim/cockpit2/gauges/indicators/heading_AHARS_deg_mag_pilot"]) or 0

        # попутный ветер
        # tail wind
        wind_direction = my_direction + 180

        await xp.set_param(xp.Params["sim/weather/wind_altitude_msl_m[0]"], 1000)
        await xp.set_param(xp.Params["sim/weather/wind_direction_degt[0]"], wind_direction)
        await xp.set_param(xp.Params["sim/weather/wind_speed_kt[0]"], wind_speed_kts)
        await xp.set_param(xp.Params["sim/weather/shear_speed_kt[0]"], 0)
        await xp.set_param(xp.Params["sim/weather/shear_direction_degt[0]"], shear_direction)
        await xp.set_param(xp.Params["sim/weather/turbulence[0]"], 0.5)

        await xp.set_param(xp.Params["sim/weather/wind_altitude_msl_m[0]"], 2000)
        await xp.set_param(xp.Params["sim/weather/wind_direction_degt[0]"], wind_direction)
        await xp.set_param(xp.Params["sim/weather/wind_speed_kt[0]"], wind_speed_kts)
        await xp.set_param(xp.Params["sim/weather/shear_speed_kt[0]"], 0)
        await xp.set_param(xp.Params["sim/weather/shear_direction_degt[0]"], shear_direction)
        await xp.set_param(xp.Params["sim/weather/turbulence[0]"], 0.5)

        await xp.set_param(xp.Params["sim/weather/wind_altitude_msl_m[0]"], 3000)
        await xp.set_param(xp.Params["sim/weather/wind_direction_degt[0]"], wind_direction)
        await xp.set_param(xp.Params["sim/weather/wind_speed_kt[0]"], wind_speed_kts)
        await xp.set_param(xp.Params["sim/weather/shear_speed_kt[0]"], 0)
        await xp.set_param(xp.Params["sim/weather/shear_direction_degt[0]"], shear_direction)
        await xp.set_param(xp.Params["sim/weather/turbulence[0]"], 0.5)

        await sim.sleep(5 * 60)
    finally:
        await xp.set_param(xp.Params["sim/weather/wind_altitude_msl_m[0]"], 0)
        await xp.set_param(xp.Params["sim/weather/wind_direction_degt[0]"], 0)
        await xp.set_param(xp.Params["sim/weather/wind_speed_kt[0]"], 0)
        await xp.set_param(xp.Params["sim/weather/shear_speed_kt[0]"], 0)
        await xp.set_param(xp.Params["sim/weather/shear_direction_degt[0]"], 0)
        await xp.set_param(xp.Params["sim/weather/turbulence[0]"], 0)

        await xp.set_param(xp.Params["sim/weather/wind_altitude_msl_m[0]"], 0)
        await xp.set_param(xp.Params["sim/weather/wind_direction_degt[0]"], 0)
        await xp.set_param(xp.Params["sim/weather/wind_speed_kt[0]"], 0)
        await xp.set_param(xp.Params["sim/weather/shear_speed_kt[0]"], 0)
        await xp.set_param(xp.Params["sim/weather/shear_direction_degt[0]"], 0)
        await xp.set_param(xp.Params["sim/weather/turbulence[0]"], 0)

        await xp.set_param(xp.Params["sim/weather/wind_altitude_msl_m[0]"], 0)
        await xp.set_param(xp.Params["sim/weather/wind_direction_degt[0]"], 0)
        await xp.set_param(xp.Params["sim/weather/wind_speed_kt[0]"], 0)
        await xp.set_param(xp.Params["sim/weather/shear_speed_kt[0]"], 0)
        await xp.set_param(xp.Params["sim/weather/shear_direction_degt[0]"], 0)
        await xp.set_param(xp.Params["sim/weather/turbulence[0]"], 0)


@scenario("TEST", "WIND", "HEADWIND")
async def test_wind_head(ac_state: xp_ac.ACState):
    try:
        # degrees
        wind_direction = 0 
        shear_direction = 0
        wind_speed_kts = 30

        my_direction = xp.ACState.get_curr_param(xp.Params["sim/cockpit2/gauges/indicators/heading_AHARS_deg_mag_pilot"]) or 0

        # встречный ветер
        # tail wind
        wind_direction = my_direction

        await xp.set_param(xp.Params["sim/weather/wind_altitude_msl_m[0]"], 1000)
        await xp.set_param(xp.Params["sim/weather/wind_direction_degt[0]"], wind_direction)
        await xp.set_param(xp.Params["sim/weather/wind_speed_kt[0]"], wind_speed_kts)
        await xp.set_param(xp.Params["sim/weather/shear_speed_kt[0]"], 0)
        await xp.set_param(xp.Params["sim/weather/shear_direction_degt[0]"], shear_direction)
        await xp.set_param(xp.Params["sim/weather/turbulence[0]"], 0.5)

        await xp.set_param(xp.Params["sim/weather/wind_altitude_msl_m[0]"], 2000)
        await xp.set_param(xp.Params["sim/weather/wind_direction_degt[0]"], wind_direction)
        await xp.set_param(xp.Params["sim/weather/wind_speed_kt[0]"], wind_speed_kts)
        await xp.set_param(xp.Params["sim/weather/shear_speed_kt[0]"], 0)
        await xp.set_param(xp.Params["sim/weather/shear_direction_degt[0]"], shear_direction)
        await xp.set_param(xp.Params["sim/weather/turbulence[0]"], 0.5)

        await xp.set_param(xp.Params["sim/weather/wind_altitude_msl_m[0]"], 3000)
        await xp.set_param(xp.Params["sim/weather/wind_direction_degt[0]"], wind_direction)
        await xp.set_param(xp.Params["sim/weather/wind_speed_kt[0]"], wind_speed_kts)
        await xp.set_param(xp.Params["sim/weather/shear_speed_kt[0]"], 0)
        await xp.set_param(xp.Params["sim/weather/shear_direction_degt[0]"], shear_direction)
        await xp.set_param(xp.Params["sim/weather/turbulence[0]"], 0.5)

        await sim.sleep(5 * 60)
    finally:
        await xp.set_param(xp.Params["sim/weather/wind_altitude_msl_m[0]"], 0)
        await xp.set_param(xp.Params["sim/weather/wind_direction_degt[0]"], 0)
        await xp.set_param(xp.Params["sim/weather/wind_speed_kt[0]"], 0)
        await xp.set_param(xp.Params["sim/weather/shear_speed_kt[0]"], 0)
        await xp.set_param(xp.Params["sim/weather/shear_direction_degt[0]"], 0)
        await xp.set_param(xp.Params["sim/weather/turbulence[0]"], 0)

        await xp.set_param(xp.Params["sim/weather/wind_altitude_msl_m[0]"], 0)
        await xp.set_param(xp.Params["sim/weather/wind_direction_degt[0]"], 0)
        await xp.set_param(xp.Params["sim/weather/wind_speed_kt[0]"], 0)
        await xp.set_param(xp.Params["sim/weather/shear_speed_kt[0]"], 0)
        await xp.set_param(xp.Params["sim/weather/shear_direction_degt[0]"], 0)
        await xp.set_param(xp.Params["sim/weather/turbulence[0]"], 0)

        await xp.set_param(xp.Params["sim/weather/wind_altitude_msl_m[0]"], 0)
        await xp.set_param(xp.Params["sim/weather/wind_direction_degt[0]"], 0)
        await xp.set_param(xp.Params["sim/weather/wind_speed_kt[0]"], 0)
        await xp.set_param(xp.Params["sim/weather/shear_speed_kt[0]"], 0)
        await xp.set_param(xp.Params["sim/weather/shear_direction_degt[0]"], 0)
        await xp.set_param(xp.Params["sim/weather/turbulence[0]"], 0)


@scenario("TEST", "WIND", "CROSSWIND")
async def test_wind_windshear(ac_state: xp_ac.ACState):
    try:
        # degrees
        wind_direction = 0 
        shear_direction = 0
        wind_speed_kts = 30

        my_direction = xp.ACState.get_curr_param(xp.Params["sim/cockpit2/gauges/indicators/heading_AHARS_deg_mag_pilot"]) or 0

        # попутный ветер
        # tail wind
        wind_direction = my_direction + 90

        await xp.set_param(xp.Params["sim/weather/wind_altitude_msl_m[0]"], 1000)
        await xp.set_param(xp.Params["sim/weather/wind_direction_degt[0]"], wind_direction)
        await xp.set_param(xp.Params["sim/weather/wind_speed_kt[0]"], wind_speed_kts)
        await xp.set_param(xp.Params["sim/weather/shear_speed_kt[0]"], 0)
        await xp.set_param(xp.Params["sim/weather/shear_direction_degt[0]"], shear_direction)
        await xp.set_param(xp.Params["sim/weather/turbulence[0]"], 0.5)

        await xp.set_param(xp.Params["sim/weather/wind_altitude_msl_m[0]"], 2000)
        await xp.set_param(xp.Params["sim/weather/wind_direction_degt[0]"], wind_direction)
        await xp.set_param(xp.Params["sim/weather/wind_speed_kt[0]"], wind_speed_kts)
        await xp.set_param(xp.Params["sim/weather/shear_speed_kt[0]"], 0)
        await xp.set_param(xp.Params["sim/weather/shear_direction_degt[0]"], shear_direction)
        await xp.set_param(xp.Params["sim/weather/turbulence[0]"], 0.5)

        await xp.set_param(xp.Params["sim/weather/wind_altitude_msl_m[0]"], 3000)
        await xp.set_param(xp.Params["sim/weather/wind_direction_degt[0]"], wind_direction)
        await xp.set_param(xp.Params["sim/weather/wind_speed_kt[0]"], wind_speed_kts)
        await xp.set_param(xp.Params["sim/weather/shear_speed_kt[0]"], 0)
        await xp.set_param(xp.Params["sim/weather/shear_direction_degt[0]"], shear_direction)
        await xp.set_param(xp.Params["sim/weather/turbulence[0]"], 0.5)

        await sim.sleep(5 * 60)
    finally:
        await xp.set_param(xp.Params["sim/weather/wind_altitude_msl_m[0]"], 0)
        await xp.set_param(xp.Params["sim/weather/wind_direction_degt[0]"], 0)
        await xp.set_param(xp.Params["sim/weather/wind_speed_kt[0]"], 0)
        await xp.set_param(xp.Params["sim/weather/shear_speed_kt[0]"], 0)
        await xp.set_param(xp.Params["sim/weather/shear_direction_degt[0]"], 0)
        await xp.set_param(xp.Params["sim/weather/turbulence[0]"], 0)

        await xp.set_param(xp.Params["sim/weather/wind_altitude_msl_m[0]"], 0)
        await xp.set_param(xp.Params["sim/weather/wind_direction_degt[0]"], 0)
        await xp.set_param(xp.Params["sim/weather/wind_speed_kt[0]"], 0)
        await xp.set_param(xp.Params["sim/weather/shear_speed_kt[0]"], 0)
        await xp.set_param(xp.Params["sim/weather/shear_direction_degt[0]"], 0)
        await xp.set_param(xp.Params["sim/weather/turbulence[0]"], 0)

        await xp.set_param(xp.Params["sim/weather/wind_altitude_msl_m[0]"], 0)
        await xp.set_param(xp.Params["sim/weather/wind_direction_degt[0]"], 0)
        await xp.set_param(xp.Params["sim/weather/wind_speed_kt[0]"], 0)
        await xp.set_param(xp.Params["sim/weather/shear_speed_kt[0]"], 0)
        await xp.set_param(xp.Params["sim/weather/shear_direction_degt[0]"], 0)
        await xp.set_param(xp.Params["sim/weather/turbulence[0]"], 0)


# abnormal 47
# emergency 38
# normal 13

from scenarios import abnormal
from scenarios import emergency
from scenarios import normal
from scenarios import maintenance
