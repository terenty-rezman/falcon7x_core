from instrument_panel import add_to_panel, TwoStateButton, Indicator
import xplane.master as xp
import xp_aircraft_state as xp_ac
import util


@add_to_panel
class firebutton_1(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/weapons/warhead_type"]
    index = 4
    states = [0, 1]


@add_to_panel
class fireindicator_1(Indicator):
    dataref: xp.Params = xp.Params["sim/cockpit2/annunciators/engine_fires"]
    index = 0


@add_to_panel
class disch1_eng1(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/cockpit2/engine/actuators/fire_extinguisher_on"] 
    index = 0


@add_to_panel
class disch1_eng1_1(Indicator):
    dataref: xp.Params = xp.Params["sim/cockpit2/engine/actuators/fire_extinguisher_on"] 
    index = 0

    @classmethod
    def get_indication(cls):
        if firebutton_1.get_state() == 1:
            return 1

        return 0


@add_to_panel
class disch2_eng1(disch1_eng1):
    pass


@add_to_panel
class disch2_eng1_1(disch1_eng1_1):
    pass


@add_to_panel
class fire_apu_indicator(Indicator):
    dataref: xp.Params = xp.Params["sim/operation/failures/rel_apu_fire"]
    states = [0, 1, 2, 3, 4, 5, 6]

    @classmethod
    def get_state(cls):
        if (val := xp_ac.ACState.get_curr_param(cls.dataref)) is None:
            return
        return 1 if val == 6 else 0


@add_to_panel
class apu_disch(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/cockpit2/engine/actuators/fire_extinguisher_on"] 
    index = 4


@add_to_panel
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


@add_to_panel
class firebutton_2(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/weapons/warhead_type"]
    index = 5


@add_to_panel
class fireindicator_2(Indicator):
    dataref: xp.Params = xp.Params["sim/cockpit2/annunciators/engine_fires"]
    index = 1


@add_to_panel
class disch1_eng2(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/cockpit2/engine/actuators/fire_extinguisher_on"] 
    index = 1


@add_to_panel
class disch1_eng2_1(Indicator):
    dataref: xp.Params = xp.Params["sim/cockpit2/engine/actuators/fire_extinguisher_on"] 
    index = 1

    @classmethod
    def get_indication(cls):
        if firebutton_2.get_state() == 1:
            return 1

        return 0


@add_to_panel
class disch2_eng2(disch1_eng2):
    pass


@add_to_panel
class disch2_eng2_1(disch1_eng2_1):
    pass


@add_to_panel
class firebutton_3(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/weapons/warhead_type"]
    index = 6


@add_to_panel
class fireindicator_3(Indicator):
    dataref: xp.Params = xp.Params["sim/cockpit2/annunciators/engine_fires"]
    index = 2


@add_to_panel
class disch1_eng3(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/cockpit2/engine/actuators/fire_extinguisher_on"] 
    index = 2


@add_to_panel
class disch1_eng3_1(Indicator):
    dataref: xp.Params = xp.Params["sim/cockpit2/engine/actuators/fire_extinguisher_on"] 
    index = 2

    @classmethod
    def get_indication(cls):
        if firebutton_3.get_state() == 1:
            return 1

        return 0


@add_to_panel
class disch2_eng3(disch1_eng3):
    pass


@add_to_panel
class disch2_eng3_1(disch1_eng3_1):
    pass


@add_to_panel
class firerearcomp_button(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/weapons/mis_thrust2"] 
    index = 7


@add_to_panel
class firerearcomp_indicator(Indicator):
    dataref: xp.Params = xp.Params["sim/operation/failures/rel_engfir3"]
    states = [0, 1, 2, 3, 4, 5, 6]

    @classmethod
    def get_state(cls):
        if (val := xp_ac.ACState.get_curr_param(cls.dataref)) is None:
            return
        return 1 if val == 6 else 0


@add_to_panel
class firebagcomp_button(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/weapons/mis_thrust2"] 
    index = 6


@add_to_panel
class firebagcomp_indicator(Indicator):
    dataref: xp.Params = xp.Params["sim/operation/failures/rel_engfir4"]
    states = [0, 1, 2, 3, 4, 5, 6]

    @classmethod
    def get_state(cls):
        if (val := xp_ac.ACState.get_curr_param(cls.dataref)) is None:
            return
        return 1 if val == 6 else 0
