from common.instrument_panel import add_to_panel, TwoStateButton, FloatStepper
from xplane.params import Params
import common.xp_aircraft_state as xp_ac
import common.util as util
import math

import cas.cas as cas


@add_to_panel
class pc_bank_lh(FloatStepper):
    dataref = None
    logic_left = -10.0
    logic_right = 10.0
    step = 0.01

    val_type = float


@add_to_panel
class pc_bank_rh(FloatStepper):
    dataref = None
    logic_left = -10.0
    logic_right = 10.0
    step = 0.01

    val_type = float

    @classmethod
    async def set_state(cls, state: float):
        await super().set_state(state)

        lh_state = pc_bank_lh.get_state()

        total = cls.state + lh_state
        total = util.dead_zone(total, cls.logic_left, cls.logic_right, 0.5)

        await pc_bank_total.set_state(total)


@add_to_panel
class pc_bank_total(FloatStepper):
    dataref = Params["sim/joystick/yoke_roll_ratio"]

    logic_left = -10.0
    logic_right = 10.0
    left_most_value = -1.0 
    right_most_value = 1.0
    step = 0.01

    val_type = float


@add_to_panel
class pc_pitch_lh(FloatStepper):
    dataref = None
    logic_left = -10.0
    logic_right = 10.0
    step = 0.01

    val_type = float


@add_to_panel
class pc_pitch_rh(FloatStepper):
    dataref = None
    logic_left = -10.0
    logic_right = 10.0
    step = 0.01

    val_type = float

    @classmethod
    async def set_state(cls, state: float):
        await super().set_state(state)

        lh_state = pc_pitch_lh.get_state()
        await pc_pitch_total.set_state(
            cls.state - lh_state
        )
        

@add_to_panel
class pc_pitch_total(FloatStepper):
    dataref = Params["sim/joystick/yoke_pitch_ratio"]

    logic_left = -10.0
    logic_right = 10.0
    left_most_value = -1.0 
    right_most_value = 1.0
    step = 0.01

    val_type = float


@add_to_panel
class pc_heading_lh(FloatStepper):
    dataref = None

    logic_left = -10.0
    logic_right = 10.0
    left_most_value = -1.0 
    right_most_value = 1.0
    step = 0.01

    val_type = float


@add_to_panel
class pc_heading_rh(FloatStepper):
    dataref = None

    logic_left = -10.0
    logic_right = 10.0
    left_most_value = -1.0
    right_most_value = 1.0
    step = 0.01

    val_type = float

    @classmethod
    async def set_state(cls, state: float):
        await super().set_state(state)

        lh_state = pc_heading_lh.get_state()
        total = cls.state + lh_state

        total = util.dead_zone(total, cls.logic_left, cls.logic_right, 1)

        await pc_heading_total.set_state(total)


@add_to_panel
class pc_heading_total(FloatStepper):
    dataref = Params["sim/joystick/yoke_heading_ratio"]

    logic_left = -10.0
    logic_right = 10.0
    left_most_value = -1.0
    right_most_value = 1.0
    step = 0.01

    val_type = float


@add_to_panel
class pc_left_brake_lh(FloatStepper):
    dataref = None

    logic_left = 0.0
    logic_right = 10.0
    left_most_value = 0
    right_most_value = 1.0
    step = 0.01

    val_type = float


@add_to_panel
class pc_left_brake_rh(FloatStepper):
    dataref = None

    logic_left = 0.0
    logic_right = 10.0
    left_most_value = 0
    right_most_value = 1.0
    step = 0.01

    val_type = float

    @classmethod
    async def set_state(cls, state: float):
        await super().set_state(state)

        lh_state = pc_left_brake_lh.get_state()
        await pc_left_brake_total.set_state(
            cls.state + lh_state
        )


@add_to_panel
class pc_left_brake_total(FloatStepper):
    dataref = Params["sim/cockpit2/controls/left_brake_ratio"]

    logic_left = 0.0
    logic_right = 10.0
    left_most_value = 0
    right_most_value = 1.0
    step = 0.01

    val_type = float


@add_to_panel
class pc_right_brake_lh(FloatStepper):
    dataref = None

    logic_left = 0.0
    logic_right = 10.0
    left_most_value = 0
    right_most_value = 1.0
    step = 0.01

    val_type = float


@add_to_panel
class pc_right_brake_rh(FloatStepper):
    dataref = None

    logic_left = 0.0
    logic_right = 10.0
    left_most_value = 0
    right_most_value = 1.0
    step = 0.01

    val_type = float

    @classmethod
    async def set_state(cls, state: float):
        await super().set_state(state)

        lh_state = pc_right_brake_lh.get_state()
        await pc_right_brake_total.set_state(
            cls.state + lh_state
        )


@add_to_panel
class pc_right_brake_total(FloatStepper):
    dataref = Params["sim/cockpit2/controls/right_brake_ratio"]

    logic_left = 0.0
    logic_right = 10.0
    left_most_value = 0
    right_most_value = 1.0
    step = 0.01

    val_type = float



@add_to_panel
class pc_throttle_1(FloatStepper):
    dataref = Params["sim/cockpit2/engine/actuators/throttle_ratio[0]"]

    logic_left = 0
    logic_right = 10.0
    left_most_value = 0
    right_most_value = 1.0
    step = 0.01

    val_type = float


@add_to_panel
class pc_throttle_2(pc_throttle_1):
    dataref = Params["sim/cockpit2/engine/actuators/throttle_ratio[1]"]


@add_to_panel
class pc_throttle_3(pc_throttle_1):
    dataref = Params["sim/cockpit2/engine/actuators/throttle_ratio[2]"]


@add_to_panel
class pc_parkbrake(TwoStateButton):
    dataref: Params = Params["sim/flightmodel/controls/parkbrake"]
    states = [0, 0.284685]

    @classmethod
    async def set_state(cls, state):
        await super().set_state(state)

        if state == 0:
            await cas.remove_message(cas.PARK_BRAKE_ON)
        else:
            await cas.show_message(cas.PARK_BRAKE_ON)


@add_to_panel
class pc_parkbrake_half:
    state = 0

    @classmethod
    async def set_state(cls, state):
        cls.state = state

        if cls.state == 1:
            await pc_parkbrake.set_state(1)
        elif pc_parkbrake_full.state == 0:
            await pc_parkbrake.set_state(0)


@add_to_panel
class pc_parkbrake_full:
    state = 0

    @classmethod
    async def set_state(cls, state):
        cls.state = state

        if cls.state == 1:
            await pc_parkbrake.set_state(1)
        elif pc_parkbrake_half.state == 0:
            await pc_parkbrake.set_state(0)


@add_to_panel
class pc_gear(TwoStateButton):
    dataref: Params = Params["sim/cockpit2/controls/gear_handle_down"]
    states = [0, 1]
