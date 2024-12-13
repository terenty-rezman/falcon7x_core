"""""
connection to xplane copy used as mfi
"""

from xplane.connection import XPconnection
from xplane.params import Params
from xplane.params_subsriber import ParamsSubscriberTCP
import sane_tasks


sync_params = set()


async def resubscribe_to_param(param):
    await param_subscriber.subscribe(param)


async def subscribe_to_all_sync_params():
    for p in sync_params:
        await param_subscriber.subscribe(p) 


xp_mfi = XPconnection()
xp_mfi.on_subscription_failed_callback = resubscribe_to_param 
xp_mfi.on_connected_callback = lambda: sane_tasks.spawn(subscribe_to_all_sync_params())

xp_master = XPconnection()

param_subscriber = ParamsSubscriberTCP()
param_subscriber.xp_connection = xp_mfi


async def add_sync_param(param: Params):
    sync_params.add(param)
    await param_subscriber.subscribe(param)


def remove_sync_param(param: Params):
    sync_params.remove(param)


async def sync_param(param: Params, value):
    await xp_mfi.send_string(f"set {param} {value}")


async def sync_param_to_slaves(param: Params, value):
    await sync_param(param, value)
