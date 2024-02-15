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


class Button:
    dataref: xp.Params = None
    index: int = None

    @classmethod
    def get_state(cls):
        if (val := xp_ac.ACState.get_curr_param(cls.dataref)) is None:
            return

        if cls.index is not None:
            if len(val):
                return val[cls.index]
        else:
            return val
    
    @classmethod
    def get_indication(cls):
        """ для зажигания статусов на hardware панели """
        """ 1 - light indication; 0 - dont light indication """
        return cls.get_state()
    
    @classmethod
    async def wait_state(cls, val):
        def condition(param_val):
            if cls.index is None:
                return param_val == val
            else:
                return param_val[cls.index] == val

        await xp_ac.ACState.wait_until_parameter_condition(cls.dataref, condition)

    @classmethod
    async def click(cls):
        pass


class TwoStateButton(Button):
    disabled_val = 0
    enabled_val = 1

    @classmethod
    async def on_enabled(cls):
        await xp.set_param(cls.dataref, cls.enabled_val)

    @classmethod
    async def on_disabled(cls):
        await xp.set_param(cls.dataref, cls.disabled_val)
    
    @classmethod
    async def set_state(cls, state):
        if state:
            await cls.on_enabled()
        else:
            await cls.on_disabled()

    @classmethod
    async def click(cls):
        state = cls.get_state()
        if state == 0:
            await cls.set_state(1) 
        elif state == 1:
            await cls.set_state(0)


class ThreeStateButton(Button):
    state1_val = 0
    state2_val = 1
    state3_val = 3

    @classmethod
    async def on_state(cls, state):
        if state == 0:
            await xp.set_param(cls.dataref, cls.state1_val)
        elif state == 1:
            await xp.set_param(cls.dataref, cls.state2_val)
        elif state == 2:
            await xp.set_param(cls.dataref, cls.state3_val)
    
    @classmethod
    async def set_state(cls, state):
        await cls.on_state(state)

    @classmethod
    async def click(cls):
        state = cls.get_state()
        if state == 0:
            await cls.set_state(1) 
        elif state == 1:
            await cls.set_state(2)
        else:
            await cls.set_state(0)


class Indicator:
    dataref: xp.Params = None
    index = None

    @classmethod
    def get_state(cls):
        if (val := xp_ac.ACState.get_curr_param(cls.dataref)) is None:
            return

        if cls.index is not None:
            return val[cls.index]
        else:
            return val

    @classmethod
    def get_indication(cls):
        """ для зажигания статусов на hardware панели """
        """ 1 - light indication; 0 - dont light indication """
        return cls.get_state()


receive_task = None
send_task = None
receive_state_port = 1998
send_state_port = 1999

hardware_panel_items_receive = OrderedDict(
    firebutton_1=0,
    firebutton_2=1,
    firebutton_3=2,
    apu_disch=3,
    firerearcomp_button=4,
    firebagcomp_button=5,
    disch_11=6,
    disch_12=7,
    disch_21=8,
    disch_22=9,
    disch_31=10,
    disch_32=11,
    airbrake_auto=12,
    fcs_engage_norm=13,
    fcs_engage_stby=14,
    fcs_steering=15,
    apu_master=16,
    apu_start_stop=17,
    shutoff_a1=18,
    shutoff_a2=19,
    backup_pump=20,
    shutoff_b2=21,
    shutoff_b3=22,
    shutoff_c2=23,
)

hardware_panel_items_send = OrderedDict(
    firebutton_1=0,
    fireindicator_1=1,
    disch_11=2,
    disch_12=3,
    apu_disch=4,
    fire_apu_indicator=5,
    fire_apu_closed_indicator=6,
    firebutton_2=7,
    fireindicator_2=8,
    disch_21=9,
    disch_22=10,
    firebutton_3=11,
    fireindicator_3=12,
    disch_31=13,
    disch_32=14,
    firerearcomp_button=16,
    firerearcomp_indicator=17,
    firebagcomp_button=18,
    firebagcomp_indicator=19,
    airbrake_auto=20,
    fcs_engage_norm=21,
    fcs_engage_stby=22,
    fcs_steering=23,
    apu_master=24,
    apu_start_stop=25,
    shutoff_a1=26,
    shutoff_a2=27,
    backup_pump=28,
    shutoff_b2=29,
    shutoff_b3=30,
    shutoff_c2=31,
)

button_names = list(hardware_panel_items_receive.keys())
buttons_state_received_bytes = bytes(len(button_names))

panel_state_send_bytes = array.array('B', [0] * len(hardware_panel_items_send))


async def pressed_calback(button_id, state):
    print(button_id, "pressed")
    button = OverheadPanel.buttons.get(button_id)
    if button:
        await button.click()
            

async def released_callback(button_id, state):
    print(button_id, "released")


async def receive_state_task(udp_endpoint):
    global buttons_state_received_bytes

    while True:
        new_state, (host, port) = await udp_endpoint.receive()

        new_state = array.array('B', new_state)

        for i, (o, n) in enumerate(zip(buttons_state_received_bytes, new_state)):
            if n != o:
                button_id = button_names[i]
                if n != 0:
                    await pressed_calback(button_id, n)
                else:
                    await released_callback(button_id, n)

        buttons_state_received_bytes = new_state


async def run_receive_state_task():
    endpoint = await open_local_endpoint(port=receive_state_port)
    print(f"The UDP overhead panel server is running on port {endpoint.address[1]}...")

    global receive_task
    receive_task = sane_tasks.spawn(receive_state_task(endpoint))    


async def send_state_task(remote):
    while True:
        updated = False
        for i, id in enumerate(hardware_panel_items_send.keys()):
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
