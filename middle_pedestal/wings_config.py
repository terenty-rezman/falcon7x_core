import asyncio
import time

from instrument_panel import add_to_panel, TwoStateButton, Indicator, PushButton, NLocalStateButton, LocalStateIndicator, FloatStepper, array_str
import xplane as xp
import xp_aircraft_state as xp_ac
import util
        

@add_to_panel
class wc_sf_0(TwoStateButton):
    flaps_val = 0

    @classmethod
    async def set_state(cls, state):
        if state == 1:
            val = array_str(0, cls.flaps_val) 
            await xp.set_param(xp.Params["sim/multiplayer/controls/flap_request"], val)


@add_to_panel
class wc_sf_1(wc_sf_0):
    flaps_val = 0.33


@add_to_panel
class wc_sf_2(wc_sf_0):
    flaps_val = 0.66


@add_to_panel
class wc_sf_3(wc_sf_0):
    flaps_val = 1.0


@add_to_panel
class wc_backup_slats(PushButton):
    @classmethod
    async def click(cls):
        pass


@add_to_panel
class wc_ab_0(TwoStateButton):
    airbrake_val = 0

    @classmethod
    async def set_state(cls, state):
        if state == 1:
            await xp.set_param(xp.Params["sim/cockpit2/controls/speedbrake_ratio"], cls.airbrake_val)


@add_to_panel
class wc_ab_1(wc_ab_0):
    airbrake_val = 0.5


@add_to_panel
class wc_ab_2(wc_ab_0):
    airbrake_val = 1
