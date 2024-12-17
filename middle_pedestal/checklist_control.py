from common.instrument_panel import add_to_panel, TwoStateButton, Indicator, PushButton, NLocalStateButton, LocalStateIndicator, FloatStepper
        

@add_to_panel
class clc_undo_lh(PushButton):
    @classmethod
    async def click(cls):
        pass


@add_to_panel
class clc_ent_lh(PushButton):
    @classmethod
    async def click(cls):
        pass


@add_to_panel
class clc_next_lh(PushButton):
    @classmethod
    async def click(cls):
        pass


@add_to_panel
class clc_prev_lh(PushButton):
    @classmethod
    async def click(cls):
        pass


@add_to_panel
class clc_cl_lh(PushButton):
    @classmethod
    async def click(cls):
        pass


@add_to_panel
class clc_undo_rh(clc_undo_lh):
    pass


@add_to_panel
class clc_ent_rh(clc_ent_lh):
    pass


@add_to_panel
class clc_next_rh(clc_next_lh):
    pass


@add_to_panel
class clc_prev_rh(clc_prev_lh):
    pass


@add_to_panel
class clc_cl_rh(clc_cl_lh):
    pass

