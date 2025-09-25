from common.instrument_panel import add_to_panel, TwoStateButton, Indicator, PushButton, NLocalStateButton, LocalStateIndicator, FloatStepper, array_str
import xplane.master as xp

import overhead_panel.flight_control as fc
        

# @add_to_panel
# class wc_sf_0(TwoStateButton):
#     flaps_val = 0

#     @classmethod
#     async def set_state(cls, state):
#         if state == 1:
#             val = array_str(0, cls.flaps_val) 
#             await xp.set_param(xp.Params["sim/multiplayer/controls/flap_request"], val)

# @add_to_panel
# class wc_sf_1(wc_sf_0):
#     flaps_val = 0.33


# @add_to_panel
# class wc_sf_2(wc_sf_0):
#     flaps_val = 0.66


# @add_to_panel
# class wc_sf_3(wc_sf_0):
#     flaps_val = 1.0


@add_to_panel
class wc_sf(FloatStepper):
    dataref = xp.Params["sim/multiplayer/controls/flap_request"]
    index = 0

    logic_left = 0
    logic_right = 1.0

    left_most_value = 0
    right_most_value = 1.0

    step = 0.01

    val_type = float


@add_to_panel
class wc_backup_slats(NLocalStateButton):
    states = [0, 1]
    state = 0


@add_to_panel
class wc_ab(FloatStepper):
    dataref = xp.Params["sim/cockpit2/controls/speedbrake_ratio"]

    logic_left = 0
    logic_right = 1.0

    left_most_value = 0
    right_most_value = 1.0

    step = 0.01

    val_type = float

    @classmethod
    async def set_state(cls, state: float):
        if fc.airbrake_auto.get_state() == 1:
            return

        await super().set_state(state)


# @add_to_panel
# class wc_ab_0(TwoStateButton):
#     airbrake_val = 0

#     @classmethod
#     async def set_state(cls, state):
#         if state == 1:
#             await xp.set_param(xp.Params["sim/cockpit2/controls/speedbrake_ratio"], cls.airbrake_val)


# @add_to_panel
# class wc_ab_1(wc_ab_0):
#     airbrake_val = 0.5


# @add_to_panel
# class wc_ab_2(wc_ab_0):
#     airbrake_val = 1


@add_to_panel
class wc_trim_pitch_up_lh(PushButton):
    @classmethod
    async def click(cls):
        await xp.run_command_once(xp.Commands["sim/flight_controls/pitch_trim_up"])


@add_to_panel
class wc_trim_pitch_down_lh(PushButton):
    @classmethod
    async def click(cls):
        await xp.run_command_once(xp.Commands["sim/flight_controls/pitch_trim_down"])


@add_to_panel
class wc_trim_pitch_up_rh(wc_trim_pitch_up_lh):
    pass


@add_to_panel
class wc_trim_pitch_down_rh(wc_trim_pitch_down_lh):
    pass


@add_to_panel
class wc_trim_roll_up_lh(PushButton):
    @classmethod
    async def click(cls):
        await xp.run_command_once(xp.Commands["sim/flight_controls/aileron_trim_right"])


@add_to_panel
class wc_trim_roll_down_lh(PushButton):
    @classmethod
    async def click(cls):
        await xp.run_command_once(xp.Commands["sim/flight_controls/aileron_trim_left"])


@add_to_panel
class wc_trim_roll_up_rh(wc_trim_roll_up_lh):
    pass


@add_to_panel
class wc_trim_roll_down_rh(wc_trim_roll_down_lh):
    pass


@add_to_panel
class wc_trim_yaw_up_lh(PushButton):
    @classmethod
    async def click(cls):
        await xp.run_command_once(xp.Commands["sim/flight_controls/rudder_trim_right"])


@add_to_panel
class wc_trim_yaw_down_lh(PushButton):
    @classmethod
    async def click(cls):
        await xp.run_command_once(xp.Commands["sim/flight_controls/rudder_trim_left"])


@add_to_panel
class wc_trim_yaw_up_rh(wc_trim_yaw_up_lh):
    pass


@add_to_panel
class wc_trim_yaw_down_rh(wc_trim_yaw_down_lh):
    pass
