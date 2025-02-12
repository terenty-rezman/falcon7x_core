from common.instrument_panel import add_to_panel, TwoStateButton, Indicator, PushButton, NLocalStateButton, LocalStateIndicator, FloatStepper, array_str
import xplane.master as xp
        
# F7X_SDD_Avionics_Vol1.pdf

@add_to_panel
class en_motor(TwoStateButton):
    @classmethod
    async def set_state(cls, state):
        pass


@add_to_panel
class en_ign(TwoStateButton):
    @classmethod
    async def set_state(cls, state):
        pass


@add_to_panel
class en_normal(TwoStateButton):
    @classmethod
    async def set_state(cls, state):
        pass


@add_to_panel
class en_start(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/weapons/warhead_type"]
    states = [0, 1]
    index = 3

    # @classmethod
    # async def set_state(cls, state):
    #     val = array_str(3, state) 
    #     await xp.set_param(xp.Params["sim/weapons/warhead_type"], val)


@add_to_panel
class en_fuel_1(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/weapons/warhead_type"]
    states = [0, 1]
    index = 0


@add_to_panel
class en_fuel_2(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/weapons/warhead_type"]
    states = [0, 1]
    index = 1


@add_to_panel
class en_fuel_3(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/weapons/warhead_type"]
    states = [0, 1]
    index = 2
