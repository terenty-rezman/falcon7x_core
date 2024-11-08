import array
import asyncio
from collections import OrderedDict
import math

import xplane as xp
import xp_aircraft_state as xp_ac
from aioudp import open_local_endpoint, open_remote_endpoint

import sane_tasks


def is_rotate_right(new_state, old_state):
    next_state = {
        (0, 0): (0, 1),
        (0, 1): (1, 1),
        (1, 1): (1, 0),
        (1, 0): (0, 0)
    }
    if next_state[old_state] == new_state:
        return True

    return False


def is_rotate_left(new_state, old_state):
    next_state = {
        (0, 0): (1, 0),
        (1, 0): (1, 1),
        (1, 1): (0, 1),
        (0, 1): (0, 0)
    }
    if next_state[old_state] == new_state:
        return True

    return False


def add_to_panel(cls):
    CockpitPanel.buttons.setdefault(cls.__name__, cls)
    return cls


class Custom(type):
    def __getitem__(self, button_name):
       return self.buttons[button_name] 


class CockpitPanel(metaclass=Custom):
    buttons = {}

    @classmethod
    async def reset_to_default_state(cls):
        await cls["firebutton_1"].set_state(0)
    

def array_str(index, val):
    return f"[{',' * index}{val}]"


class PushButton:
    @classmethod
    async def click(cls):
        pass


class NLocalStateButton:
    """ button that has local state and no state in xplane aircraft """

    states = []

    @classmethod
    async def set_state(cls, state):
        if state in cls.states:
            cls.state = state
        else:
            raise Exception("No such state")
    
    @classmethod 
    def get_state(cls):
        return cls.state
    
    @classmethod
    def get_indication(cls):
        return cls.get_state()

    @classmethod
    async def click(cls):
        state = cls.get_state()
        if state is None:
            return

        if state == len(cls.states) - 1:
            await cls.set_state(0) 
        else:
            await cls.set_state(state + 1)

    @classmethod
    async def wait_state(cls, state):
        """ wait on logical state """

        def condition(param_val):
            curr_state = cls.get_state() 
            return curr_state == state

        await xp_ac.ACState.data_condition(condition)


class NStateButton:
    """ N states are logical states: 0, 1, 2, 3, ..., N """

    dataref = None
    states = [] # this values are sent to x plane dref;
    index = None

    @classmethod
    async def set_state(cls, state):
        """ set logical state """

        val = cls.states[state]

        # use "set value in array" syntax if needed; see ExtPlane plugin array syntax
        if cls.index is not None:
            val = array_str(cls.index, val)
        else:
            val = val

        await xp.set_param(cls.dataref, val)
    
    @classmethod 
    def get_state(cls):
        """ get logical state """

        val = xp_ac.ACState.get_curr_param(cls.dataref)
        if val is None or val == []:
            return

        if cls.index is not None:
            val = val[cls.index]

        state = cls.states.index(val)
        return state
    
    @classmethod
    def get_indication(cls):
        return cls.get_state()

    @classmethod
    async def click(cls):
        state = cls.get_state()
        if state is None:
            return

        if state == len(cls.states) - 1:
            await cls.set_state(0) 
        else:
            await cls.set_state(state + 1)

    @classmethod
    async def wait_state(cls, state):
        """ wait on logical state """

        def condition(param_val):
            curr_state = cls.get_state() 
            return curr_state == state

        await xp_ac.ACState.wait_until_parameter_condition(cls.dataref, condition)


class TwoStateButton(NStateButton):
    states = [0, 1]


class ThreeStateButton(NStateButton):
    states = [0, 1, 2]


class Indicator(TwoStateButton):
    @classmethod
    async def set_state(cls, state):
        pass

    @classmethod
    async def click(cls, state):
        pass


class LocalStateIndicator(NLocalStateButton):
    @classmethod
    async def click(cls, state):
        pass


class LocalStateDiscreteSwitch(NLocalStateButton):
    pass


class DiscreteSwitch(NStateButton):
    pass


