import time
from common.instrument_panel import add_to_panel, TwoStateButton, NLocalStateButton, Indicator
import xplane.master as xp
import common.xp_aircraft_state as xp_ac
import common.util as util
from common import plane_control as pc
from cas import cas
import overhead_panel.hydraulics as hyd


@add_to_panel
class firebutton_1(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/weapons/warhead_type"]
    index = 4
    states = [0, 1]

    blink = util.blink_anim(0.5)
    blink_timer = None

    @classmethod
    async def set_state(cls, state):
        if state == 1:
            cls.blink_timer = util.Timer()
            cls.blink_timer.start()
        else:
            cls.blink_timer = None
            await hyd.shutoff_a1.set_state(0)
            
        return await super().set_state(state)

    @classmethod
    def get_indication(cls):
        if cls.override_indication is not None:
            return cls.override_indication

        if cls.blink_timer:
            if cls.blink_timer.elapsed() < 4:
                return next(cls.blink)
            else:
                cls.blink_timer = None

        return cls.get_state()


@add_to_panel
class fireindicator_1(Indicator):
    dataref: xp.Params = xp.Params["sim/cockpit2/annunciators/engine_fires"]
    index = 0

    @classmethod
    async def set_state(cls, state):
        await super(TwoStateButton, cls).set_state(state)


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
        if cls.override_indication is not None:
            return cls.override_indication

        # fireindicator_1 instead of fireindicator_1 ?? 
        if firebutton_1.get_state() == 1:
            return 1

        return 0


@add_to_panel
class disch2_eng1(NLocalStateButton):
    states = [0, 1]
    state = 0

    @classmethod
    async def click(cls):
        await super().click()


@add_to_panel
class disch2_eng1_1(NLocalStateButton):
    states = [0, 1]
    state = 0

    @classmethod
    async def click(cls):
        await super().click()

    @classmethod
    def get_indication(cls):
        if cls.override_indication is not None:
            return cls.override_indication

        # fireindicator_1 instead of fireindicator_1 ?? 
        if firebutton_1.get_state() == 1:
            return 1

        return 0

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
        if cls.override_indication is not None:
            return cls.override_indication

        if xp_ac.ACState.get_curr_param(xp.Params["sim/operation/failures/rel_apu_fire"]) == 6:
            if xp_ac.ACState.get_curr_param(cls.dataref) == 1:
                # blink animation
                return next(cls.blink)
            else:
                return 1
        return 0


@add_to_panel
class firebutton_2(firebutton_1):
    dataref: xp.Params = xp.Params["sim/weapons/warhead_type"]
    index = 5

    states = [0, 1]

    blink = util.blink_anim(0.5)
    blink_timer = None

    @classmethod
    async def set_state(cls, state):
        if state == 1:
            cls.blink_timer = util.Timer()
            cls.blink_timer.start()
        else:
            cls.blink_timer = None
            await hyd.shutoff_b2.set_state(0)
            await hyd.shutoff_c2.set_state(0)
            
        return await super().set_state(state)


@add_to_panel
class fireindicator_2(fireindicator_1):
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
        if cls.override_indication is not None:
            return cls.override_indication

        if firebutton_2.get_state() == 1:
            return 1

        return 0


@add_to_panel
class disch2_eng2(NLocalStateButton):
    states = [0, 1]
    state = 0

    @classmethod
    async def click(cls):
        await super().click()


@add_to_panel
class disch2_eng2_1(NLocalStateButton):
    states = [0, 1]
    state = 0

    @classmethod
    async def click(cls):
        await super().click()

    @classmethod
    def get_indication(cls):
        if cls.override_indication is not None:
            return cls.override_indication

        if firebutton_2.get_state() == 1:
            return 1

        return 0


@add_to_panel
class firebutton_3(firebutton_1):
    dataref: xp.Params = xp.Params["sim/weapons/warhead_type"]
    index = 6

    states = [0, 1]

    blink = util.blink_anim(0.5)
    blink_timer = None

    @classmethod
    async def set_state(cls, state):
        if state == 1:
            cls.blink_timer = util.Timer()
            cls.blink_timer.start()
        else:
            cls.blink_timer = None
            await hyd.shutoff_a3.set_state(0)
            await hyd.shutoff_b3.set_state(0)
            
        return await super().set_state(state)


@add_to_panel
class fireindicator_3(fireindicator_1):
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
        if cls.override_indication is not None:
            return cls.override_indication

        if firebutton_3.get_state() == 1:
            return 1

        return 0


@add_to_panel
class disch2_eng3(NLocalStateButton):
    states = [0, 1]
    state = 0

    @classmethod
    async def click(cls):
        await super().click()


@add_to_panel
class disch2_eng3_1(NLocalStateButton):
    states = [0, 1]
    state = 0

    @classmethod
    async def click(cls):
        await super().click()

    @classmethod
    def get_indication(cls):
        if cls.override_indication is not None:
            return cls.override_indication

        if firebutton_3.get_state() == 1:
            return 1

        return 0


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


@add_to_panel
class fire_test(NLocalStateButton):
    states = [0, 1]
    state = 0
    cas_shown = False

    @classmethod
    async def set_state(cls, state):
        await super().set_state(state)

        if state and cls.cas_shown == False:
            # show cas
            await cas.show_message(cas.FIRE_TEST_IN_PROGRESS)
            cls.cas_shown = True
        
        if state == 0 and cls.cas_shown == True:
            # hide cas
            await cas.remove_message(cas.FIRE_TEST_IN_PROGRESS)
            cls.cas_shown = False

        if state == 0:
            state = None

        firebutton_1.set_override_indication(state)
        firebutton_2.set_override_indication(state)
        firebutton_3.set_override_indication(state)

        fireindicator_1.set_override_indication(state)
        fireindicator_2.set_override_indication(state)
        fireindicator_3.set_override_indication(state)

        disch1_eng1.set_override_indication(state)
        disch1_eng1_1.set_override_indication(state)
        disch2_eng1.set_override_indication(state)
        disch2_eng1_1.set_override_indication(state)

        disch1_eng2.set_override_indication(state)
        disch1_eng2_1.set_override_indication(state)
        disch2_eng2.set_override_indication(state)
        disch2_eng2_1.set_override_indication(state)

        disch1_eng3.set_override_indication(state)
        disch1_eng3_1.set_override_indication(state)
        disch2_eng3.set_override_indication(state)
        disch2_eng3_1.set_override_indication(state)

        fire_apu_indicator.set_override_indication(state)
        fire_apu_indicator.set_override_indication(state)
        fire_apu_closed_indicator.set_override_indication(state)
        apu_disch.set_override_indication(state)
        firebagcomp_indicator.set_override_indication(state)
        firebagcomp_button.set_override_indication(state)
        firerearcomp_button.set_override_indication(state)
        firerearcomp_indicator.set_override_indication(state)

        pc.pc_thrust_red_light_1.set_override_indication(state)
        pc.pc_thrust_red_light_2.set_override_indication(state)
        pc.pc_thrust_red_light_3.set_override_indication(state)
