from .overhead_panel import add_to_overhead_panel, TwoStateButton, Indicator
import xplane as xp
import xp_aircraft_state as xp_ac


@add_to_overhead_panel("airbrake_auto")
class airbrake_auto(TwoStateButton):
    # vol 2 27-66
    dataref: xp.Params = xp.Params["sim/cockpit2/controls/speedbrake_ratio"]
    enabled_val = "0"
    disabled_val = "0.5"

    @classmethod
    def get_state(cls):
        if (val := xp_ac.ACState.get_curr_param_if_available(cls.dataref)) is not None:
            return 1 if val == 0 else 0


@add_to_overhead_panel("fcs_engage_norm")
class fcs_engage_norm(TwoStateButton):
    # vol 2 27-16
    dataref: xp.Params = xp.Params["sim/cockpit2/switches/artificial_stability_on"]
    enabled_val = "0"
    disabled_val = "1"

    @classmethod
    def get_state(cls):
        if (val := xp_ac.ACState.get_curr_param_if_available(cls.dataref)) is None:
            return
        return 1 if val == 0 else 0


@add_to_overhead_panel("fcs_engage_stby")
class fcs_engage_stby(TwoStateButton):
    # vol 2 27-16
    dataref: xp.Params = xp.Params["sim/cockpit2/switches/yaw_damper_on"]
    enabled_val = "0"
    disabled_val = "1"

    @classmethod
    def get_state(cls):
        if (val := xp_ac.ACState.get_curr_param_if_available(cls.dataref)) is None:
            return
        return 1 if val == 0 else 0


@add_to_overhead_panel("fcs_steering")
class fcs_steering(TwoStateButton):
    # vol 2 hz gde
    dataref: xp.Params = xp.Params["sim/cockpit2/controls/nosewheel_steer_on"]
    enabled_val = "0"
    disabled_val = "1"

    @classmethod
    def get_state(cls):
        if (val := xp_ac.ACState.get_curr_param_if_available(cls.dataref)) is None:
            return
        return 1 if val == 0 else 0