class FloatSwitch(NStateButton):
    """ swith with continious float state """
    """ logical state actually is int in range of [0 255] """
    """ xp state is float in range of [float_left_most_value float_right_most_value] """

    states = [i for i in range(256)] # these states are not sent to xplane
    float_left_most_value = -1 # float value between left most and right most edge values are sent to xplane
    float_right_most_value = 1

    @classmethod
    async def set_state(cls, state):
        """ set logical state """
        byte_val = cls.states[state]

        # map int [0 255] to float [0.0 1.0]
        float_val = byte_val / 255 

        # map float [0.0 1.0] to [float_left_most_value float_right_most_value]
        xp_val = (cls.float_right_most_value - cls.float_left_most_value) * float_val + cls.float_left_most_value

        # use "set value in array" syntax if needed; see ExtPlane plugin array syntax
        if cls.index is not None:
            xp_val = array_str(cls.index, xp_val)
        else:
            xp_val = xp_val

        await xp.set_param(cls.dataref, xp_val)

    @classmethod 
    def get_state(cls):
        """ get logical state """

        xp_val = xp_ac.ACState.get_curr_param(cls.dataref)
        if xp_val is None or xp_val == []:
            return

        if cls.index is not None:
            xp_val = xp_val[cls.index]
        
        # map xp_val to float val [0.0 1.0]
        float_val = (xp_val - cls.float_left_most_value) / (cls.float_right_most_value - cls.float_left_most_value)
        # map float_val [0.0 1.0] to logical state int [0 255] 
        byte_val = int(float_val * 255)
        
        logical_state = byte_val
        return logical_state


class FloatStepper():
    """ logic value is in range [logic_left - logic_right] """
    logic_left = 0
    logic_right = 1

    dataref = None

    left_most_value = 0 
    right_most_value = 1
    index = None

    state = 0
    step = 0.1

    val_type = float

    @classmethod
    async def set_state(cls, state: float):
        """ set logical state """

        state = min(max(cls.logic_left, state), cls.logic_right)

        cls.state = state

        # from [logic_left logic_right] to [0 1]
        val_01 = (state - cls.logic_left) / (cls.logic_right - cls.logic_left)

        # map logic state [0.0 1.0] to [float_left_most_value float_right_most_value]
        xp_val = (cls.right_most_value - cls.left_most_value) * val_01 + cls.left_most_value

        # use "set value in array" syntax if needed; see ExtPlane plugin array syntax
        if cls.index is not None:
            xp_val = cls.val_type(xp_val)
            xp_val = array_str(cls.index, xp_val)
        else:
            xp_val = cls.val_type(xp_val)

        if cls.dataref is not None:
            await xp.set_param(cls.dataref, xp_val)

    @classmethod 
    def get_state(cls):
        """ get logical state """

        if cls.dataref is not None:
            xp_val = xp_ac.ACState.get_curr_param(cls.dataref)
            if xp_val is None or xp_val == []:
                return

            if cls.index is not None:
                xp_val = xp_val[cls.index]
        
            # map xp_val to float val [0.0 1.0]
            val_01 = (xp_val - cls.left_most_value) / (cls.right_most_value - cls.left_most_value)

            # map to [logic_left logic_right]
            val_logic = (cls.logic_right - cls.logic_left) * val_01 + cls.logic_left
            cls.state = val_logic

        return cls.state 

    @classmethod 
    def get_indication(cls):
        state = cls.get_state()

        if state is None:
            return

        return int(state)

    
    @classmethod
    async def inc(cls):
        state = cls.get_state()
        if not state:
            return

        logic_step = cls.step / (cls.right_most_value - cls.left_most_value)
        await cls.set_state(state + logic_step)

    @classmethod
    async def dec(cls):
        state = cls.get_state()
        if not state:
            return

        logic_step = cls.step / (cls.right_most_value - cls.left_most_value)
        await cls.set_state(state - logic_step)


receive_task = None
send_task = None


async def handle_uso_button_state(button_id, state):
    item = CockpitPanel.buttons.get(button_id)
    if item:
        if state:
            print(button_id, "pressed")
            await item.click()
        else:
            print(button_id, "released")


async def handle_uso_switch_state(switch_id, state):
    item = CockpitPanel.buttons.get(switch_id)
    if item:
        await item.set_state(state)
        print(switch_id, "state", state)


async def handle_uso_rotate_switch_state(rotate_id, new_state, old_state):
    item = CockpitPanel.buttons.get(rotate_id)
    if item:
        right = is_rotate_right(new_state, old_state)
        left = is_rotate_left(new_state, old_state)

        if right:
            await item.inc()
            print(rotate_id, "inc")
        elif left:
            await item.dec()
            print(rotate_id, "dec")


