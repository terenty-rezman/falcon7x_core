from instrument_panel import add_to_panel, TwoStateButton, ThreeStateButton, FloatSwitch, DiscreteSwitch
import xplane as xp


@add_to_panel
class bleed1(ThreeStateButton):
    dataref: xp.Params = xp.Params["sim/weapons/mis_thrust2"]
    states = [1, 2, 0]
    index = 18

    @classmethod
    async def set_state(cls, state):
        await super().set_state(state)

        await xp.run_command_once(xp.Commands["sim/bleed_air/bleed_air_left"])


@add_to_panel
class bleed1_off(bleed1):
    @classmethod
    def get_state(cls):
        return super().get_state() == 2


@add_to_panel
class bleed1_hpoff(bleed1):
    @classmethod
    def get_state(cls):
        return super().get_state() == 1


@add_to_panel
class bleed12(ThreeStateButton):
    dataref: xp.Params = xp.Params["sim/weapons/mis_thrust2"]
    states = [2, 0, 1]
    index = 2 


@add_to_panel
class bleed12_on(bleed12):
    @classmethod
    def get_state(cls):
        return super().get_state() == 2


@add_to_panel
class bleed12_off(bleed12):
    @classmethod
    def get_state(cls):
        return super().get_state() == 1


@add_to_panel
class bleed2(ThreeStateButton):
    dataref: xp.Params = xp.Params["sim/weapons/mis_thrust2"]
    states = [1, 2, 0]
    index = 17

    @classmethod
    async def set_state(cls, state):
        await super().set_state(state)

        await xp.run_command_once(xp.Commands["sim/bleed_air/bleed_air_auto"])


@add_to_panel
class bleed2_hpoff(bleed2):
    @classmethod
    def get_state(cls):
        return super().get_state() == 1


@add_to_panel
class bleed2_off(bleed2):
    @classmethod
    def get_state(cls):
        return super().get_state() == 2


@add_to_panel
class bleed13(ThreeStateButton):
    dataref: xp.Params = xp.Params["sim/weapons/mis_thrust2"]
    states = [2, 0, 1]
    index = 1 


@add_to_panel
class bleed13_on(bleed13):
    @classmethod
    def get_state(cls):
        return super().get_state() == 2


@add_to_panel
class bleed13_off(bleed13):
    @classmethod
    def get_state(cls):
        return super().get_state() == 1


@add_to_panel
class bleed_apu(ThreeStateButton):
    dataref: xp.Params = xp.Params["sim/custom/7x/overAPUaction"]
    states = [1, 2, 0]


@add_to_panel
class bleed_apu_on(bleed_apu):
    @classmethod
    def get_state(cls):
        return super().get_state() == 1


@add_to_panel
class bleed_apu_off(bleed_apu):
    @classmethod
    def get_state(cls):
        return super().get_state() == 2


@add_to_panel
class bleed3(ThreeStateButton):
    dataref: xp.Params = xp.Params["sim/weapons/mis_thrust2"]
    states = [1, 2, 0]
    index = 19

    @classmethod
    async def set_state(cls, state):
        await super().set_state(state)

        await xp.run_command_once(xp.Commands["sim/bleed_air/bleed_air_right"])
