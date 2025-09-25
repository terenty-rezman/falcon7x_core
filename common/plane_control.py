from common.instrument_panel import add_to_panel, TwoStateButton, FloatStepper, NLocalStateButton
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
        lh_state = util.dead_zone(lh_state, pc_bank_lh.logic_left, pc_bank_lh.logic_right, 1)

        rh_state = util.dead_zone(cls.state, cls.logic_left, cls.logic_right, 1)

        total = lh_state + rh_state

        await pc_bank_total.set_state(total) 
        #await pc_bank_total.set_state(0)


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
        lh_state = util.dead_zone(lh_state, pc_pitch_lh.logic_left, pc_pitch_lh.logic_right, 1)

        rh_state = util.dead_zone(cls.state, cls.logic_left, cls.logic_right, 1) 

        total = rh_state - lh_state

        await pc_pitch_total.set_state(total) 
        #await pc_pitch_total.set_state(0)
        

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

        #lh_state = pc_heading_lh.get_state()
        total = cls.state

        total = util.dead_zone(total, cls.logic_left, cls.logic_right, 1)

        await pc_heading_total.set_state(total)
        #await pc_heading_total.set_state(0)


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
    old_value = False

    @classmethod
    async def set_state(cls, state: float):
        await super().set_state(state)

        lh_state = pc_left_brake_lh.get_state()
        total =  cls.state + lh_state
        total = util.dead_zone(total, cls.logic_left, cls.logic_right, 1)

        # hysteresis
        new_val = True if total > 5 else cls.old_value
        new_val = False if total < 3 else cls.old_value

        if new_val == cls.old_value:
            return
        
        cls.old_value = new_val

        print(cls, new_val)
        
        if new_val:
            await xp.begin_command(Commands["sim/flight_controls/left_brake"])
        else:
            await xp.end_command(Commands["sim/flight_controls/left_brake"])


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
    old_value = False

    @classmethod
    async def set_state(cls, state: float):
        await super().set_state(state)

        lh_state = pc_right_brake_lh.get_state()
        total =  cls.state + lh_state
        total = util.dead_zone(total, cls.logic_left, cls.logic_right, 1)

        # hysteresis
        new_val = True if total > 5 else cls.old_value
        new_val = False if total < 3 else cls.old_value

        if new_val == cls.old_value:
            return
        
        cls.old_value = new_val

        print(cls, new_val)
        
        if new_val:
            await xp.begin_command(Commands["sim/flight_controls/right_brake"])
        else:
            await xp.end_command(Commands["sim/flight_controls/right_brake"])


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

        if not auto_throttle_enabled:
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
        if state == 0:
            await xp.set_param(cls.dataref, cls.states[0])
            await cas.remove_message(cas.PARK_BRAKE_ON)
        else:
            await xp.set_param(cls.dataref, cls.states[1])
            await cas.show_message(cas.PARK_BRAKE_ON)
    
    @classmethod
    def get_state(cls):
        val = xp_ac.ACState.get_curr_param(cls.dataref) or 0
        if val < 0.05:
            state = 0
        else:
            state = 1

        return state


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
        cls.filter_sum = min(40, cls.filter_sum)
        cls.filter_sum = max(0, cls.filter_sum)

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
    dataref_xp = xp.Params["sim/cockpit2/annunciators/reverser_deployed"]

    logic_left = 0
    logic_right = 2   

    step = 0.01
    val_type = float

    filter_sum = 0
    old_state = False

    skip_steps = 0

    @classmethod
    async def set_state(cls, state: float):
        if cls.skip_steps > 0:
            cls.skip_steps -= 1
            return

        dx = 1 if state > 1 else -1  

        # filter
        cls.filter_sum += dx
        cls.filter_sum = min(40, cls.filter_sum)
        cls.filter_sum = max(0, cls.filter_sum)

        xp_state = xp.ACState.get_curr_param(cls.dataref_xp) or 0
        cls.state = 1 if xp_state == 7 else 0
        new_state = cls.state

        # гистерезис
        if cls.filter_sum > 25:
            new_state = True

        if cls.filter_sum < 15:
            new_state = False

        if new_state == cls.state:
            return

        print(cls, new_state)

        await xp.run_command_once(Commands["sim/engines/thrust_reverse_toggle"])
        cls.skip_steps = 40 

    @classmethod
    async def get_state(cls):
        state = xp.ACState.get_curr_param(cls.dataref_xp) or 0
        cls.state = 1 if state == 7 else 0
        return cls.state

@add_to_panel
class pc_thrust_red_light_1(NLocalStateButton):
    states = [0, 1]
    state = 0

@add_to_panel
class pc_thrust_red_light_2(NLocalStateButton):
    states = [0, 1]
    state = 0


@add_to_panel
class pc_thrust_red_light_3(NLocalStateButton):
    states = [0, 1]
    state = 0
