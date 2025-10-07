from common.instrument_panel import add_to_panel, TwoStateButton, Indicator, NStateXPButton, NLocalStateButton, LocalStateIndicator, FloatStepper
import xplane.master as xp

@add_to_panel
class rev_ads_lh(NStateXPButton):
    dataref = xp.Params["sim/custom/7x/z_ads_pilot"]

    states = [1, 2, 3]
    state = 1

    @classmethod
    async def click(cls):
        state = cls.get_state()
        if state is None:
            return

        if state == 0:
            await cls.set_state(2) 
        else:
            await cls.set_state(state - 1)


@add_to_panel
class rev_ads_rh(NStateXPButton):
    dataref = xp.Params["sim/custom/7x/z_ads_copilot"]
    states = [1, 2, 3]
    state = 1


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


@add_to_panel
class rev_fms_lh(NLocalStateButton):
    states = [0, 1]
    state = 0

    @classmethod
    async def click(cls):
        await super().click()


@add_to_panel
class rev_fms_rh(rev_fms_lh):
    pass


@add_to_panel
class rev_ra_lh(NLocalStateButton):
    states = [0, 1]
    state = 0

    @classmethod
    async def click(cls):
        await super().click()


@add_to_panel
class rev_ra_rh(rev_ra_lh):
    pass


@add_to_panel
class rev_ils_vor_lh(NLocalStateButton):
    states = [0, 1]
    state = 0

    @classmethod
    async def click(cls):
        await super().click()


@add_to_panel
class rev_ils_vor_rh(rev_ils_vor_lh):
    pass


@add_to_panel
class rev_pdu_mdu(NLocalStateButton):
    states = [0, 1]
    state = 0

    @classmethod
    async def click(cls):
        await super().click()
