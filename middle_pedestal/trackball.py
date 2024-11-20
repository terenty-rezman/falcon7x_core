from instrument_panel import add_to_panel, TwoStateButton, Indicator, PushButton, NLocalStateButton, LocalStateIndicator, FloatStepper
        
# F7X_SDD_Avionics_Vol1.pdf

@add_to_panel
class tb_mic_lh(PushButton):
    @classmethod
    async def click(cls):
        pass


@add_to_panel
class tb_disp_left_lh(PushButton):
    @classmethod
    async def click(cls):
        pass


@add_to_panel
class tb_disp_right_lh(PushButton):
    @classmethod
    async def click(cls):
        pass


@add_to_panel
class tb_disp_up_lh(PushButton):
    @classmethod
    async def click(cls):
        pass


@add_to_panel
class tb_disp_down_lh(PushButton):
    @classmethod
    async def click(cls):
        pass


@add_to_panel
class tb_menu_lh(PushButton):
    @classmethod
    async def click(cls):
        pass


@add_to_panel
class tb_mic_rh(tb_mic_lh):
    pass


@add_to_panel
class tb_disp_left_rh(tb_disp_left_lh):
    pass


@add_to_panel
class tb_disp_right_rh(tb_disp_right_lh):
    pass


@add_to_panel
class tb_disp_up_rh(tb_disp_up_lh):
    pass


@add_to_panel
class tb_disp_down_rh(tb_disp_down_lh):
    pass


@add_to_panel
class tb_menu_rh(tb_menu_lh):
    pass
