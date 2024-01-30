from dataclasses import dataclass
from asyncio import Future


@dataclass
class DataCallback:
    callback: callable
    future: Future


class ACState:
    curr_xplane_state = {}
    initial_xplane_state = {}

    _data_callbacks: list[DataCallback] = []

    @classmethod
    def clear_all(cls):
        cls.curr_xplane_state = {}
        cls.initial_xplane_state = {}
        cls._data_callbacks = []


    @classmethod
    def update_data_callbacks(cls):
        # exit if callbacks list is empty
        if not cls._data_callbacks:
            return 

        # call each callback
        for c in cls._data_callbacks:
            # if callback returs true its finished
            if c.callback(cls):
                c.future.set_result(None)

        # remove finished callbacks
        cls._data_callbacks[:] = [c for c in cls._data_callbacks if c.future.done() == False]
            

    @classmethod
    def data_condition(cls, callback):
        f = Future()
        cls._data_callbacks.append(
            DataCallback(
                callback, f
            )
        )
        return f
    
    @classmethod
    def param_available(cls, param_name: str) -> bool:
        return param_name in cls.curr_xplane_state
    
    @classmethod
    async def wait_until_param_available(cls, param_name: str):
        def param_available(ac_state: ACState):
            if ac_state.param_available("sim/time/total_running_time_sec"):
                return True
        
        await cls.data_condition(param_available)



