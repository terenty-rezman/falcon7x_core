from enum import IntEnum


class Sound(IntEnum):
    MUTE = 0
    GONG = 1


async def play_sound(sound_id: Sound):
    pass


async def stop_all_sounds():
    pass
