"""
Xplane parameters, failures & commands
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

    # Failures
    "sim/operation/failures/rel_engfir0", # engine 1 fire

    "sim/operation/failures/rel_engfir3", # fire rear comp
    "sim/operation/failures/rel_engfir4", # fire bag comp

    "sim/operation/failures/rel_engfla0",
    "sim/operation/failures/rel_apu_fire", # apu fire
])
Params.__str__ = to_str


Commands = Enum('XplaneCommands', [
    "sim/operation/toggle_main_menu",
    "sim/view/forward_with_nothing", # 1st person camera with nothing
    "sim/operation/reload_aircraft",
    "sim/operation/fix_all_systems",
    "sim/electrical/APU_start",
    "sim/electrical/APU_off",
])
Commands.__str__ = to_str


xp_writer = None
xp_reader = None
xp_reader_task = None
on_new_xp_data_callback = None
on_new_xp_data_exception_callback = None
terminate_reader_task = False


async def send_string(writer, msg: str):
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


async def connect_to_xplane(server_address, server_port, on_new_data_callback, on_data_exception_callback):
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
