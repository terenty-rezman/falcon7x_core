import timeit
import asyncio
from enum import Enum 
import traceback

from common.xp_aircraft_state import ACState
from aircraft_systems.aircraft_systems import Systems as ACSystems

from common.joystick import Joystick
from common.scenario import Scenario

import xplane.master as xp
import xplane.mfi as xp_mfi

from common.instrument_panel import CockpitPanel
import common.instrument_panel as op
import common.util as util
import common.web_interface as web_interface
import common.simulation as simulation
from cas import cas
import synoptic_remote.synoptic as synoptic_remote
from common import sane_tasks
import common.send_to_autothrottle as auto_throttle_send

import settings


USE_JOYSTICK = False
if USE_JOYSTICK:
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
    if dataref not in ACState.enabled_overrides:
        ACState.curr_params[dataref] = value

    # NOTE!: maybe creating task for every param update is a bad idea
    if dataref in xp_mfi.sync_params:
        asyncio.create_task(xp_mfi.sync_param_to_slaves(dataref, value))

    # send to synoptic qml UI
    if dataref in synoptic_remote.sync_params and \
        dataref not in synoptic_remote.param_overrides.enabled_overrides: # synoptic_remote.update() will send overrides instead of xplane data ref value
        synoptic_remote.update(dataref, value)

    ACState.update_data_callbacks()
    ACSystems.update()
    # print(dataref, value)


async def ac_state_callback_task():
    while True:
        if ACState.data_updated:
            ACState.update_data_callbacks()
            ACState.data_updated = False

            ACSystems.update()

        await asyncio.sleep(0.1)


def on_data_exception(ex: Exception):
    print(traceback.format_exc())


def on_new_xp_data_udp(received_vals):
    for param, value in received_vals.items():
        # запомнить текущее состояние ЛА
        if param not in ACState.enabled_overrides:
            ACState.curr_params[param] = value

    ACState.data_updated = True


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
    # synoptic_remote.add_sync_param(xp.Params["sim/cockpit2/engine/actuators/throttle_ratio"])
    pass


async def main_loop():
    ACState.clear_all()

    # await util.subscribe_to_time_param() # we need time param to load situation correctly 

    # await load_default_sit()

    await xp.set_param(xp.Params["sim/operation/override/override_joystick"], 1)
    await xp.set_param(xp.Params["sim/operation/override/override_gearbrake"], 1)

    await Scenario.kill_current_scenario()
    await ACSystems.reset()
    ACState.clear_all()

    await CockpitPanel.reset_to_default_state()

    # await Scenario.run_scenario_task(("EMERGENCY", "ELECTRICAL POWER", "36 ELEC: LH+RH ESS PWR LO"), ACState)
    # await Scenario.run_scenario_task(("TEST", "TEST", "test_scenario_1"), ACState)

    import common.plane_control as pc

    while True:
        # x, y, z, rz = joystick.get_axes_values()
        # if joystick.is_plugged():
        #     await xp.set_param(xp.Params["sim/joystick/yoke_roll_ratio"], x)
        #     await xp.set_param(xp.Params["sim/joystick/yoke_pitch_ratio"], -y)
        #     await xp.set_param(xp.Params["sim/joystick/yoke_heading_ratio"], rz - z)

        await asyncio.sleep(0.1)

    
async def connect_to_mfi():
    await xp_mfi.xp_mfi.connect_until_success(settings.MFI_XP_HOST, settings.XP_MASTER_PORT, None, None, 5)
    xp_mfi.param_subscriber.run_subsriber_task()


async def main():
    await web_interface.run_server_task(settings.WEB_INTERFACE_HOST, settings.WB_INTERFACE_PORT)

    sane_tasks.spawn(ac_state_callback_task())

    await xp.xp_master_udp.connect(settings.XP_MASTER_HOST, settings.XP_MASTER_UDP_PORT, on_new_xp_data_udp, on_data_exception_udp)
    await xp.xp_master.connect_until_success(settings.XP_MASTER_HOST, settings.XP_MASTER_PORT, on_new_xp_data, on_data_exception)

    await op.run_receive_uso_task(settings.USO_HOST, settings.USO_RECEIVE_PORT)
    await op.run_send_uso_task(settings.USO_HOST, settings.USO_SEND_PORT)

    simulation.run_time_update_task()

    xp.param_subscriber.run_subsriber_task()
    xp.udp_param_subscriber.run_subsriber_task()

    # connection to mfi is optional
    sane_tasks.spawn(connect_to_mfi())
    await add_mfi_sync_list()

    synoptic_remote.run_updater(ACState)
    add_remote_synoptic_ui_sync_list()

    await auto_throttle_send.run_send_to_autothrottle_task(settings.AUTO_THROTTLE_HOST, settings.AUTO_THROTTLE_PORT)

    await main_loop()   


asyncio.run(main())

# TODO: на перезапуске игры или сценария надо слать физическое состояние всех переключателей на иксплейн чтобы синхронизировать состояния физической
# кабины с виртуальной
