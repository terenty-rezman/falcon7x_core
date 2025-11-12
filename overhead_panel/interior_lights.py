import asyncio
import time

from common.instrument_panel import add_to_panel, TwoStateButton, ThreeStateButton, FloatSwitch, DiscreteSwitch, PushButton
import xplane.master as xp
import common.xp_aircraft_state as xp_ac
import common.util as util


@add_to_panel
class il_emerge_lights(DiscreteSwitch):
    dataref: xp.Params = xp.Params["sim/weapons/warhead_type"]
    states = [2, 1, 0, 3]
    index = 7

    off_digit = 0
    arm_digit = 0

    @classmethod
    def get_state(cls):
        state = super().get_state()

        if state is None:
            return

        if state > 2:
            return 2

        return state

    @classmethod
    async def set_state(cls, state):
        if state is None:
            if cls.arm_digit == 1 and cls.off_digit == 0:
                state = 0
            if cls.arm_digit == 0 and cls.off_digit == 1:
                state = 2
            else:
                state = 1

        if state > 2:
            state = 0

        await super().set_state(state)

    @classmethod
    async def click(cls):
        state = cls.get_state()
        if state is None:
            return

        if state > 2:
            await cls.set_state(0) 
        else:
            await cls.set_state(state)

    @classmethod
    def get_indication(cls):
        if cls.override_indication is not None:
            return cls.override_indication

        param = xp_ac.ACState.get_curr_param(xp.Params["sim/cockpit2/switches/generic_lights_switch"])
        if param is None:
            return 0
        
        param = param[0]
        return param


@add_to_panel
class il_emerge_lights_arm():
    @classmethod
    async def set_state(cls, state):
        il_emerge_lights.arm_digit = state
        await il_emerge_lights.set_state(None)


@add_to_panel
class il_emerge_lights_off():
    @classmethod
    async def set_state(cls, state):
        il_emerge_lights.off_digit = state
        await il_emerge_lights.set_state(None)


# @add_to_panel
# class il_emerge_lights_on(il_emerge_lights):
#     @classmethod
#     async def set_state(cls, state):
#         if state == 1:
#             await super().set_state(1)

#     @classmethod
#     def get_indication(cls):
#         if cls.override_indication is not None:
#             return cls.override_indication

#         state = cls.get_state()
#         if state == 1:
#             return 1

#         return 0


@add_to_panel
class il_fasten(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/cockpit2/switches/fasten_seat_belts"]


@add_to_panel
class il_smoking(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/cockpit2/switches/no_smoking"]


@add_to_panel
class il_cabin(ThreeStateButton):
    dataref: xp.Params = xp.Params["sim/custom/7x/paxlum"]
    states = [1, 2, 0]


@add_to_panel
class il_cabin_pax(il_cabin):
    @classmethod
    def get_state(cls):
        return super().get_state() == 1


@add_to_panel
class il_cabin_off(il_cabin):
    @classmethod
    def get_state(cls):
        return super().get_state() == 2


@add_to_panel
class rain_rplint_rh(PushButton):
    @classmethod
    async def click(cls):
        pass
