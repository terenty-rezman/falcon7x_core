import asyncio
import numpy as np

from common.aioudp import open_local_endpoint, open_remote_endpoint
import common.sane_tasks as sane_tasks

import common.plane_control as pc
from front_panel import autopilot as at


AUTOTHROTTLE_SEND_DELAY = 0.1

send_task = None

at_struct_dtype = np.dtype([
    ('xplane_throttle_1', 'f4'),
    ('xplane_throttle_2', 'f4'),
    ('xplane_throttle_3', 'f4'),
    ('uso_throttle_1', 'f4'),
    ('uso_throttle_2', 'f4'),
    ('uso_throttle_3', 'f4'),
    ('auto_throttle_enabled', 'f4'),
])

at_struct = np.zeros(1, dtype=at_struct_dtype)


async def run_send_to_autothrottle_task(at_host, at_send_port):
    remote = await open_remote_endpoint(at_host, port=at_send_port)

    global send_task
    send_task = sane_tasks.spawn(send_autothrottle_task(remote))    


async def send_autothrottle_task(remote):
    while True:
        at_struct["xplane_throttle_1"] = pc.pc_throttle_1.get_state() or 0 # [0; 10]
        at_struct["xplane_throttle_2"] = pc.pc_throttle_1.get_state() or 0 # [0; 10]
        at_struct["xplane_throttle_3"] = pc.pc_throttle_1.get_state() or 0 # [0; 10]
        at_struct["uso_throttle_1"] = pc.pc_throttle_1.get_uso_state() or 0 # [0; 10]
        at_struct["uso_throttle_2"] = pc.pc_throttle_1.get_uso_state() or 0 # [0; 10]
        at_struct["uso_throttle_3"] = pc.pc_throttle_1.get_uso_state() or 0 # [0; 10]
        at_struct["auto_throttle_enabled"] = at.fp_autothrottle.get_state() or 0 # [0; 10]

        remote.send(at_struct.tobytes())

        await asyncio.sleep(AUTOTHROTTLE_SEND_DELAY)
