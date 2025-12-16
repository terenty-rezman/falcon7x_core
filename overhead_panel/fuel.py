import asyncio
import time

from common.instrument_panel import add_to_panel, TwoStateButton, ThreeStateButton, FloatSwitch, DiscreteSwitch, NStateXPLongPressButton
import xplane.master as xp


@add_to_panel
class boost1(NStateXPLongPressButton):
    dataref: xp.Params = xp.Params["sim/custom/7x/fpump0"]
    states = [2, 0, 1]

    long_states_idxs = [1, 2]
    short_states_idxs = [0, 2]

    @classmethod
    async def set_state(cls, state):
        pass
        return await super().set_state(state)


@add_to_panel
class boost1_off(boost1):
    @classmethod
    def get_state(cls):
        return super().get_state() == 1


@add_to_panel
class boost1_stby(boost1):
    @classmethod
    def get_state(cls):
        return super().get_state() == 2


@add_to_panel
class xtk_left(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/7x/bt1f3"]


@add_to_panel
class xtk_right(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/7x/bt3f1"]


@add_to_panel
class boost3(NStateXPLongPressButton):
    dataref: xp.Params = xp.Params["sim/custom/7x/fpump2"]
    states = [2, 0, 1]

    long_states_idxs = [1, 2]
    short_states_idxs = [0, 2]

    @classmethod
    async def set_state(cls, state):
        pass
        return await super().set_state(state)


@add_to_panel
class boost3_off(boost3):
    @classmethod
    def get_state(cls):
        return super().get_state() == 1


@add_to_panel
class boost3_stby(boost3):
    @classmethod
    def get_state(cls):
        return super().get_state() == 2


@add_to_panel
class xtk_up_1(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/7x/bt1f2"]


@add_to_panel
class backup_13(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/7x/bk13"]


@add_to_panel
class xtk_up_2(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/7x/bt3f2"]


@add_to_panel
class xtk_down_1(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/7x/bt2f1"]


@add_to_panel
class boost2(NStateXPLongPressButton):
    dataref: xp.Params = xp.Params["sim/custom/7x/fpump1"]
    states = [2, 0, 1]

    long_states_idxs = [1, 2]
    short_states_idxs = [0, 2]

    @classmethod
    async def set_state(cls, state):
        pass
        return await super().set_state(state)


@add_to_panel
class boost2_off(boost2):
    @classmethod
    def get_state(cls):
        return super().get_state() == 1


@add_to_panel
class boost2_stby(boost2):
    @classmethod
    def get_state(cls):
        return super().get_state() == 2


@add_to_panel
class xtk_down_2(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/7x/bt2f3"]


@add_to_panel
class xbp_12(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/weapons/mis_thrust3"]
    index = 21


@add_to_panel
class xbp_13(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/weapons/mis_thrust3"]
    index = 22


@add_to_panel
class xbp_23(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/weapons/mis_thrust3"]
    index = 23
