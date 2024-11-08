import asyncio
import time

from instrument_panel import add_to_panel, TwoStateButton, ThreeStateButton, FloatSwitch, DiscreteSwitch
import xplane as xp


@add_to_panel
class windshield_lh(ThreeStateButton):
    dataref: xp.Params = xp.Params["sim/cockpit2/ice/ice_AOA_heat_on_copilot"]
    states = [1, 2, 0]


@add_to_panel
class windshield_lh_off(windshield_lh):
    @classmethod
    def get_state(cls):
        return super().get_state() == 2


@add_to_panel
class windshield_lh_max(windshield_lh):
    @classmethod
    def get_state(cls):
        return super().get_state() == 1


@add_to_panel
class windshield_rh(ThreeStateButton):
    dataref: xp.Params = xp.Params["sim/cockpit2/ice/ice_window_heat_on"]
    states = [1, 2, 0]


@add_to_panel
class windshield_rh_off(windshield_rh):
    @classmethod
    def get_state(cls):
        return super().get_state() == 2


@add_to_panel
class windshield_rh_max(windshield_rh):
    @classmethod
    def get_state(cls):
        return super().get_state() == 1


@add_to_panel
class windshield_backup(ThreeStateButton):
    dataref: xp.Params = xp.Params["sim/cockpit2/ice/ice_auto_ignite_on"]
    states = [1, 2, 0]


@add_to_panel
class windshield_backup_max(windshield_backup):
    @classmethod
    def get_state(cls):
        return super().get_state() == 1


@add_to_panel
class windshield_backup_off(windshield_backup):
    @classmethod
    def get_state(cls):
        return super().get_state() == 2
