"""""
connection to xplane copy used as mfi
"""

from xplane.connection import XPconnection
from xplane.params import Params


xp_mfi = XPconnection()

sync_params = set()
subsribed_params = set()


def add_sync_param(param: Params):
    sync_params.add(param)


def remove_sync_param(param: Params):
    sync_params.remove(param)


async def sync_param(param: Params, value):
    if param not in subsribed_params:
        await xp_mfi.send_string(f"sub {param}")
        subsribed_params.add(param)
        # NOTE: need a way to unsubscribe!

    await xp_mfi.send_string(f"set {param} {value}")


async def sync_param_to_slaves(param: Params, value):
    await sync_param(param, value)
