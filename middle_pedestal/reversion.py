from common.instrument_panel import add_to_panel, TwoStateButton, Indicator, PushButton, NLocalStateButton, LocalStateIndicator, FloatStepper
        

@add_to_panel
class rev_ads_lh(NLocalStateButton):
    states = [0, 1, 2, 3]
    state = 0

    @classmethod
    async def click(cls):
        await super().click()


@add_to_panel
class rev_ads_rh(rev_ads_lh):
    pass


@add_to_panel
class rev_irs_lh(NLocalStateButton):
    states = [0, 1, 2]
    state = 0

    @classmethod
    async def click(cls):
        await super().click()


@add_to_panel
class rev_irs_rh(rev_irs_lh):
    pass
