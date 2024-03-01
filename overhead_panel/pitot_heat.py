from .overhead_panel import add_to_overhead_panel, TwoStateButton, ThreeStateButton, FloatSwitch, DiscreteSwitch
import xplane as xp


@add_to_overhead_panel
class probe_12(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/cockpit2/ice/ice_pitot_heat_on_pilot"]

    @classmethod
    def get_indication(cls):
        return not super().get_indication()


@add_to_overhead_panel
class probe_3(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/cockpit2/ice/ice_pitot_heat_on_copilot"]

    @classmethod
    def get_indication(cls):
        return not super().get_indication()


@add_to_overhead_panel
class probe_4(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/cockpit2/ice/ice_AOA_heat_on"]

    @classmethod
    def get_indication(cls):
        return not super().get_indication()
