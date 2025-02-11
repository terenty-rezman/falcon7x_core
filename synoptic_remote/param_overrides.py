"""""
drefs that can be overriden by core logic and sent to qml synoptic
"""

from typing import List
from xplane.params import Params
import synoptic_remote.synoptic_connection as synoptic_connection


overrides_values = dict()

enabled_overrides = set()


async def enable_param_overrides(params_list: List[Params]):
    global enabled_overrides
    enabled_overrides |= set(params_list)

    params_list = [str(p) for p in params_list]

    await synoptic_connection.enable_param_overrides(params_list)


async def disable_param_overrides(params_list: List[Params]):
    global enabled_overrides
    enabled_overrides -= set(params_list)

    params_list = [str(p) for p in params_list]

    await synoptic_connection.disable_param_overrides(params_list)


def set_override_param(param: Params, value):
    global overrides_values

    if param in enabled_overrides:
        overrides_values[str(param)] = value
    else:
        raise Exception(f"param {param} is not enabled for override!")


def clear_override_values():
    global overrides_values
    overrides_values = dict()
