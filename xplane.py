"""
Xplane parameters, failures & commands

ExtPlane plugin is used to communicate with xplane https://github.com/vranki/ExtPlane
"""

import asyncio
import json

from enum import Enum 

import sane_tasks


def to_str(self):
    return self.name


Params = Enum('XplaneParams', [
    "sim/time/total_running_time_sec",
    "sim/cockpit/electrical/night_vision_on",
    "sim/operation/override/override_joystick",
    "sim/joystick/yoke_pitch_ratio",
    "sim/joystick/yoke_roll_ratio",
    "sim/joystick/yoke_heading_ratio",
    "sim/flightmodel/position/elevation",
    "sim/weapons/warhead_type",
    "sim/cockpit2/engine/actuators/fire_extinguisher_on",
    "sim/cockpit2/annunciators/engine_fires",
    "sim/weapons/mis_thrust2",
    "sim/weapons/mis_thrust3",
    "sim/cockpit/engine/APU_switch",

    "sim/cockpit2/controls/speedbrake_ratio", # flight control - airbrake auto
    "sim/cockpit2/switches/artificial_stability_on", # fcs engage norm
    "sim/cockpit2/switches/yaw_damper_on", # fcs engage stby
    "sim/cockpit2/controls/nosewheel_steer_on", # fcs steering

    "sim/cockpit2/electrical/APU_generator_on", # apu master
    "sim/cockpit2/electrical/APU_N1_percent", # apu start stop
    "sim/cockpit2/electrical/APU_starter_switch", # apu start stop

    "sim/custom/7x/selecthyd", # backup pump hydraulics

    "sim/custom/7x/lhmaster", # dc supply - lh_master
    "sim/custom/7x/lhinit", # dc supply - lh init
    "sim/cockpit2/electrical/cross_tie", # dc supply - bus tie
    "sim/custom/7x/rhinit", # dc supply - rh init
    "sim/custom/7x/rhmaster", # dc supply - rh_master
    "sim/cockpit/electrical/gpu_on", # dc supply - ext power
    "sim/cockpit2/electrical/generator_on", # dc supply - gen 1
    "sim/custom/7x/lhisol", # dc supply - lh isol
    "sim/cockpit2/switches/ram_air_turbine_on", # dc supply - rat reset
    "sim/custom/7x/rhisol", # dc supply - rh isol
    "sim/cockpit2/electrical/battery_on", # dc supply - bat 1

    "sim/weapons/target_index", # air condition - pack
    "sim/custom/7x/fpump0", # fuel - boost1
    "sim/7x/bt1f3", # fuel - xtk 1
    "sim/7x/bt3f1", # fuel - xtk 2
    "sim/custom/7x/fpump2", # fuel - boost 3
    "sim/7x/bt1f2", # fuel - xtk 3
    "sim/7x/bt3f2", # fuel - xtk 4
    "sim/7x/bk13", # fuel - backup 1_3
    "sim/7x/bt2f1", # fuel - xtk 5
    "sim/custom/7x/fpump1", # fuel - boost2 
    "sim/7x/bt2f3", # fuel - xtk 6

    "sim/custom/7x/AIwingsel", # anti ice - wings
    "sim/cockpit2/ice/ice_inlet_heat_on_per_engine", # anti ice - eng 1
    "sim/custom/7x/AIengcentre", # anti ice - eng 2

    "sim/custom/7x/overAPUaction", # bleed - bleed apu
    "sim/cockpit2/pressurization/actuators/dump_to_altitude_on", 

    "sim/cockpit2/ice/ice_pitot_heat_on_pilot", # pitot heat - probe 12 
    "sim/cockpit2/ice/ice_pitot_heat_on_copilot", # pitot heat - probe 3
    "sim/cockpit2/ice/ice_AOA_heat_on", # pitot heat - probe 4
    "sim/cockpit2/ice/ice_AOA_heat_on_copilot", # windshield heat - lh
    "sim/cockpit2/ice/ice_window_heat_on", # windshield heat - rh
    "sim/cockpit2/ice/ice_auto_ignite_on", # windshield heat - backup

    "sim/custom/7x/lum1", # exterior lights - nav
    "sim/custom/7x/lum2", # exterior lights - anticol
    "sim/cockpit2/switches/spot_light_on", # exterior lights - wing
    "sim/cockpit2/switches/landing_lights_switch", # exterior lights - langing lh
    "sim/cockpit/electrical/taxi_light_on", # exterior lights - taxi

    "sim/cockpit2/switches/instrument_brightness_ratio", # exterior lights - overhead

    "sim/cockpit2/switches/generic_lights_switch", # interiorl lights - emerge lights
    "sim/cockpit2/switches/fasten_seat_belts", # interior lights - fasten belts
    "sim/cockpit2/switches/no_smoking", # interior lights - no smoking
    "sim/custom/7x/paxlum", # interior lights - cabin

    "sim/cockpit2/annunciators/master_warning", # front panel - master warning
    "sim/cockpit2/annunciators/plugin_master_warning", # front panel - master warning
    "sim/cockpit2/annunciators/master_caution",
    "sim/cockpit2/annunciators/plugin_master_caution",

    "sim/cockpit2/radios/actuators/com1_standby_frequency_hz_833", # front panel - vhf control lh
    "sim/cockpit2/gauges/actuators/barometer_setting_in_hg_pilot", # front panel - baro
    "sim/custom/7x/flydir", # front panel - FD/TD
    "sim/cockpit/radios/ap_src", # front panel - pilot side
    "sim/cockpit/autopilot/autopilot_mode", # front panel - autopilot on/off
    "sim/weapons/targ_h", # front panel - vs path
    "sim/cockpit2/autopilot/vvi_status", # front panel - vs mode
    "sim/cockpit2/autopilot/fms_vnav", #  front panel - vnav
    "sim/cockpit2/autopilot/altitude_dial_ft", # front panel - asel
    "sim/cockpit2/autopilot/altitude_hold_armed", # front panel - alt
    "sim/cockpit2/gauges/actuators/barometer_setting_in_hg_copilot", # secondary flight display - std
    "sim/multiplayer/controls/flap_request", # pedestal - wings config - slats/flats sf

    # Failures
    "sim/operation/failures/rel_engfir0", # engine 1 fire

    "sim/operation/failures/rel_engfir3", # fire rear comp
    "sim/operation/failures/rel_engfir4", # fire bag comp

    "sim/operation/failures/rel_engfla0",
    "sim/operation/failures/rel_apu_fire", # apu fire

    "sim/cockpit2/engine/indicators/N2_percent", # eng N2
    "sim/7x/choixtcas", # PDU show ENG TRM

    "sim/cockpit2/autopilot/airspeed_dial_kts_mach", # front panel - airspeed val
    "sim/cockpit/autopilot/airspeed_is_mach", # front panel - airspeed kts or mach
    "sim/cockpit2/autopilot/autothrottle_enabled", # front panel - AT auto throttle
    "sim/cockpit2/autopilot/approach_status", # front panel - approach
    "sim/cockpit2/autopilot/nav_status", # front panel - lnav  
    "sim/cockpit/autopilot/heading_mag", # fron panel - hdg/trk
    "sim/cockpit2/autopilot/heading_mode", # front panel - hdg/trk mode

    "sim/cockpit2/controls/left_brake_ratio", # pedal brake left
    "sim/cockpit2/controls/right_brake_ratio", # pedal brake right
    "sim/cockpit2/engine/actuators/throttle_ratio", # throttle

    "sim/cockpit/weapons/firing_rate", # synoptic page

    # our custom datarefs
    "sim/custom/7x/z_eng1_oil_press_override", # custom eng1 oil pressure
    "sim/custom/7x/z_eng1_oil_press", # custom eng1 oil pressure
])
Params.__str__ = to_str


