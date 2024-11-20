import asyncio
import time

from instrument_panel import add_to_panel, TwoStateButton, ThreeStateButton, FloatSwitch, DiscreteSwitch, PushButton
import xplane.master as xp
import xp_aircraft_state as xp_ac
import util



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
        if state > 2:
            await super().set_state(0)
        else:
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
                return next(cls.blink)
        return 0


@add_to_panel
class el_landing_lh_off(el_landing_lh):
    @classmethod
    async def set_state(cls, state):
        if state == 1:
            await super().set_state(2)


@add_to_panel
class el_landing_lh_on(el_landing_lh):
    @classmethod
    async def set_state(cls, state):
        if state == 1:
            await super().set_state(0)


@add_to_panel
class el_landing_lh_pulse(el_landing_lh):
    @classmethod
    async def set_state(cls, state):
        if state == 1:
            await super().set_state(1)


@add_to_panel
class el_landing_rh(el_landing_lh):
    index = 10


@add_to_panel
class el_landing_rh_off(el_landing_rh):
    @classmethod
    async def set_state(cls, state):
        if state == 1:
            await super().set_state(2)


@add_to_panel
class el_landing_rh_on(el_landing_rh):
    @classmethod
    async def set_state(cls, state):
        if state == 1:
            await super().set_state(0)


@add_to_panel
class el_landing_rh_pulse(el_landing_rh):
    @classmethod
    async def set_state(cls, state):
        if state == 1:
            await super().set_state(1)


@add_to_panel
class el_taxi(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/cockpit/electrical/taxi_light_on"]
