from .overhead_panel import add_to_overhead_panel, TwoStateButton, Indicator
import xplane as xp
import xp_aircraft_state as xp_ac
import util


@add_to_overhead_panel("firebutton_1")
class firebutton_1(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/weapons/warhead_type"]
    index = 4
    enabled_val = "[,,,,1]"
    disabled_val = "[,,,,0]"


@add_to_overhead_panel("fireindicator_1")
class fireindicator_1(Indicator):
    dataref: xp.Params = xp.Params["sim/cockpit2/annunciators/engine_fires"]
    index = 0


@add_to_overhead_panel("disch_11")
class disch_11(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/cockpit2/engine/actuators/fire_extinguisher_on"] 
    index = 0
    enabled_val = "[1]"
    disabled_val = "[0]"


disch_12 = disch_11
add_to_overhead_panel("disch_12")(disch_12)

@add_to_overhead_panel("fire_apu_indicator")
class fire_apu_indicator(Indicator):
    dataref: xp.Params = xp.Params["sim/operation/failures/rel_apu_fire"]


@add_to_overhead_panel("apu_disch")
class apu_disch(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/cockpit2/engine/actuators/fire_extinguisher_on"] 
    index = 4
    enabled_val = "[,,,,1]"
    disabled_val = "[,,,,0]"


@add_to_overhead_panel("fire_apu_closed_indicator")
class fire_apu_closed_indicator(Indicator):
    dataref: xp.Params = xp.Params["sim/cockpit/engine/APU_switch"]
    blink = util.blink_anim(0.7)

    @classmethod
    def get_indication(cls):
        if xp_ac.ACState.param_available(xp.Params["sim/operation/failures/rel_apu_fire"]):
            if xp_ac.ACState.curr_params[xp.Params["sim/operation/failures/rel_apu_fire"]]:
                if xp_ac.ACState.param_available(cls.dataref):
                    if xp_ac.ACState.curr_params[cls.dataref] == 0:
                        return next(cls.blink)
                    else:
                        return 1
            return 0





@add_to_overhead_panel("firebutton_2")
class firebutton_2(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/weapons/warhead_type"]
    index = 5
    enabled_val = "[,,,,,1]"
    disabled_val = "[,,,,,0]"


@add_to_overhead_panel("fireindicator_2")
class fireindicator_2(Indicator):
    dataref: xp.Params = xp.Params["sim/cockpit2/annunciators/engine_fires"]
    index = 1


@add_to_overhead_panel("disch_21")
class disch_21(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/cockpit2/engine/actuators/fire_extinguisher_on"] 
    index = 1
    enabled_val = "[,1]"
    disabled_val = "[,0]"


disch_22 = disch_21
add_to_overhead_panel("disch_22")(disch_22)


@add_to_overhead_panel("firebutton_3")
class firebutton_3(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/weapons/warhead_type"]
    index = 6
    enabled_val = "[,,,,,,1]"
    disabled_val = "[,,,,,,0]"


@add_to_overhead_panel("fireindicator_3")
class fireindicator_3(Indicator):
    dataref: xp.Params = xp.Params["sim/cockpit2/annunciators/engine_fires"]
    index = 2


@add_to_overhead_panel("disch_31")
class disch_31(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/cockpit2/engine/actuators/fire_extinguisher_on"] 
    index = 2
    enabled_val = "[,,1]"
    disabled_val = "[,,0]"


disch_32 = disch_31
add_to_overhead_panel("disch_32")(disch_32)


@add_to_overhead_panel("firerearcomp_button")
class firerearcomp_button(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/weapons/mis_thrust2"] 
    index = 7
    enabled_val = "[,,,,,,,1]"
    disabled_val = "[,,,,,,,0]"


@add_to_overhead_panel("firerearcomp_indicator")
class firerearcomp_indicator(Indicator):
    dataref: xp.Params = xp.Params["sim/operation/failures/rel_engfir3"]

    @classmethod
    def get_state(cls):
        if xp_ac.ACState.param_available(cls.dataref):
            val = xp_ac.ACState.curr_params[cls.dataref]
            return 1 if val == 6 else 0


@add_to_overhead_panel("firebagcomp_button")
class firebagcomp_button(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/weapons/mis_thrust2"] 
    index = 6
    enabled_val = "[,,,,,,1]"
    disabled_val = "[,,,,,,0]"


@add_to_overhead_panel("firebagcomp_indicator")
class firebagcomp_indicator(Indicator):
    dataref: xp.Params = xp.Params["sim/operation/failures/rel_engfir4"]

    @classmethod
    def get_state(cls):
        if xp_ac.ACState.param_available(cls.dataref):
            val = xp_ac.ACState.curr_params[cls.dataref]
            return 1 if val == 6 else 0
