from instrument_panel import add_to_panel, TwoStateButton, Indicator
import xplane.master as xp
import xp_aircraft_state as xp_ac


@add_to_panel
class airbrake_auto(TwoStateButton):
    # vol 2 27-66
    dataref: xp.Params = xp.Params["sim/cockpit2/controls/speedbrake_ratio"]
    states = [-0.5, 0, 0.5, 1.0]

    @classmethod
    def get_state(cls):
        state = super().get_state()

        if state is None:
            return

        if state > 0:
            return 1
        return 0

    @classmethod
    async def click(cls):
        state = cls.get_state()
        if state is None:
            return

        if state != 0:
            await cls.set_state(0) 
        else:
            await cls.set_state(1)


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