async def handle_uso_float_state(float_id, new_state):
    item = CockpitPanel.buttons.get(float_id)
    if item:
        await item.set_state(new_state)


async def run_send_uso_task(uso_host, uso_send_port):
    remote = await open_remote_endpoint(uso_host, port=uso_send_port)

    global send_task
    send_task = sane_tasks.spawn(send_uso_task(remote))    


async def run_receive_uso_task(uso_host, uso_receive_port):
    endpoint = await open_local_endpoint(host=uso_host, port=uso_receive_port)
    print(f"The UDP overhead panel server is running on port {endpoint.address[1]}...")

    global receive_task
    receive_task = sane_tasks.spawn(receive_uso_task(endpoint))    


import numpy as np
import uso.uso_receive as uso_receive

uso_bits_state = [0] * len(uso_receive.uso_bitfield_names)
uso_floats_state = [0] * len(uso_receive.uso_float_field_names)


async def receive_uso_task(udp_endpoint):
    global uso_bits_state
    global uso_floats_state

    while True:
        new_state, (host, port) = await udp_endpoint.receive()

        new_state = uso_receive.unpack_packet(new_state)
        new_bit_state = new_state["bits"]
        new_floats_state = new_state["floats"]

        # push buttons
        for button_id, bit_idx in uso_receive.uso_pushbuttons_receive_map.items():
            old_state = uso_bits_state[bit_idx]
            new_state = new_bit_state[bit_idx]
            if new_state != old_state:
                await handle_uso_button_state(button_id, new_state)

        # switches 
        for switch_id, bit_idx in uso_receive.uso_switches_receive_map.items():
            old_state = uso_bits_state[bit_idx]
            new_state = new_bit_state[bit_idx]
            if new_state != old_state:
                await handle_uso_switch_state(switch_id, new_state)

        # rotate switches
        for rotate_id, bit_idx in uso_receive.uso_rotate_switch_receive_map.items():
            first_idx = bit_idx
            second_idx = bit_idx + 1

            old_state = (
                uso_bits_state[first_idx], uso_bits_state[second_idx]
            )
            new_state = (
                new_bit_state[first_idx], new_bit_state[second_idx]
            )

            if new_state != old_state:
                await handle_uso_rotate_switch_state(rotate_id, new_state, old_state)
        
        # floats fields
        for float_id, bit_idx in uso_receive.uso_floats_receive_map.items():
            old_state = uso_floats_state[bit_idx]
            new_state = new_floats_state[bit_idx]
            if not math.isclose(old_state, new_state, abs_tol=0.0001):
                await handle_uso_float_state(float_id, new_state)

        uso_bits_state = new_bit_state
        uso_floats_state = new_floats_state


import uso.uso_send as uso_send

uso_send_lamps = [0] * len(uso_send.uso_bitfield_names)


async def send_uso_task(remote):
    while True:
        for lamp_id, bit_idx in uso_send.uso_lamp_send_map.items():
            item = CockpitPanel.buttons.get(lamp_id)
            if item is None:
                print("X")

            state = item.get_indication() or 0
            state = min(max(state, 0), 1) 
            uso_send_lamps[bit_idx] = state

        uso_packet = uso_send.create_packet(uso_send_lamps)

        remote.send(uso_packet.tobytes())

        await asyncio.sleep(0.3)


from overhead_panel import fire_panel
from overhead_panel import flight_control
from overhead_panel import engines_apu
from overhead_panel import hydraulics
from overhead_panel import dc_supply
from overhead_panel import air_conditioning
from overhead_panel import fuel
from overhead_panel import anti_ice
from overhead_panel import bleed
from overhead_panel import pressurization
from overhead_panel import pitot_heat
from overhead_panel import windshield_heat
from overhead_panel import pax_oxygen
from overhead_panel import exterior_lights
from overhead_panel import cockpit_lights
from overhead_panel import interior_lights
from front_panel import warning
from front_panel import autopilot
from front_panel import secondary_flight_display
from middle_pedestal import audio
from middle_pedestal import emergency
from middle_pedestal import checklist_control
from middle_pedestal import wings_config
from middle_pedestal import trackball
from middle_pedestal import engine
import plane_control
