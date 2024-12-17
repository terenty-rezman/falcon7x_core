import timeit
import asyncio
from enum import Enum 
import traceback

from common.xp_aircraft_state import ACState
from aircraft_systems.aicrcaft_systems import Systems as ACSystems

from common.joystick import Joystick
from common.scenario import Scenario

import xplane.master as xp
import xplane.mfi as xp_mfi

from common.instrument_panel import CockpitPanel
import common.instrument_panel as op
import common.util as util
import common.web_interface as web_interface
from cas import cas
import synoptic_remote.synoptic as synoptic_remote


# mfi slave xplane
MFI_XP_HOST = "192.168.32.252"

# cas displays
cas.CAS_HOST = "127.0.0.1"
cas.CAS_PORT_LEFT = 8881
cas.CAS_PORT_RIGHT = 8882

# connect to master xplane plugin
XP_MASTER_HOST = "127.0.0.1"
XP_MASTER_PORT = 51000

# native xplane udp port to send to
XP_MASTER_UDP_PORT = 49000

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


start = timeit.timeit()

def on_new_xp_data(type, dataref, value):
    # global start
    dataref = xp.Params[dataref]

    # запомнить стартовое состояния ЛА
    # if dataref not in ACState.initial_params:
    #     ACState.initial_params[dataref] = value

    # запомнить текущее состояние ЛА
    ACState.curr_params[dataref] = value

    # NOTE!: maybe creating task for every param update is a bad idea
    if dataref in xp_mfi.sync_params:
        asyncio.create_task(xp_mfi.sync_param_to_slaves(dataref, value))

    # send to synoptic UI
    if dataref in synoptic_remote.sync_params:
        synoptic_remote.update(dataref, value)

    ACState.update_data_callbacks()


def on_data_exception(ex: Exception):
    print(traceback.format_exc())


def on_new_xp_data_udp(received_vals):
    for param, value in received_vals.items():
        # запомнить текущее состояние ЛА
        ACState.curr_params[param] = value


def on_data_exception_udp(ex):
    print(traceback.format_exc())


async def load_default_sit():
    await util.load_sit("Output/situations/1.sit")


async def add_mfi_sync_list():
    await xp_mfi.add_sync_param(xp.Params["sim/cockpit/weapons/firing_rate"])
    await xp_mfi.add_sync_param(xp.Params["sim/custom/7x/lhinit"])
    await xp_mfi.add_sync_param(xp.Params["sim/custom/7x/rhinit"])


def add_remote_synoptic_ui_sync_list():
    # synoptic_remote.add_sync_param(xp.Params["sim/cockpit2/engine/indicators/N1_percent[0]"])
    synoptic_remote.add_sync_param(xp.Params["sim/cockpit2/engine/actuators/throttle_ratio"])


async def main_loop():
    ACState.clear_all()

    await util.subscribe_to_time_param() # we need time param to load situation correctly 

    # await load_default_sit()

    await xp.set_param(xp.Params["sim/operation/override/override_joystick"], 1)

    await Scenario.clear_all()
    await ACSystems.reset()
    ACState.clear_all()

    await CockpitPanel.reset_to_default_state()

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

    
async def connect_to_mfi():
    await xp_mfi.xp_mfi.connect_until_success(MFI_XP_HOST, XP_MASTER_PORT, None, None)
    xp_mfi.param_subscriber.run_subsriber_task()


async def main():
    # await Scenario.run_scenario_task(("ABNORMAL", "ICE AND RAIN PROTECTION", "A/I: STALL WARNING OFFSET"), ACState)

    await op.run_receive_uso_task(USO_HOST, USO_RECEIVE_PORT)
    await op.run_send_uso_task(USO_HOST, USO_SEND_PORT)

    await xp.xp_master_udp.connect(XP_MASTER_HOST, XP_MASTER_UDP_PORT, on_new_xp_data_udp, on_data_exception_udp)
    await xp.xp_master.connect_until_success(XP_MASTER_HOST, XP_MASTER_PORT, on_new_xp_data, on_data_exception)

    xp.param_subscriber.run_subsriber_task()
    xp.udp_param_subscriber.run_subsriber_task()

    # connection to mfi is optional
    asyncio.create_task(connect_to_mfi())
    await add_mfi_sync_list()

    # synoptic_remote.run_updater()
    add_remote_synoptic_ui_sync_list()

    await web_interface.run_server_task(WEB_INTERFACE_HOST, WB_INTERFACE_PORT)

    await main_loop()   


asyncio.run(main())
