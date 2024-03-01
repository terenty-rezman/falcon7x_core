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


@add_to_overhead_panel
class cabin_alt(DiscreteSwitch):
    dataref: xp.Params = xp.Params["sim/weapons/mis_thrust2"]
    states = [0, 1, -1]
    index = 15

    @classmethod
    async def set_state(cls, state):
        if pressu_man.get_state() == 0: 
            return 
            
        await super().set_state(state)

        if state == 1:
            await xp.run_command_once(xp.Commands["sim/pressurization/vvi_up"])
        elif state == 2:
            await xp.run_command_once(xp.Commands["sim/pressurization/vvi_down"])


@add_to_overhead_panel
class pressu_man(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/weapons/mis_thrust2"]
    index = 16
