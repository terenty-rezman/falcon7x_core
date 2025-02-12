"""""
Xplane parameters, failures & commands

ExtPlane plugin is used to communicate with xplane https://github.com/vranki/ExtPlane
"""

from common.xp_aircraft_state import ACState
from xplane.connection import XPconnection, XPconnectionUDP
from xplane.params import Params
from xplane.params_subsriber import ParamsSubscriberTCP, ParamSubscriberUDP
from xplane.params_to_subscribe import Subscribe
import common.sane_tasks as sane_tasks


async def subscribe_to_all_tcp_params():
    for p, freq, proto, in Subscribe.to_subscribe:
        if proto == "tcp":
            await subscribe_to_param(p, freq)
        elif proto == "udp":
            continue
        else:
            raise Exception(f"unknown protocol {proto} for param to subscribe !")

    # await ACState.wait_until_param_available(Params["sim/time/total_running_time_sec"])


async def resubscribe_to_tcp_param(param):
    await subscribe_to_param(param)


xp_master = XPconnection()
xp_master.on_connected_callback = lambda: sane_tasks.spawn(subscribe_to_all_tcp_params())
xp_master.on_subscription_failed_callback = resubscribe_to_tcp_param 

param_subscriber = ParamsSubscriberTCP()
param_subscriber.xp_connection = xp_master


xp_master_udp = XPconnectionUDP()
udp_param_subscriber = ParamSubscriberUDP() 
udp_param_subscriber.xp_udp = xp_master_udp


async def subscribe_to_param(param: Params, freq=None):
    await param_subscriber.subscribe(param, freq)


async def set_param(param: Params, value):
    if param in Subscribe.udp_params_set:
        xp_master_udp.set_param(param, value)
    else:
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


def set_subscribe_params(params):
    Subscribe.set_subscribe_params(params)
