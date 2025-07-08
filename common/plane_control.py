from common.instrument_panel import add_to_panel, TwoStateButton, FloatStepper
from xplane.params import Params, Commands
import xplane.master as xp
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
        lh_state = util.dead_zone(lh_state, pc_bank_lh.logic_left, pc_bank_lh.logic_right, 0.5)

        rh_state = util.dead_zone(cls.state, cls.logic_left, cls.logic_right, 0.5) 

        total = lh_state + rh_state

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
        lh_state = util.dead_zone(lh_state, pc_pitch_lh.logic_left, pc_pitch_lh.logic_right, 0.5)

        rh_state = util.dead_zone(cls.state, cls.logic_left, cls.logic_right, 0.5) 

        total = rh_state - lh_state

        await pc_pitch_total.set_state(total)
        

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

    last_uso_state = None

    @classmethod
    async def set_state(cls, state: float):
        cls.last_uso_state = state

        auto_throttle_enabled = xp_ac.ACState.get_curr_param(Params["sim/cockpit2/autopilot/autothrottle_enabled"])
        if auto_throttle_enabled is None:
            return

        if auto_throttle_enabled == 0:
            await super().set_state(state)
    
    @classmethod
    def get_uso_state(cls):
        return cls.last_uso_state


@add_to_panel
class pc_throttle_2(pc_throttle_1):
    dataref = Params["sim/cockpit2/engine/actuators/throttle_ratio[1]"]
    last_uso_state = None


@add_to_panel
class pc_throttle_3(pc_throttle_1):
    dataref = Params["sim/cockpit2/engine/actuators/throttle_ratio[2]"]
    last_uso_state = None


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
        state = 1 if state > 0.5 else 0
        cls.state = state


@add_to_panel
class pc_parkbrake_full:
    state = 0
    filter_sum = 0
    last_enabled = None

    @classmethod
    async def set_state(cls, state):
        # float to int
        state = 1 if state > 0.5 else 0

        cls.state = state

        half_state = pc_parkbrake_half.state
        dx = 1 if cls.state or half_state else -1  

        # filter
        cls.filter_sum += dx
        cls.filter_sum = min(0, cls.filter_sum)
        cls.filter_sum = max(40, cls.filter_sum)

        enabled = 1 if cls.filter_sum > 20 else 0

        if cls.last_enabled is None:
            await pc_parkbrake.set_state(enabled)
        elif cls.last_enabled != enabled :
            await pc_parkbrake.set_state(enabled)

        cls.last_enabled = enabled 


@add_to_panel
class pc_gear(TwoStateButton):
    dataref: Params = Params["sim/cockpit2/controls/gear_handle_down"]
    states = [0, 1]


@add_to_panel
class pc_gear_float(FloatStepper):
    dataref = None
    logic_left = 0
    logic_right = 1
    step = 0.01

    val_type = float

    @classmethod
    async def set_state(cls, state: float):
        await super().set_state(state)

        gear = 0
        if state > 0.5:
            gear = 1

        await pc_gear.set_state(gear)


@add_to_panel
class pc_thrust_reverse(FloatStepper):
    dataref = None
    logic_left = 0
    logic_right = 2
    step = 0.01
    val_type = float

    dataref_revers_deployed = Params["sim/cockpit2/annunciators/reverser_deployed"]
    old_state_reverse_on = None

    @classmethod
    async def set_state(cls, state: float):
        reverse_deployed = xp_ac.ACState.get_curr_param(cls.dataref_revers_deployed)
        if reverse_deployed is None:
            return

        reverse_deployed = True if reverse_deployed else False
        
        if cls.old_state_reverse_on is None:
            cls.old_state_reverse_on = reverse_deployed

        new_state = True if state > 0.5 else False

        if new_state == cls.old_state_reverse_on:
            return

        await xp.run_command_once(Commands["sim/engines/thrust_reverse_toggle"])
        
        cls.old_state_reverse_on = new_state


