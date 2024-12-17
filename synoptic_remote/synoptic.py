import asyncio
import httpx

from cas.messages import *
from xplane.params import Params
import common.sane_tasks as sane_tasks


SYNOPTIC_HOST = "127.0.0.1"

# 2 instances of CAS for left & right pilots
SYNOPTIC_PORT = 8800


sync_params = set()

to_update = {}
_stop_updater = False


def add_sync_param(param: Params):
    sync_params.add(param)


async def _make_post_to_synoptic(path, json: dict, host: str, port: int):
    try:
        cas_url = f"http://{host}:{port}"
        async with httpx.AsyncClient() as client:
            await client.post(cas_url + path, json=json)
    except httpx.HTTPError as e:
        print("Synoptic Exception:", type(e).__name__, "–", e) 


def update(dataref, value):
    to_update[str(dataref)] = value


async def _updater():
    global to_update
    while not _stop_updater:
        if to_update:
            await _make_post_to_synoptic("/api/set_data", to_update, SYNOPTIC_HOST, SYNOPTIC_PORT)

            to_update = {}

        await asyncio.sleep(0.1)


def run_updater():
    sane_tasks.spawn(_updater())


def stop_updater():
    global stop_updater
    stop_updater = True
