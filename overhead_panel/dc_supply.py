import asyncio
import time

from common.instrument_panel import add_to_panel, TwoStateButton, ThreeStateButton
import xplane.master as xp


@add_to_panel
class galley_master(ThreeStateButton):
    dataref: xp.Params = xp.Params["sim/weapons/mis_thrust2"]
    index = 5
    states = [2, 0, 1]

    @classmethod
    def get_indication(cls):
        state = cls.get_state()
        if state == 0:
            return 0
        if state == 1:
            return 2
        if state == 2:
            return 1


@add_to_panel
class galley_master_on(ThreeStateButton):
    @classmethod
    def get_state(cls):
        return galley_master.get_state() == 2


@add_to_panel
class galley_master_off(ThreeStateButton):
    @classmethod
    def get_state(cls):
        return galley_master.get_state() == 1


@add_to_panel
class lh_master(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/custom/7x/lhmaster"]
    states = [1, 0]


@add_to_panel
class lh_init(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/custom/7x/lhinit"]
    states = [1, 0]


@add_to_panel
class bus_tie(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/cockpit2/electrical/cross_tie"]


@add_to_panel
class rh_init(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/custom/7x/rhinit"]
    states = [1, 0]


@add_to_panel
class rh_master(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/custom/7x/rhmaster"]
    states = [1, 0]


@add_to_panel
class cabin_master(ThreeStateButton):
    dataref: xp.Params = xp.Params["sim/weapons/mis_thrust2"]
    index = 4
    states = [2, 0, 1]

    @classmethod
    def get_indication(cls):
        if cls.override_indication is not None:
            return cls.override_indication

        state = cls.get_state()
        if state == 0:
            return 0
        if state == 1:
            return 2
        if state == 2:
            return 1


@add_to_panel
class cabin_master_on(cabin_master):
    @classmethod
    def get_state(cls):
        return super().get_state() == 2


@add_to_panel
class cabin_master_off(cabin_master):
    @classmethod
    def get_state(cls):
        return super().get_state() == 1


@add_to_panel
class ext_power(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/cockpit/electrical/gpu_on"]


@add_to_panel
class gen1(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/cockpit2/electrical/generator_on"]
    states = [0, 1]
    index = 0

    @classmethod
    def get_indication(cls):
        if cls.override_indication is not None:
            return cls.override_indication

        state = cls.get_state()
        return 0 if state == 1 else 1


@add_to_panel
class lh_isol(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/custom/7x/lhisol"]
    states = [1, 0]


@add_to_panel
class rat_reset(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/cockpit2/switches/ram_air_turbine_on"]
    states = [1, 0]


@add_to_panel
class rh_isol(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/custom/7x/rhisol"]
    states = [1, 0]


@add_to_panel
class gen2(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/cockpit2/electrical/generator_on"]
    states = [0, 1]
    index = 1

    @classmethod
    def get_indication(cls):
        if cls.override_indication is not None:
            return cls.override_indication

        state = cls.get_state()
        return 0 if state == 1 else 1


@add_to_panel
class gen3(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/cockpit2/electrical/generator_on"]
    states = [0, 1]
    index = 2

    @classmethod
    def get_indication(cls):
        if cls.override_indication is not None:
            return cls.override_indication

        state = cls.get_state()
        return 0 if state == 1 else 1


@add_to_panel
class bat1(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/cockpit2/electrical/battery_on"]
    states = [0, 1]
    index = 0

    @classmethod
    def get_indication(cls):
        if cls.override_indication is not None:
            return cls.override_indication

        state = cls.get_state()
        return 0 if state == 1 else 1


@add_to_panel
class bat2(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/cockpit2/electrical/battery_on"]
    states = [0, 1]
    index = 1

    @classmethod
    def get_indication(cls):
        if cls.override_indication is not None:
            return cls.override_indication

        state = cls.get_state()
        return 0 if state == 1 else 1
