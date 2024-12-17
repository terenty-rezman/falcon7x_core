import common.sane_tasks as sane_tasks
import asyncio


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
        if cls.logic_task is None:
            if await cls.start_condition():
                cls.logic_task = sane_tasks.spawn(cls.system_logic_task())    
                cls.logic_task.add_done_callback(cls.on_task_done)
    
    @classmethod
    def on_task_done(cls, task_future):
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
