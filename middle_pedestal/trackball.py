from common.instrument_panel import add_to_panel, TwoStateButton, Indicator, PushButton, NLocalStateButton, LocalStateIndicator, FloatStepper
import synoptic_remote.synoptic_connection as synoptic
        
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
        await synoptic.send_button_click("tb_menu_lh")


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
class tb_menu_rh(PushButton):
    @classmethod
    async def click(cls):
        await synoptic.send_button_click("tb_menu_rh")


@add_to_panel
class tb_set_top_lh(FloatStepper):
    dataref = None
    logic_left = -10.0
    logic_right = 10.0
    step = 0.01

    val_type = float


@add_to_panel
class tb_set_bottom_lh(FloatStepper):
    dataref = None
    logic_left = -10.0
    logic_right = 10.0
    step = 0.01

    val_type = float


@add_to_panel
class tb_reserv_lh(NLocalStateButton):
    states = [0, 1]
    state = 0


@add_to_panel
class tb_set_top_rh(FloatStepper):
    dataref = None
    logic_left = -10.0
    logic_right = 10.0
    step = 0.01

    val_type = float


@add_to_panel
class tb_set_bottom_rh(FloatStepper):
    dataref = None
    logic_left = -10.0
    logic_right = 10.0
    step = 0.01

    val_type = float


@add_to_panel
class tb_reserv_rh(NLocalStateButton):
    states = [0, 1]
    state = 0
