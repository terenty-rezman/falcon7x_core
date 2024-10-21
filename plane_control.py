from instrument_panel import add_to_panel, TwoStateButton, Indicator, PushButton, NLocalStateButton, LocalStateIndicator, FloatStepper
import xplane as xp
import xp_aircraft_state as xp_ac
import util


@add_to_panel
class pc_bank_lh(FloatStepper):
    dataref = xp.Params["sim/joystick/yoke_roll_ratio"]

    left_most_value = -1.0 
    right_most_value = 1.0
    step = 0.01

    val_type = float


@add_to_panel
class pc_pitch_lh(FloatStepper):
    dataref = xp.Params["sim/joystick/yoke_pitch_ratio"]

    left_most_value = -1.0 
    right_most_value = 1.0
    step = 0.01

    val_type = float


@add_to_panel
class pc_heading_lh(FloatStepper):
    dataref = xp.Params["sim/joystick/yoke_heading_ratio"]

    left_most_value = -1.0 
    right_most_value = 1.0
    step = 0.01

    val_type = float
