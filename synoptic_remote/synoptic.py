import asyncio
import time

from cas.messages import *
from xplane.params import Params
import common.sane_tasks as sane_tasks

import synoptic_remote.synoptic_connection as synoptic_connection
import synoptic_remote.param_overrides as param_overrides


sync_params = set()

to_update = {}
_stop_updater = False


def add_sync_param(param: Params):
    sync_params.add(param)


def update(dataref, value):
    to_update[str(dataref)] = value


async def _updater(ac_state):
    started = time.time()
    global to_update
    while not _stop_updater:
        if to_update or param_overrides.overrides_values:
            await synoptic_connection.set_data(to_update, param_overrides.overrides_values)

            to_update = {}
            param_overrides.clear_override_values()

            elapsed = time.time() - started
            if elapsed > 2:
                params_list = [str(p) for p in ac_state.enabled_overrides]
                await synoptic_connection.enable_param_overrides(params_list)
                started = time.time()

        await asyncio.sleep(synoptic_connection.Settings.SEND_DELAY)


def run_updater(ac_state):
    sane_tasks.spawn(_updater(ac_state))


def stop_updater():
    global stop_updater
    stop_updater = True
