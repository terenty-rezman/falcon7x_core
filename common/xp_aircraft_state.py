from typing import List
import time
import traceback

from dataclasses import dataclass
from asyncio import Future
from typing import Callable, Optional, Any
from collections import defaultdict

from xplane.params import Params


@dataclass
class DataCallback:
    callback: Callable[["ACState"], None]
    future: Future


class ACState:
    # initial values of xplane params
    initial_params = {}

    # current values of xplane params
    curr_params = {}

    # when any of params value updated
    data_updated = False

    _data_callbacks: list[DataCallback] = []

    enabled_overrides = defaultdict(int)

    @classmethod
    def clear_all(cls):
        cls.curr_params = {}
        cls.initial_params = {}
        cls._data_callbacks = []

    # TODO: add reset method to cancel all pending tasks !!! 
    # or do i need to clear _data_callbacks only?

    @classmethod
    def update_data_callbacks(cls):
        # exit if callbacks list is empty
        if not cls._data_callbacks:
            return 

        # call each callback
        for c in cls._data_callbacks:
            # if callback returs true its finished
            if c.callback(cls):
                try:
                    c.future.set_result(None)
                except Exception as e:
                    traceback.print_exception(type(e), e, e.__traceback__)

        # remove finished callbacks
        cls._data_callbacks[:] = [c for c in cls._data_callbacks if c.future.done() == False]

    @classmethod
    def data_condition(cls, callback: Callable[["ACState"], bool]):
        f = Future()
        cls._data_callbacks.append(
            DataCallback(
                callback, f
            )
        )
        return f
    
    @classmethod
    def wait_until_parameter_condition(cls, xp_param: Params, condition: Callable[["ACState"], bool], timeout=None):
        start_time = time.time()

        def param_condition(ac_state: ACState):
            if timeout:
                if time.time() - start_time > timeout:
                    return True

            if not ac_state.param_available(xp_param):
                return False

            if condition(ac_state.curr_params[xp_param]):
                return True
        
        return cls.data_condition(param_condition)

    @classmethod
    def param_available(cls, xp_param: Params) -> bool:
        return xp_param in cls.curr_params
    
    @classmethod 
    def get_curr_param(cls, xp_param: Params) -> Optional[Any]:
        return cls.curr_params.get(xp_param)

    @classmethod
    def set_curr_param(cls, xp_param: Params, value):
        cls.curr_params[xp_param] = value
        cls.data_updated = True
    
    @classmethod
    def wait_until_param_available(cls, xp_param: Params):
        def param_available(ac_state: ACState):
            if ac_state.param_available(xp_param):
                return True
        
        return cls.data_condition(param_available)

    @classmethod
    def enable_param_overrides(cls, params_list: List[Params]):
        for p in params_list:
            cls.enabled_overrides[p] += 1

    @classmethod
    def disable_param_overrides(cls, params_list: List[Params]):
        for p in params_list:
            cls.enabled_overrides[p] -= 1

        for p, count in list(cls.enabled_overrides.items()):
            if count <= 0:
                del cls.enabled_overrides[p]

