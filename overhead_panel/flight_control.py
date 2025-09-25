from common.instrument_panel import add_to_panel, TwoStateButton, Indicator, NLocalStateButton
import xplane.master as xp
import common.xp_aircraft_state as xp_ac


@add_to_panel
class airbrake_auto(NLocalStateButton):
    # vol 2 27-66
    dataref: xp.Params = xp.Params["sim/cockpit2/controls/speedbrake_ratio"]
    state = 0

    @classmethod 
    def get_state(cls):
        return cls.state

    @classmethod
    async def set_state(cls, state):
        cls.state = state

        if state > 0:
            await xp.set_param(cls.dataref, -0.5)


@add_to_panel
class fcs_engage_norm(TwoStateButton):
    # vol 2 27-16
    dataref: xp.Params = xp.Params["sim/cockpit2/switches/artificial_stability_on"]
    states = [1, 0]


@add_to_panel
class fcs_engage_stby(TwoStateButton):
    # vol 2 27-16
    dataref: xp.Params = xp.Params["sim/cockpit2/switches/yaw_damper_on"]
    states = [1, 0]


@add_to_panel
class fcs_steering(TwoStateButton):
    # vol 2 hz gde
    dataref: xp.Params = xp.Params["sim/cockpit2/controls/nosewheel_steer_on"]
    states = [1, 0]
