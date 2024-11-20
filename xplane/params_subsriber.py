import asyncio

from xplane.connection import XPconnection
from xplane.params import Params
import sane_tasks


class ParamsSubscriber:
    def __init__(self) -> None:
        self.to_subscribe = asyncio.Queue()
        self.xp_connection: XPconnection = None
        self.temrminate_task = False
    
    async def subscribe(self, param: Params):
        await self.to_subscribe.put(param)
    
    def run_subsriber_task(self):
        asyncio.create_task(self._subscriber_task())
    
    async def _subscriber_task(self):
        while not self.temrminate_task:
            param = await self.to_subscribe.get()
            if self.xp_connection:
                try:
                    await self.xp_connection.send_string(f"sub {param}")
                except Exception as e:
                    print(e)

                    # subscription failed put job back
                    self.to_subscribe.put(param)
                    await asyncio.sleep(0.5)
