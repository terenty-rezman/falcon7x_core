from .overhead_panel import add_to_overhead_panel, TwoStateButton, Indicator, array_str
import xplane as xp
import xp_aircraft_state as xp_ac
import util


@add_to_overhead_panel
class firebutton_1(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/weapons/warhead_type"]
    index = 4
    enabled_val = array_str(index, "1")
    disabled_val = array_str(index, "0")


@add_to_overhead_panel
class fireindicator_1(Indicator):
    dataref: xp.Params = xp.Params["sim/cockpit2/annunciators/engine_fires"]
    index = 0


@add_to_overhead_panel
class disch_11(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/cockpit2/engine/actuators/fire_extinguisher_on"] 
    index = 0
    enabled_val = array_str(index, "1")
    disabled_val = array_str(index, "0")

    @classmethod
    def get_indication(cls):
        val = cls.get_state()

        if val is None:
            return val

        if firebutton_1.get_state() == 1:
            if val == 0:
                return 1
            else:
                return 2
        else:
            if val == 0:
                return 0
            else:
                return 2 


@add_to_overhead_panel
class disch_12(disch_11):
    pass

@add_to_overhead_panel
class fire_apu_indicator(Indicator):
    dataref: xp.Params = xp.Params["sim/operation/failures/rel_apu_fire"]


@add_to_overhead_panel
class apu_disch(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/cockpit2/engine/actuators/fire_extinguisher_on"] 
    index = 4
    enabled_val = array_str(index, "1")
    disabled_val = array_str(index, "0")


@add_to_overhead_panel
class fire_apu_closed_indicator(Indicator):
    dataref: xp.Params = xp.Params["sim/cockpit/engine/APU_switch"]
    blink = util.blink_anim(0.7)

    @classmethod
    def get_indication(cls):
        if xp_ac.ACState.get_curr_param(xp.Params["sim/operation/failures/rel_apu_fire"]) == 6:
            if xp_ac.ACState.get_curr_param(cls.dataref) == 0:
                # blink animation
                return next(cls.blink)
            else:
                return 1
        return 0


@add_to_overhead_panel
class firebutton_2(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/weapons/warhead_type"]
    index = 5
    enabled_val = array_str(index, "1")
    disabled_val = array_str(index, "0")


@add_to_overhead_panel
class fireindicator_2(Indicator):
    dataref: xp.Params = xp.Params["sim/cockpit2/annunciators/engine_fires"]
    index = 1


@add_to_overhead_panel
class disch_21(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/cockpit2/engine/actuators/fire_extinguisher_on"] 
    index = 1
    enabled_val = array_str(index, "1")
    disabled_val = array_str(index, "0")

    @classmethod
    def get_indication(cls):
        val = cls.get_state()

        if val is None:
            return val

        if firebutton_2.get_state() == 1:
            if val == 0:
                return 1
            else:
                return 2
        else:
            if val == 0:
                return 0
            else:
                return 2 


@add_to_overhead_panel
class disch_22(disch_21):
    pass


@add_to_overhead_panel
class firebutton_3(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/weapons/warhead_type"]
    index = 6
    enabled_val = array_str(index, "1")
    disabled_val = array_str(index, "0")


@add_to_overhead_panel
class fireindicator_3(Indicator):
    dataref: xp.Params = xp.Params["sim/cockpit2/annunciators/engine_fires"]
    index = 2


@add_to_overhead_panel
class disch_31(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/cockpit2/engine/actuators/fire_extinguisher_on"] 
    index = 2
    enabled_val = array_str(index, "1")
    disabled_val = array_str(index, "0")

    @classmethod
    def get_indication(cls):
        val = cls.get_state()

        if val is None:
            return val

        if firebutton_3.get_state() == 1:
            if val == 0:
                return 1
            else:
                return 2
        else:
            if val == 0:
                return 0
            else:
                return 2 


@add_to_overhead_panel
class disch_32(disch_31):
    pass


@add_to_overhead_panel
class firerearcomp_button(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/weapons/mis_thrust2"] 
    index = 7
    enabled_val = array_str(index, "1")
    disabled_val = array_str(index, "0")


@add_to_overhead_panel
class firerearcomp_indicator(Indicator):
    dataref: xp.Params = xp.Params["sim/operation/failures/rel_engfir3"]

    @classmethod
    def get_state(cls):
        if (val := xp_ac.ACState.get_curr_param(cls.dataref)) is None:
            return
        return 1 if val == 6 else 0


@add_to_overhead_panel
class firebagcomp_button(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/weapons/mis_thrust2"] 
    index = 6
    enabled_val = array_str(index, "1")
    disabled_val = array_str(index, "0")


@add_to_overhead_panel
class firebagcomp_indicator(Indicator):
    dataref: xp.Params = xp.Params["sim/operation/failures/rel_engfir4"]

    @classmethod
    def get_state(cls):
        if (val := xp_ac.ACState.get_curr_param(cls.dataref)) is None:
            return
        return 1 if val == 6 else 0
