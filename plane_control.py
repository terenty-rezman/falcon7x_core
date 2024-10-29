from instrument_panel import add_to_panel, TwoStateButton, Indicator, PushButton, NLocalStateButton, LocalStateIndicator, FloatStepper
import xplane as xp
import xp_aircraft_state as xp_ac
import util


@add_to_panel
class pc_bank_lh(FloatStepper):
    dataref = xp.Params["sim/joystick/yoke_roll_ratio"]

    logic_left = -10.0
    logic_right = 10.0
    left_most_value = -1.0 
    right_most_value = 1.0
    step = 0.01

    val_type = float


@add_to_panel
class pc_pitch_lh(FloatStepper):
    dataref = xp.Params["sim/joystick/yoke_pitch_ratio"]

    logic_left = -1.0
    logic_right = 1.0
    left_most_value = -1.0 
    right_most_value = 1.0
    step = 0.01

    val_type = float


@add_to_panel
class pc_heading_lh(FloatStepper):
    dataref = xp.Params["sim/joystick/yoke_heading_ratio"]

    logic_left = -1.0
    logic_right = 1.0
    left_most_value = -1.0 
    right_most_value = 1.0
    step = 0.01

    val_type = float


@add_to_panel
class pc_left_brake_lh(FloatStepper):
    dataref = xp.Params["sim/cockpit2/controls/left_brake_ratio"]

    logic_left = -1.0
    logic_right = 1.0
    left_most_value = 0
    right_most_value = 1.0
    step = 0.01

    val_type = float

@add_to_panel
class pc_right_brake_lh(FloatStepper):
    dataref = xp.Params["sim/cockpit2/controls/right_brake_ratio"]

    logic_left = -1.0
    logic_right = 1.0
    left_most_value = 0
    right_most_value = 1.0
    step = 0.01

    val_type = float


@add_to_panel
class pc_left_brake_rh(pc_left_brake_lh):
    pass

@add_to_panel
class pc_right_brake_rh(pc_right_brake_lh):
    pass


@add_to_panel
class pc_heading_rh(pc_heading_lh):
    pass


@add_to_panel
class pc_bank_rh(pc_bank_lh):
    pass


@add_to_panel
class pc_pitch_rh(pc_pitch_lh):
    pass


@add_to_panel
class pc_throttle_1(FloatStepper):
    dataref = xp.Params["sim/cockpit2/engine/actuators/throttle_ratio"]
    index = 0

    logic_left = -1.0
    logic_right = 1.0
    left_most_value = 0
    right_most_value = 1.0
    step = 0.01

    val_type = float


@add_to_panel
class pc_throttle_2(pc_throttle_1):
    index = 1


@add_to_panel
class pc_throttle_3(pc_throttle_1):
    index = 2
