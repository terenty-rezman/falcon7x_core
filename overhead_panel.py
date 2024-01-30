import xplane as xp
import aircraft as ac


def overhead_button(name):
    def add_button(cls):
        OverheadPanel.buttons.setdefault(name, cls)
    return add_button


class Custom(type):
    def __getitem__(self, button_name):
       return self.buttons[button_name] 


class OverheadPanel(metaclass=Custom):
    buttons = {}

    @classmethod
    async def reset_to_default_state(cls):
        await cls["Fireclosed 0"].set_enabled(False)
        await OverheadPanel["dish 2 2 2 2"].set_enabled(False)


class TwoStateButton:
    @classmethod
    async def on_enabled(cls):
        pass

    @classmethod
    async def on_disabled(cls):
        pass
    
    @classmethod
    async def set_enabled(cls, on=True):
        if on:
            await cls.on_enabled()
        else:
            await cls.on_disabled()

    @classmethod
    def get_state(cls):
        pass
        

@overhead_button("Fireclosed 0")
class Fireclosed0(TwoStateButton):
    @classmethod
    async def on_enabled(cls):
        await xp.set_param(xp.Params["sim/weapons/warhead_type"], "[,,,,1]" )

    @classmethod
    async def on_disabled(cls):
        await xp.set_param(xp.Params["sim/weapons/warhead_type"], "[,,,,0]" )

    @classmethod
    def get_state(cls):
        if ac.ACState.param_available("sim/weapons/warhead_type"):
            return ac.ACState.curr_xplane_state["sim/weapons/warhead_type"][4]


@overhead_button("dish 2 2 2 2")
class Dish2222(TwoStateButton):
    @classmethod
    async def on_enabled(cls):
        await xp.set_param(xp.Params["sim/cockpit2/engine/actuators/fire_extinguisher_on"], "[1]" )

    @classmethod
    async def on_disabled(cls):
        await xp.set_param(xp.Params["sim/cockpit2/engine/actuators/fire_extinguisher_on"], "[0]" )

    @classmethod
    def get_state(cls):
        if ac.ACState.param_available("sim/cockpit2/engine/actuators/fire_extinguisher_on"):
            return ac.ACState.curr_xplane_state["sim/cockpit2/engine/actuators/fire_extinguisher_on"][0]
