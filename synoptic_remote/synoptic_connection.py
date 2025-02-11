from typing import List

import httpx

import xplane.params


class Settings:
    QML_SYNOPTIC_HOST = "127.0.0.1"

    # qml synoptic port
    QML_SYNOPTIC_PORT = 8800

    # send refs to qml delay
    SEND_DELAY = 0.1 # sec


client = httpx.AsyncClient()


async def _make_post_to_synoptic(path, json: dict, host: str, port: int):
    try:
        cas_url = f"http://{host}:{port}"
        await client.post(cas_url + path, json=json)
    except httpx.HTTPError as e:
        print("Synoptic Exception:", type(e).__name__, "–", e) 


async def set_data(data: dict, overrides: dict):
    all_data = dict()

    if data:
        all_data["data"] = data
    
    if overrides:
        all_data["overrides"] = overrides

    await _make_post_to_synoptic(
        "/api/set_data", all_data, 
        Settings.QML_SYNOPTIC_HOST, 
        Settings.QML_SYNOPTIC_PORT
    )


async def enable_param_overrides(params: List[xplane.params.Params]):
    await _make_post_to_synoptic(
        "/api/enable_param_overrides", params, 
        Settings.QML_SYNOPTIC_HOST, 
        Settings.QML_SYNOPTIC_PORT
    )


async def disable_param_overrides(params: List[xplane.params.Params]):
    await _make_post_to_synoptic(
        "/api/disable_param_overrides", params, 
        Settings.QML_SYNOPTIC_HOST, 
        Settings.QML_SYNOPTIC_PORT
    )
