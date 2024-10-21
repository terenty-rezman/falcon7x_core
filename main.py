import asyncio
from enum import Enum 
import traceback

from xp_aircraft_state import ACState
from aircraft_systems.aicrcaft_systems import Systems as ACSystems

from joystick import Joystick
from scenario import Scenario

import xplane as xp
from instrument_panel import CockpitPanel
import instrument_panel as op
import util


SERVER_ADDRESS = "127.0.0.1"
SERVER_PORT = 51000


joystick = Joystick()
if joystick.is_plugged():
    joystick.run_in_thread()
else:
    print("No joystick connected!")


def on_new_xp_data(type, dataref, value):
    dataref = xp.Params[dataref]

    # запомнить стартовое состояния ЛА
    if dataref not in ACState.initial_params:
        ACState.initial_params[dataref] = value

    # запомнить текущее состояние ЛА
    ACState.curr_params[dataref] = value

    ACState.update_data_callbacks()


def on_data_exception(ex: Exception):
    print(traceback.format_exc())


async def load_default_sit():
    await util.load_sit("Output/situations/1.sit")


async def main_loop():
    ACState.clear_all()

    await load_default_sit()

    await util.subscribe_to_all_data()

    await xp.set_param(xp.Params["sim/operation/override/override_joystick"], 1)

    await Scenario.clear_all()
    await ACSystems.reset()
    ACState.clear_all()

    await CockpitPanel.reset_to_default_state()

    await util.request_all_data()

    # await Scenario.run_scenario_task("fcs_direct_laws_active_1", ACState)

    while True:
        x, y, z, rz = joystick.get_axes_values()
        if joystick.is_plugged():
            await xp.set_param(xp.Params["sim/joystick/yoke_roll_ratio"], x)
            await xp.set_param(xp.Params["sim/joystick/yoke_pitch_ratio"], -y)
            await xp.set_param(xp.Params["sim/joystick/yoke_heading_ratio"], rz - z)

        # NOTE: maybe run in separate task?
        await ACSystems.update()

        await asyncio.sleep(0.1)


async def main():
    await op.run_receive_uso_task()

    await xp.connect_to_xplane_until_success(SERVER_ADDRESS, SERVER_PORT, on_new_xp_data, on_data_exception)

    await op.run_receive_state_task()
    await op.run_send_state_task()

    await main_loop()   

    await xp.disconnect()


asyncio.run(main())


