import asyncio
from enum import Enum 
import traceback

from xp_aircraft_state import ACState
from aircraft_systems.aicrcaft_systems import Systems as ACSystems

from joystick import Joystick
from scenario import Scenario

import xplane.master as xp
import xplane.mfi as xp_mfi

from instrument_panel import CockpitPanel
import instrument_panel as op
import util
import web_interface
from cas import cas


# mfi slave xplane
MFI_XP_HOST = "192.168.32.252"

# cas displays
cas.CAS_HOST = "127.0.0.1"
cas.CAS_PORT_LEFT = 8881
cas.CAS_PORT_RIGHT = 8882

# connect to xplane plugin
XP_SERVER_HOST = "127.0.0.1"
XP_SERVER_PORT = 51000

# web interface listens on this address:
WEB_INTERFACE_HOST = "127.0.0.1"
WB_INTERFACE_PORT = 6070

# uso udp ports
USO_HOST = "127.0.0.1"
USO_RECEIVE_PORT = 2001
USO_SEND_PORT = 2002


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

    # NOTE!: maybe creating task for every param update is a bad idea
    if dataref in xp_mfi.sync_params:
        asyncio.create_task(xp_mfi.sync_param_to_slaves(dataref, value))

    ACState.update_data_callbacks()


def on_data_exception(ex: Exception):
    print(traceback.format_exc())


async def load_default_sit():
    await util.load_sit("Output/situations/1.sit")


def add_mfi_sync_list():
    xp_mfi.add_sync_param(xp.Params["sim/cockpit/weapons/firing_rate"])
    xp_mfi.add_sync_param(xp.Params["sim/custom/7x/lhinit"])
    xp_mfi.add_sync_param(xp.Params["sim/custom/7x/rhinit"])


async def main_loop():
    ACState.clear_all()

    await util.subscribe_to_time_param() # we need time param to load situation correctly 

    # await load_default_sit()

    await xp.subscribe_to_all_data()  

    await xp.set_param(xp.Params["sim/operation/override/override_joystick"], 1)

    await Scenario.clear_all()
    await ACSystems.reset()
    ACState.clear_all()

    await CockpitPanel.reset_to_default_state()

    await util.request_all_data()

    # await Scenario.run_scenario_task(("EMERGENCY", "ELECTRICAL POWER", "36 ELEC: LH+RH ESS PWR LO"), ACState)

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
    # await Scenario.run_scenario_task(("ABNORMAL", "ICE AND RAIN PROTECTION", "A/I: STALL WARNING OFFSET"), ACState)

    await op.run_receive_uso_task(USO_HOST, USO_RECEIVE_PORT)
    await op.run_send_uso_task(USO_HOST, USO_SEND_PORT)

    await xp.xp_master.connect_until_success(XP_SERVER_HOST, XP_SERVER_PORT, on_new_xp_data, on_data_exception)
    # await xp.xp_master.connect(XP_SERVER_HOST, XP_SERVER_PORT, on_new_xp_data, on_data_exception)

    # await xp_mfi.xp_mfi.connect(MFI_XP_HOST, XP_SERVER_PORT)
    add_mfi_sync_list()

    await web_interface.run_server_task(WEB_INTERFACE_HOST, WB_INTERFACE_PORT)

    await main_loop()   

    await xp.xp_master.disconnect()


asyncio.run(main())
