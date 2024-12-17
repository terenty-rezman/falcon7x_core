from common.instrument_panel import add_to_panel, TwoStateButton, Indicator, PushButton, NLocalStateButton, LocalStateIndicator, FloatStepper
        
# F7X_SDD_Avionics_Vol1.pdf 31-2


@add_to_panel
class ep_aural_warn_1(NLocalStateButton):
    states = [0, 1]
    state = 0

    @classmethod
    async def set_state(cls, state):
        await super().set_state(state)


@add_to_panel
class ep_aural_warn_2(NLocalStateButton):
    states = [0, 1]
    state = 0

    @classmethod
    async def set_state(cls, state):
        await super().set_state(state)


@add_to_panel
class ep_bag_fan(NLocalStateButton):
    states = [0, 1]
    state = 0

    @classmethod
    async def set_state(cls, state):
        await super().set_state(state)


@add_to_panel
class ep_elec_rh_ess(NLocalStateButton):
    states = [0, 1]
    state = 0

    @classmethod
    async def click(cls):
        await super().click()


@add_to_panel
class ep_fuel_2_bu(NLocalStateButton):
    states = [0, 1]
    state = 0

    @classmethod
    async def set_state(cls, state):
        await super().set_state(state)


@add_to_panel
class ep_rat_auto(NLocalStateButton):
    states = [0, 1]
    state = 0

    @classmethod
    async def set_state(cls, state):
        await super().set_state(state)


@add_to_panel
class ep_trim_emerg(NLocalStateButton):
    states = [0, 1]
    state = 0

    @classmethod
    async def set_state(cls, state):
        await super().set_state(state)
