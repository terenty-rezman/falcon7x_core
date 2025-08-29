from typing import List
from enum import StrEnum

import httpx

import xplane.params


class Sound(StrEnum):
    GONG = "gong"


async def play_sound(sound_id: Sound, volume=1.0, looped=False):
    params = {
        "name": str(sound_id),
        "volume": volume,
        "looped": looped
    }

    await _make_post_to_soundplayer(
        "/api/play_sound", params, 
        Settings.SOUNDPLAYER_HOST, 
        Settings.SOUNDPLAYER_PORT
    )


async def stop_sound(sound_id: Sound):
    params = {
        "name": str(sound_id),
    }

    await _make_post_to_soundplayer(
        "/api/stop_sound", params, 
        Settings.SOUNDPLAYER_HOST, 
        Settings.SOUNDPLAYER_PORT
    )


async def stop_all_sounds():
    await _make_post_to_soundplayer(
        "/api/stop_all_sounds", {}, 
        Settings.SOUNDPLAYER_HOST, 
        Settings.SOUNDPLAYER_PORT
    )


class Settings:
    SOUNDPLAYER_HOST = "127.0.0.1"

    # qml synoptic port
    SOUNDPLAYER_PORT = 4455


client = httpx.AsyncClient()


async def _make_post_to_soundplayer(path, json: dict, host: str, port: int):
    try:
        cas_url = f"http://{host}:{port}"
        await client.post(cas_url + path, json=json)
    except httpx.HTTPError as e:
        print("SoundPlayer Exception:", type(e).__name__, "–", e) 
