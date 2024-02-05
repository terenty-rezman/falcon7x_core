import asyncio

from xp_aircraft_state import ACState as xpACState


class System:
    logic_task = None

    @classmethod
    async def start_condition(cls):
        pass

    @classmethod
    async def system_logic_task(cls):
        pass


    @classmethod
    async def update(cls):
        if await cls.start_condition():
            cls.logic_task = asyncio.create_task(cls.system_logic_task())    
            cls.logic_task.add_done_callback(cls.on_task_done)
    
    @classmethod
    def on_task_done(cls):
        cls.logic_task = None
    
    @classmethod
    async def reset(cls):
        if cls.logic_task:
            cls.logic_task.cancel()
            try:
                await cls.logic_task
            except asyncio.CancelledError:
                print(f"{cls.__name__} logic task stopped")
                cls.logic_task = None


class APUFireProtection(System):
    @classmethod
    async def start_condition(cls):
        return False

    @classmethod
    async def system_logic_task(cls):
        pass
