import asyncio

import xp_aircraft_state as xp_ac
import xplane as xp
import sane_tasks
import overhead_panel as op


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


class APUFireProtection(System):
    @classmethod
    async def start_condition(cls):
        if xp_ac.ACState.param_available(xp.Params["sim/operation/failures/rel_apu_fire"]):
            if xp_ac.ACState.curr_params[xp.Params["sim/operation/failures/rel_apu_fire"]] == 6:
                return True

    @classmethod
    async def system_logic_task(cls):
        await asyncio.sleep(2)

        # Apu fire protection system automatically closes apu fsov
        await xp.set_param(xp.Params["sim/cockpit/engine/APU_switch"], 1)

        # wait until user presses apu extinguisher button 
        await op.apu_disch.wait_state(1)

        await asyncio.sleep(2)

        # fire has been succesfully extinguished
        failure = xp.Params["sim/operation/failures/rel_apu_fire"]
        await xp.set_param(failure, 0)
        await xp_ac.ACState.wait_until_parameter_condition(failure, lambda p: p == 0)
