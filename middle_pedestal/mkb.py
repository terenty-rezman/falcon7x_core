from common.instrument_panel import add_to_panel, TwoStateButton, Indicator, PushButton, NLocalStateButton, LocalStateIndicator, FloatStepper
        

@add_to_panel
class mkb_a_rh(NLocalStateButton):
    states = [0, 1]
    state = 0

    @classmethod
    async def click(cls):
        await super().click()


@add_to_panel
class mkb_b_rh(NLocalStateButton):
    states = [0, 1]
    state = 0

    @classmethod
    async def click(cls):
        await super().click()


@add_to_panel
class mkb_c_rh(NLocalStateButton):
    states = [0, 1]
    state = 0

    @classmethod
    async def click(cls):
        await super().click()
