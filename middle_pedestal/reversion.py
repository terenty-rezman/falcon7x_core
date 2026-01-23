import math

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
class rev_irs_lh(NStateXPButton):
    dataref = xp.Params["sim/custom/7x/z_irs_pilot"]
    states = [1, 2, 3]
    state = 0


@add_to_panel
class rev_irs_rh(NStateXPButton):
    dataref = xp.Params["sim/custom/7x/z_irs_copilot"]
    states = [1, 2, 3]
    state = 0


@add_to_panel
class rev_fms_lh(NStateXPButton):
    dataref = xp.Params["sim/custom/7x/z_fms_pilot"]

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
class rev_fms_rh(NStateXPButton):
    dataref = xp.Params["sim/custom/7x/z_fms_copilot"]
    states = [1, 2, 3]
    state = 1


@add_to_panel
class rev_ra_lh(NStateXPButton):
    dataref = xp.Params["sim/custom/7x/z_ra_pilot"]
    states = [1, 2]
    state = 0


@add_to_panel
class rev_ra_rh(NStateXPButton):
    dataref = xp.Params["sim/custom/7x/z_ra_copilot"]
    states = [1, 2]
    state = 0


@add_to_panel
class rev_ils_vor_lh(NStateXPButton):
    dataref = xp.Params["sim/custom/7x/z_vor_pilot"]
    states = [1, 2]
    state = 0


@add_to_panel
class rev_ils_vor_rh(NStateXPButton):
    dataref = xp.Params["sim/custom/7x/z_vor_copilot"]
    states = [1, 2]
    state = 0


@add_to_panel
class rev_pdu_mdu(NLocalStateButton):
    states = [0, 1]
    state = 0

    @classmethod
    async def click(cls):
        await super().click()


@add_to_panel
class rev_dim_1(FloatStepper):
    dataref: xp.Params = xp.Params["sim/custom/7x/z_left_screen_brightness"]

    logic_left = 0
    logic_right = 10.0

    left_most_value = 0
    right_most_value = 100

    step = 0.01
    state = 0

    OUTPUT = 0
    uso_receive_dt = 0.01
    T = 0.5

    @classmethod
    async def set_state(cls, state: float):
        if not math.isclose(state, cls.OUTPUT, abs_tol=0.1):
            cls.OUTPUT = state

            state = min(max(cls.logic_left, state), cls.logic_right)

            cls.state = state

            # from [logic_left logic_right] to [0 1]
            val_01 = (state - cls.logic_left) / (cls.logic_right - cls.logic_left)

            xp_val = (cls.right_most_value - cls.left_most_value) * val_01 + cls.left_most_value
            xp_val = int(xp_val)

            await xp.set_param(cls.dataref, xp_val)

        # x_i = cls.OUTPUT
        # y = state
        # x_i_1 = x_i + (y - x_i) / cls.T * cls.uso_receive_dt

        # if not math.isclose(x_i_1, cls.OUTPUT, abs_tol=0.1):
        #     cls.OUTPUT = x_i_1

        #     state = min(max(cls.logic_left, state), cls.logic_right)

        #     cls.state = state

        #     # from [logic_left logic_right] to [0 1]
        #     val_01 = (state - cls.logic_left) / (cls.logic_right - cls.logic_left)

        #     xp_val = (cls.right_most_value - cls.left_most_value) * val_01 + cls.left_most_value
        #     xp_val = int(xp_val)

        #     await xp.set_param(cls.dataref, xp_val)


@add_to_panel
class rev_dim_2(rev_dim_1):
    dataref: xp.Params = xp.Params["sim/custom/7x/z_up_screen_brightness"]

    state = 0

    OUTPUT = 0
    uso_receive_dt = 0.01
    T = 0.5


@add_to_panel
class rev_dim_3(rev_dim_1):
    dataref: xp.Params = xp.Params["sim/custom/7x/z_right_screen_brightness"]

    state = 0

    OUTPUT = 0
    uso_receive_dt = 0.01
    T = 0.5


@add_to_panel
class rev_dim_4(rev_dim_1):
    dataref: xp.Params = xp.Params["sim/custom/7x/z_down_screen_brightness"]

    state = 0

    OUTPUT = 0
    uso_receive_dt = 0.01
    T = 0.5


@add_to_panel
class rev_dim_4(rev_dim_1):
    dataref: xp.Params = xp.Params["sim/custom/7x/z_mini_screen_brightness"]

    state = 0

    OUTPUT = 0
    uso_receive_dt = 0.01
    T = 0.5
