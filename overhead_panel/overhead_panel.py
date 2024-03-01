import array
import asyncio
from collections import OrderedDict

import xplane as xp
import xp_aircraft_state as xp_ac
from aioudp import open_local_endpoint, open_remote_endpoint

import sane_tasks


def add_to_overhead_panel(cls):
    OverheadPanel.buttons.setdefault(cls.__name__, cls)
    return cls


class Custom(type):
    def __getitem__(self, button_name):
       return self.buttons[button_name] 


class OverheadPanel(metaclass=Custom):
    buttons = {}

    @classmethod
    async def reset_to_default_state(cls):
        await cls["firebutton_1"].set_state(0)
        await OverheadPanel["disch_11"].set_state(0)
    

def array_str(index, val):
    return f"[{',' * index}{val}]"

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


receive_task = None
send_task = None
receive_state_port = 1998
send_state_port = 1999

hardware_panel_items_receive = [
    "firebutton_1",
    "firebutton_2",
    "firebutton_3",
    "apu_disch",
    "firerearcomp_button",
    "firebagcomp_button",
    "disch_11",
    "disch_12",
    "disch_21",
    "disch_22",
    "disch_31",
    "disch_32",
    "airbrake_auto",
    "fcs_engage_norm",
    "fcs_engage_stby",
    "fcs_steering",
    "apu_master",
    "apu_start_stop",
    "shutoff_a1",
    "shutoff_a2",
    "backup_pump",
    "shutoff_b2",
    "shutoff_b3",
    "shutoff_c2",
    "galley_master",
    "lh_master",
    "lh_init",
    "bus_tie",
    "rh_init",
    "rh_master",
    "cabin_master",
    "ext_power",
    "gen1",
    "lh_isol",
    "rat_reset",
    "rh_isol",
    "gen2",
    "gen3",
    "bat1",
    "bat2",
    "aft_temp",
    "fwd_temp",
    "fwd_temp_push",
    "crew_temp",
    "crew_temp_push",
    "crew_ratio",
    "gnd_vent",
    "pack",
    "bag_isol",
    "xbleed_ecs",
    "boost1",
    "xtk_1",
    "xtk_2",
    "boost3",
    "xtk_3",
    "backup_13",
    "xtk_4",
    "xtk_5",
    "boost2",
    "xtk_6",
    "xbp_12",
    "xbp_13",
    "xbp_23",
    "wings",
    "ice_brake",
    "ice_eng1",
    "ice_eng2",
    "ice_eng3",
    "bleed1",
    "bleed12",
    "bleed2",
    "bleed13",
    "bleed_apu",
    "bleed3",
    "dump",
    "bag_vent",
    "cabin_alt",
    "pressu_man",
    "probe_12",
    "probe_3",
    "probe_4",
    "windshield_lh",
    "windshield_rh",
    "windshield_backup",
    "pax_oxygen",
]

hardware_panel_items_send = [ 
    "firebutton_1",
    "fireindicator_1",
    "disch_11",
    "disch_12",
    "apu_disch",
    "fire_apu_indicator",
    "fire_apu_closed_indicator",
    "firebutton_2",
    "fireindicator_2",
    "disch_21",
    "disch_22",
    "firebutton_3",
    "fireindicator_3",
    "disch_31",
    "disch_32",
    "firerearcomp_button",
    "firerearcomp_indicator",
    "firebagcomp_button",
    "firebagcomp_indicator",
    "airbrake_auto",
    "fcs_engage_norm",
    "fcs_engage_stby",
    "fcs_steering",
    "apu_master",
    "apu_start_stop",
    "shutoff_a1",
    "shutoff_a2",
    "backup_pump",
    "shutoff_b2",
    "shutoff_b3",
    "shutoff_c2",
    "galley_master",
    "lh_master",
    "lh_init",
    "bus_tie",
    "rh_init",
    "rh_master",
    "cabin_master",
    "ext_power",
    "gen1",
    "lh_isol",
    "rat_reset",
    "rh_isol",
    "gen2",
    "gen3",
    "bat1",
    "bat2",
    "aft_temp",
    "fwd_temp",
    "fwd_temp_push",
    "crew_temp",
    "crew_temp_push",
    "crew_ratio",
    "gnd_vent",
    "bag_isol",
    "xbleed_ecs",
    "boost1",
    "xtk_1",
    "xtk_2",
    "boost3",
    "xtk_3",
    "backup_13",
    "xtk_4",
    "xtk_5",
    "boost2",
    "xtk_6",
    "xbp_12",
    "xbp_13",
    "xbp_23",
    "wings",
    "ice_brake",
    "ice_eng1",
    "ice_eng2",
    "ice_eng3",
    "bleed1",
    "bleed12",
    "bleed2",
    "bleed13",
    "bleed_apu",
    "bleed3",
    "dump",
    "bag_vent",
    "pressu_man",
    "probe_12",
    "probe_3",
    "probe_4",
    "windshield_lh",
    "windshield_rh",
    "windshield_backup",
]


button_names = list(hardware_panel_items_receive)
buttons_state_received_bytes = bytes(len(button_names))

panel_state_send_bytes = array.array('B', [0] * len(hardware_panel_items_send))


async def handle_button_state(button_id, state):
    item = OverheadPanel.buttons.get(button_id)

    if item:
        # special case for switches
        if issubclass(item, (FloatSwitch, DiscreteSwitch)):
            print(state)
            await item.set_state(state)
        else:
            # default case - button
            if state:
                print(button_id, "pressed")
                await item.click()
            else:
                print(button_id, "released")


async def receive_state_task(udp_endpoint):
    global buttons_state_received_bytes

    while True:
        new_state, (host, port) = await udp_endpoint.receive()

        new_state = array.array('B', new_state)

        for i, (o, n) in enumerate(zip(buttons_state_received_bytes, new_state)):
            if n != o:
                button_id = button_names[i]
                await handle_button_state(button_id, n)

        buttons_state_received_bytes = new_state


async def run_receive_state_task():
    endpoint = await open_local_endpoint(port=receive_state_port)
    print(f"The UDP overhead panel server is running on port {endpoint.address[1]}...")

    global receive_task
    receive_task = sane_tasks.spawn(receive_state_task(endpoint))    


async def send_state_task(remote):
    while True:
        updated = False
        for i, id in enumerate(hardware_panel_items_send):
            btn = OverheadPanel.buttons.get(id)
            if btn:
                state = btn.get_indication()
                if state is not None:
                    panel_state_send_bytes[i] = state
                    updated = True
        
        if updated:
            remote.send(panel_state_send_bytes.tobytes())

        await asyncio.sleep(0.1)
        

async def run_send_state_task():
    remote = await open_remote_endpoint("127.0.0.1", port=send_state_port)

    global send_task
    send_task = sane_tasks.spawn(send_state_task(remote))    


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
