import asyncio
from time import time, ctime

from xplane.connection import XPconnection, XPconnectionUDP
from xplane.params import Params
from xplane.params_to_subscribe import to_subscribe
import common.sane_tasks as sane_tasks


class ParamsSubscriberTCP:
    def __init__(self) -> None:
        self.to_subscribe = asyncio.Queue()
        self.xp_connection: XPconnection = None
        self.terminate_task = False
    
    async def subscribe(self, param: Params, freq=None):
        await self.to_subscribe.put((param, freq))
    
    def run_subsriber_task(self):
        sane_tasks.spawn(self._subscriber_task())
    
    async def _subscriber_task(self):
        while not self.terminate_task:
            param, freq = await self.to_subscribe.get()
            if self.xp_connection:
                try:
                    if freq:
                        await self.xp_connection.send_string(f"sub {param} {freq}")
                    else:
                        await self.xp_connection.send_string(f"sub {param}")
                except Exception as e:
                    print(e)

                    # subscription failed put job back
                    await self.to_subscribe.put(param)
                    await asyncio.sleep(0.5)


class ParamSubscriberUDP:
    def __init__(self) -> None:
        self.to_subscribe = asyncio.Queue()
        self.xp_udp: XPconnectionUDP = None
        self.terminate_task = False
        self.subscribed_once = False # subscribe at least once

    def run_subsriber_task(self):
        sane_tasks.spawn(self._subscriber_task())
    
    async def _subscriber_task(self):
        while not self.terminate_task:
            now = time()
            if not self.xp_udp.last_packet_received_time or \
                now - self.xp_udp.last_packet_received_time > 4 or \
                self.subscribed_once == False:
                
                print("connecting to native xplane udp...")
                for p, freq, proto, in to_subscribe:
                    if proto == "udp":
                        self.xp_udp.subscribe_to_param(p, freq)

                if self.xp_udp.last_packet_received_time is not None and \
                    now - self.xp_udp.last_packet_received_time < 4:
                    self.subscribed_once = True
                    
            await asyncio.sleep(2)
