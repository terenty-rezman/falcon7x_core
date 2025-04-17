import common.sane_tasks as sane_tasks
import asyncio
from common.util import in_sequence


class System:
    logic_task = None
    is_killing = False

    @classmethod
    def start_condition(cls):
        pass

    @classmethod
    def kill_condition(cls):
        pass

    @classmethod
    async def system_logic_task(cls):
        pass

    @classmethod
    async def killing_task(cls):
        pass

    @classmethod
    def update(cls):
        if cls.logic_task is None and cls.is_killing == False:
            if cls.start_condition():
                cls.logic_task = sane_tasks.spawn(cls.system_logic_task())    
                cls.logic_task.add_done_callback(cls.on_task_done)
        if cls.logic_task and cls.is_killing == False:
            if cls.kill_condition():
                cls.is_killing = True
                sane_tasks.spawn(in_sequence(cls.killing_task(), cls.reset()))
    
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
            cls.is_killing = False
