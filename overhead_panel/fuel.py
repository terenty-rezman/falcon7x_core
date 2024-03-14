import asyncio
import time

from instrument_panel import add_to_panel, TwoStateButton, ThreeStateButton, FloatSwitch, DiscreteSwitch
import xplane as xp


@add_to_panel
class boost1(ThreeStateButton):
    dataref: xp.Params = xp.Params["sim/custom/7x/fpump0"]
    states = [2, 0, 1]


@add_to_panel
class xtk_1(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/7x/bt1f3"]


@add_to_panel
class xtk_2(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/7x/bt3f1"]


@add_to_panel
class boost3(ThreeStateButton):
    dataref: xp.Params = xp.Params["sim/custom/7x/fpump2"]
    states = [2, 0, 1]


@add_to_panel
class xtk_3(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/7x/bt1f2"]


@add_to_panel
class backup_13(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/7x/bk13"]


@add_to_panel
class xtk_4(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/7x/bt3f2"]


@add_to_panel
class xtk_5(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/7x/bt2f1"]


@add_to_panel
class boost2(ThreeStateButton):
    dataref: xp.Params = xp.Params["sim/custom/7x/fpump1"]
    states = [2, 0, 1]


@add_to_panel
class xtk_6(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/7x/bt2f3"]


@add_to_panel
class xbp_12(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/weapons/mis_thrust3"]
    index = 21


@add_to_panel
class xbp_13(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/weapons/mis_thrust3"]
    index = 22


@add_to_panel
class xbp_23(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/weapons/mis_thrust3"]
    index = 23
