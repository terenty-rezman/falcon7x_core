from common.instrument_panel import add_to_panel, TwoStateButton, ThreeStateButton, FloatSwitch, DiscreteSwitch
import xplane.master as xp


@add_to_panel
class dump(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/cockpit2/pressurization/actuators/dump_to_altitude_on"]


@add_to_panel
class bag_vent(ThreeStateButton):
    dataref: xp.Params = xp.Params["sim/weapons/mis_thrust2"]
    states = [3, 0, 1]
    index = 0 


@add_to_panel
class bag_vent_on(bag_vent):
    @classmethod
    def get_state(cls):
        return super().get_state() == 2


@add_to_panel
class bag_vent_off(bag_vent):
    @classmethod
    def get_state(cls):
        return super().get_state() == 1


@add_to_panel
class cabin_alt(DiscreteSwitch):
    dataref: xp.Params = xp.Params["sim/weapons/mis_thrust2"]
    states = [0, 1, -1]
    index = 15

    climb_digit = 0
    descend_digit = 0

    @classmethod
    async def set_state(cls, state):
        if pressu_man.get_state() == 0: 
            return 
        
        if state is None:
            if cls.climb_digit == 0 and cls.descend_digit == 0:
                state = 1
            elif cls.descend_digit == 1:
                state = 2
            else:
                state = 0
            
        await super().set_state(state)

        if state == 1:
            await xp.run_command_once(xp.Commands["sim/pressurization/vvi_up"])
        elif state == 2:
            await xp.run_command_once(xp.Commands["sim/pressurization/vvi_down"])


@add_to_panel
class cabin_alt_climb():
    @classmethod
    async def set_state(cls, state):
        cabin_alt.climb_digit = state 
        await cabin_alt.set_state(None)


@add_to_panel
class cabin_alt_descent():
    @classmethod
    async def set_state(cls, state):
        cabin_alt.descend_digit = state 
        if state == 1:
            await cabin_alt.set_state(None)


@add_to_panel
class pressu_man(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/weapons/mis_thrust2"]
    index = 16
