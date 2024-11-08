
import asyncio
import time

from instrument_panel import add_to_panel, TwoStateButton, ThreeStateButton, FloatSwitch, DiscreteSwitch, FloatStepper
import xplane as xp


@add_to_panel
class aft_temp(FloatStepper):
    dataref: xp.Params = xp.Params["sim/weapons/mis_thrust2"]
    index = 9

    logic_left = 0
    logic_right = 1

    left_most_value = 0 
    right_most_value = -3 

    state = 0
    step = 0.01

    val_type = float


@add_to_panel
class fwd_temp(FloatStepper):
    dataref: xp.Params = xp.Params["sim/weapons/mis_thrust2"]
    index = 10

    logic_left = 0
    logic_right = 1

    float_left_most_value = 0
    float_right_most_value = -3

    state = 0
    step = 0.01

    val_type = float


@add_to_panel
class fwd_temp_push(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/weapons/mis_thrust2"]
    index = 12


@add_to_panel
class crew_temp(FloatStepper):
    dataref: xp.Params = xp.Params["sim/weapons/mis_thrust2"]
    index = 11

    float_left_most_value = 0
    float_right_most_value = -3

    logic_left = 0
    logic_right = 1

    state = 0
    step = 0.01

    val_type = float


@add_to_panel
class crew_temp_push(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/weapons/mis_thrust2"]
    index = 14


@add_to_panel
class crew_ratio(FloatStepper):
    dataref: xp.Params = xp.Params["sim/weapons/mis_thrust3"]
    index = 20
    float_left_most_value = 0
    float_right_most_value = -3

    logic_left = 0
    logic_right = 1

    state = 0
    step = 0.01

    val_type = float


@add_to_panel
class gnd_vent(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/weapons/mis_thrust3"]
    index = 0
    states = [1, 0]


@add_to_panel
class pack(DiscreteSwitch):
    dataref: xp.Params = xp.Params["sim/weapons/target_index"]
    index = 0
    states = [1, 2, 3, 4, 0]


@add_to_panel
class pack_crew_off(pack):
    @classmethod
    async def set_state(cls, state):
        if state == 1:
            return await super().set_state(1)


@add_to_panel
class pack_normal(pack):
    @classmethod
    async def set_state(cls, state):
        if state == 1:
            return await super().set_state(0)


@add_to_panel
class pack_backup(pack):
    @classmethod
    async def set_state(cls, state):
        if state == 1:
            return await super().set_state(2)


@add_to_panel
class pack_emerg(pack):
    @classmethod
    async def set_state(cls, state):
        if state == 1:
            return await super().set_state(3)


@add_to_panel
class pack_pax_off(pack):
    @classmethod
    async def set_state(cls, state):
        if state == 1:
            return await super().set_state(4)


@add_to_panel
class bag_isol(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/weapons/mis_thrust2"]
    index = 8


@add_to_panel
class xbleed_ecs(ThreeStateButton):
    dataref: xp.Params = xp.Params["sim/weapons/mis_thrust2"]
    index = 20
    states = [2, 0, 1]

    @classmethod
    def get_indication(cls):
        state = super().get_state()
        if state == 0:
            return 0
        if state == 1:
            return 2
        if state == 2:
            return 1


@add_to_panel
class xbleed_ecs_on(xbleed_ecs):
    @classmethod
    def get_state(cls):
        return xbleed_ecs.get_state() == 2


@add_to_panel
class xbleed_ecs_off(xbleed_ecs):
    @classmethod
    def get_state(cls):
        return xbleed_ecs.get_state() == 1