Commands = Enum('XplaneCommands', [
    "sim/operation/toggle_main_menu",
    "sim/view/forward_with_nothing", # 1st person camera with nothing
    "sim/operation/reload_aircraft",
    "sim/operation/fix_all_systems",
    "sim/electrical/APU_start",
    "sim/electrical/APU_off",
    "sim/bleed_air/bleed_air_left", # bleed - bleed 1
    "sim/bleed_air/bleed_air_auto", # bleed - bleed 2
    "sim/bleed_air/bleed_air_right", # bleed - bleed 3
    "sim/pressurization/vvi_down", # pressurization - cabin alt
    "sim/pressurization/vvi_up", # pressurization - cabin alt
    "sim/annunciator/clear_master_warning", # front panel - master warning
    "sim/annunciator/clear_master_caution", # front panel - master caution
    "sim/autopilot/knots_mach_toggle", # front panel - speed mach or kts 
    "sim/autopilot/autothrottle_toggle", # front panel - auto throttle
    "sim/autopilot/approach", # front panel - change approach mode
    "sim/autopilot/NAV", # front panel - lnav
    "sim/autopilot/heading_sync", # front panel - hdg trk sync
    "sim/autopilot/heading", # front panel - hdg trk mode
    "sim/autopilot/vertical_speed", # front panel - vs mode
    "sim/autopilot/FMS", # front panel - vs mode
    "sim/autopilot/altitude_hold", # front panel - alt
])

