import asyncio
import time

from common.instrument_panel import add_to_panel, TwoStateButton, ThreeStateButton, FloatSwitch, DiscreteSwitch, PushButton
import xplane.master as xp
import common.xp_aircraft_state as xp_ac
import common.util as util



@add_to_panel
class rain_rplint_lh(PushButton):
    @classmethod
    async def click(cls):
        pass


@add_to_panel
class el_nav(ThreeStateButton):
    dataref: xp.Params = xp.Params["sim/custom/7x/lum1"]
    states = [1, 2, 0]


@add_to_panel
class el_nav_logo(el_nav):
    @classmethod
    def get_state(cls):
        return super().get_state() == 1


@add_to_panel
class el_nav_off(el_nav):
    @classmethod
    def get_state(cls):
        return super().get_state() == 2


@add_to_panel
class el_anticol(ThreeStateButton):
    dataref: xp.Params = xp.Params["sim/custom/7x/lum2"]
    states = [2, 0, 1]


@add_to_panel
class el_anticol_red(el_anticol):
    @classmethod
    def get_state(cls):
        return super().get_state() == 2


@add_to_panel
class el_anticol_off(el_anticol):
    @classmethod
    def get_state(cls):
        return super().get_state() == 1


@add_to_panel
class el_wing(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/cockpit2/switches/spot_light_on"]


@add_to_panel
class el_landing_lh(DiscreteSwitch):
    dataref: xp.Params = xp.Params["sim/weapons/warhead_type"]
    states = [2, 1, 0, 3]
    index = 11

    blink = util.blink_anim(0.5)

    on_digit = 0
    off_digit = 0

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
            if cls.off_digit == 1 and cls.on_digit == 0:
                state = 2
            elif cls.off_digit == 0 and cls.on_digit == 1:
                state = 0
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
        # param = xp_ac.ACState.get_curr_param(xp.Params["sim/cockpit2/switches/landing_lights_switch"])

        state = cls.get_state()
        if state == 0:
            return 1
        elif state == 1:
            if el_anticol.get_state() == 0:
                # return next(cls.blink)
                return 1
        return 0


@add_to_panel
class el_landing_lh_off():
    @classmethod
    async def set_state(cls, state):
        el_landing_lh.off_digit = state
        await el_landing_lh.set_state(None)


@add_to_panel
class el_landing_lh_on():
    @classmethod
    async def set_state(cls, state):
        el_landing_lh.on_digit = state
        await el_landing_lh.set_state(None)


# @add_to_panel
# class el_landing_lh_pulse(el_landing_lh):
#     @classmethod
#     async def set_state(cls, state):
#         if state == 1:
#             await super().set_state(1)


@add_to_panel
class el_landing_rh(el_landing_lh):
    index = 10

    on_digit = 0
    off_digit = 0


@add_to_panel
class el_landing_rh_off():
    @classmethod
    async def set_state(cls, state):
        el_landing_rh.off_digit = state
        await el_landing_rh.set_state(None)


@add_to_panel
class el_landing_rh_on():
    @classmethod
    async def set_state(cls, state):
        el_landing_rh.on_digit = state
        await el_landing_rh.set_state(None)


# @add_to_panel
# class el_landing_rh_pulse(el_landing_rh):
#     @classmethod
#     async def set_state(cls, state):
#         if state == 1:
#             await super().set_state(1)


@add_to_panel
class el_taxi(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/cockpit/electrical/taxi_light_on"]
