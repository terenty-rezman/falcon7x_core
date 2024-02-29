from .overhead_panel import add_to_overhead_panel, TwoStateButton, ThreeStateButton, FloatSwitch, DiscreteSwitch
import xplane as xp


@add_to_overhead_panel
class dump(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/cockpit2/pressurization/actuators/dump_to_altitude_on"]


@add_to_overhead_panel
class bag_vent(ThreeStateButton):
    dataref: xp.Params = xp.Params["sim/weapons/mis_thrust2"]
    states = [3, 0, 1]
    index = 0 