Commands.__str__ = to_str


xp_writer = None
xp_reader = None
xp_reader_task = None
on_new_xp_data_callback = None
on_new_xp_data_exception_callback = None
terminate_reader_task = False


async def send_string(writer, msg: str):
    if not writer:
        print("not connected to xplane!")
        return 

    msg += "\n"
    writer.write(msg.encode())
    await writer.drain()
    await asyncio.sleep(0) # NOTE: needed to call event loop !


async def subscribe_to_param(param: Params):
    await send_string(xp_writer, f"sub {param}")


async def set_param(param: Params, value):
    await send_string(xp_writer, f"set {param} {value}")


async def get_param(param: Params):
    """ получить актуальное значения параметра """
    await send_string(xp_writer, f"upd {param}")


async def load_sit(name):
    await send_string(xp_writer, f"sit {name}")


async def run_command_once(cmd):
    await send_string(xp_writer, f"cmd once {cmd}")

async def begin_command(cmd):
    await send_string(xp_writer, f"cmd begin {cmd}")

async def end_command(cmd):
    await send_string(xp_writer, f"cmd end {cmd}")

async def read_line(reader) -> str:
    return await reader.readline()


def parse_xplane_dataref(data_line: str):
    type, dataref, value = data_line.split()
    type = type.decode()
    dataref = dataref.decode()

    if type == "ui":
        value = int(value) 
    elif type in ["uf", "ud"]:
        value = float(value)
    elif type in ["uia", "ufa"]:
        value = value.decode()
        value = json.loads(value)
    else:
        print("Warning: dataref parse not INPLEMENTED!")
    
    return type, dataref, value
    

async def handle_read():
    global terminate_reader_task
    global on_new_xp_data_callback
    global xp_reader

    try:
        # read first 3 welcome lines
        l = await read_line(xp_reader)
        l = await read_line(xp_reader)
        l = await read_line(xp_reader)

        while not terminate_reader_task:
            data = await read_line(xp_reader)
            type, dataref, value = parse_xplane_dataref(data)

            if on_new_xp_data_callback:
                on_new_xp_data_callback(type, dataref, value) 
    except Exception as ex:
        print(data)
        on_new_xp_data_exception_callback(ex)


async def disconnect():
    global terminate_reader_task
    global xp_reader_task

    if xp_writer:
        xp_writer.close()
        await xp_writer.wait_closed()

    if xp_reader_task:
        terminate_reader_task = True
        await xp_reader_task
        terminate_reader_task = False
    

async def connect_to_xplane_until_success(server_address, server_port, on_new_data_callback, on_data_exception_callback):
    while True:
        try:
            await connect_to_xplane(server_address, server_port, on_new_data_callback, on_data_exception_callback)
            print(f"connected to xplane: {server_address}:{server_port} !")
            break
        except ConnectionRefusedError:
            print(f"Could not connect to xplane: {server_address}:{server_port} !")
            print(f"retrying...")
            asyncio.sleep(0.5)


async def connect_to_xplane_once(server_address, server_port, on_new_data_callback, on_data_exception_callback):
    try:
        await connect_to_xplane(server_address, server_port, on_new_data_callback, on_data_exception_callback)
        print(f"connected to xplane: {server_address}:{server_port} !")
    except ConnectionRefusedError:
        print(f"Could not connect to xplane: {server_address}:{server_port} !")


async def connect_to_xplane(server_address, server_port, on_new_data_callback, on_data_exception_callback):
    """ connect to ExtPlane plugin """

    global xp_writer
    global xp_reader
    global xp_reader_task
    global on_new_xp_data_callback
    global on_new_xp_data_exception_callback 

    await disconnect()

    on_new_xp_data_callback = on_new_data_callback
    on_new_xp_data_exception_callback = on_data_exception_callback
    xp_reader, xp_writer = await asyncio.open_connection(server_address, server_port)

    xp_reader_task = sane_tasks.spawn(handle_read())    
