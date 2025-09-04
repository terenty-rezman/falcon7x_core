from common.instrument_panel import add_to_panel, TwoStateButton, Indicator, PushButton, NLocalStateButton, LocalStateIndicator, FloatStepper
        

@add_to_panel
class rev_ads_left(NLocalStateButton):
    states = [0, 1, 2, 3]
    state = 0

    @classmethod
    async def click(cls):
        await super().click()


@add_to_panel
class rev_ads_right(NLocalStateButton):
    states = [0, 1, 2, 3]
    state = 0

    @classmethod
    async def click(cls):
        await super().click()
