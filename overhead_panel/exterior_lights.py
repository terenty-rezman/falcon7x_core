import asyncio
import time

from .overhead_panel import add_to_overhead_panel, TwoStateButton, ThreeStateButton, FloatSwitch, DiscreteSwitch, PushButton
import xplane as xp
import xp_aircraft_state as xp_ac
import util



@add_to_overhead_panel
class rain_rplint_lh(PushButton):
    @classmethod
    async def click(cls):
        pass


@add_to_overhead_panel
class el_nav(ThreeStateButton):
    dataref: xp.Params = xp.Params["sim/custom/7x/lum1"]
    states = [1, 2, 0]


@add_to_overhead_panel
class el_anticol(ThreeStateButton):
    dataref: xp.Params = xp.Params["sim/custom/7x/lum2"]
    states = [2, 0, 1]


@add_to_overhead_panel
class el_wing(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/cockpit2/switches/spot_light_on"]


@add_to_overhead_panel
class el_landing_lh(DiscreteSwitch):
    dataref: xp.Params = xp.Params["sim/weapons/warhead_type"]
    states = [2, 1, 0]
    index = 11

    blink = util.blink_anim(0.7)

    @classmethod
    def get_indication(cls):
        # param = xp_ac.ACState.get_curr_param(xp.Params["sim/cockpit2/switches/landing_lights_switch"])

        state = cls.get_state()
        if state == 0:
            return 1
        elif state == 1:
            return next(cls.blink)
        else:
            return 0
