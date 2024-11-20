"""""
Xplane parameters, failures & commands

ExtPlane plugin is used to communicate with xplane https://github.com/vranki/ExtPlane
"""

from xp_aircraft_state import ACState
from xplane.connection import XPconnection
from xplane.params import Params


xp_master = XPconnection()


async def subscribe_to_param(param: Params):
    await xp_master.send_string(f"sub {param}")


async def set_param(param: Params, value):
    await xp_master.send_string(f"set {param} {value}")


async def get_param(param: Params):
    """ получить актуальное значения параметра """
    await xp_master.send_string(f"upd {param}")


async def load_sit(name):
    await xp_master.send_string(f"sit {name}")


async def run_command_once(cmd):
    await xp_master.send_string(f"cmd once {cmd}")


async def begin_command(cmd):
    await xp_master.send_string(f"cmd begin {cmd}")


async def end_command(cmd):
    await xp_master.send_string(f"cmd end {cmd}")


async def subscribe_to_all_data():
    for p in Params:
        await subscribe_to_param(p)

    await ACState.wait_until_param_available(Params["sim/time/total_running_time_sec"])
