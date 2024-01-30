import asyncio
from enum import Enum 
import traceback

from aircraft import ACState

from joystick import Joystick
from scenario import Scenario

import xplane as xp
from overhead_panel import OverheadPanel
import util


SERVER_ADDRESS = "127.0.0.1"
SERVER_PORT = 51000


joystick = Joystick()
joystick.run_in_thread()


def on_new_xp_data(type, dataref, value):
    # запомнить стартовое состояния ЛА
    if dataref not in ACState.initial_xplane_state:
        ACState.initial_xplane_state[dataref] = value

    # запомнить текущее состояние ЛА
    ACState.curr_xplane_state[dataref] = value

    ACState.update_data_callbacks()


def on_data_exception(ex: Exception):
    print(traceback.format_exc())


async def load_default_sit():
    await util.load_sit("Output/situations/1.sit")


async def main_loop():
    ACState.clear_all()
    await util.subscribe_to_all_data()

    await xp.set_param(xp.Params["sim/operation/override/override_joystick"], 1)

    await load_default_sit()
    await Scenario.clear_all()
    ACState.clear_all()

    await OverheadPanel.reset_to_default_state()

    await Scenario.run_scenario_task("test_scenario_1", ACState)

    while True:
        x, y, z, rz = joystick.get_axes_values()
        await xp.set_param(xp.Params["sim/joystick/yoke_roll_ratio"], x)
        await xp.set_param(xp.Params["sim/joystick/yoke_pitch_ratio"], -y)
        await xp.set_param(xp.Params["sim/joystick/yoke_heading_ratio"], rz - z)

        await asyncio.sleep(0.1)


async def main():
    await xp.connect_to_xplane(SERVER_ADDRESS, SERVER_PORT, on_new_xp_data, on_data_exception)

    await main_loop()   

    await xp.disconnect()


asyncio.run(main())
