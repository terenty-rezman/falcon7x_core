import array
import asyncio
from collections import OrderedDict

import xplane as xp
import xp_aircraft_state as xp_ac
from aioudp import open_local_endpoint, open_remote_endpoint

import sane_tasks


def overhead_button(name):
    def add_button(cls):
        OverheadPanel.buttons.setdefault(name, cls)
        return cls
    return add_button


class Custom(type):
    def __getitem__(self, button_name):
       return self.buttons[button_name] 


class OverheadPanel(metaclass=Custom):
    buttons = {}

    @classmethod
    async def reset_to_default_state(cls):
        await cls["firebutton_1"].set_enabled(False)
        await OverheadPanel["disch_11"].set_enabled(False)


class TwoStateButton:
    dataref: xp.Params = None
    index: int = None
    enabled_val = "1"
    disabled_val = "0"

    @classmethod
    async def on_enabled(cls):
        await xp.set_param(cls.dataref, cls.enabled_val)

    @classmethod
    async def on_disabled(cls):
        await xp.set_param(cls.dataref, cls.disabled_val)
    
    @classmethod
    async def set_enabled(cls, on=True):
        if on:
            await cls.on_enabled()
        else:
            await cls.on_disabled()

    @classmethod
    def get_state(cls):
        if xp_ac.ACState.param_available(cls.dataref):
            val = xp_ac.ACState.curr_params[cls.dataref]
            if cls.index is not None:
                return val[cls.index]
            else:
                return val
    
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
        state = cls.get_state()
        if state == 0:
            await cls.set_enabled(True) 
        elif state == 1:
            await cls.set_enabled(False)


class Indicator:
    dataref: xp.Params = None
    index = None

    @classmethod
    def get_state(cls):
        if xp_ac.ACState.param_available(cls.dataref):
            val = xp_ac.ACState.curr_params[cls.dataref]
            if cls.index is not None:
                return val[cls.index]
            else:
                return val


@overhead_button("firebutton_1")
class firebutton_1(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/weapons/warhead_type"]
    index = 4
    enabled_val = "[,,,,1]"
    disabled_val = "[,,,,0]"


@overhead_button("fireindicator_1")
class fireindicator_1(Indicator):
    dataref: xp.Params = xp.Params["sim/cockpit2/annunciators/engine_fires"]
    index = 0


@overhead_button("disch_11")
class disch_11(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/cockpit2/engine/actuators/fire_extinguisher_on"] 
    index = 0
    enabled_val = "[1]"
    disabled_val = "[0]"


disch_12 = disch_11
overhead_button("disch_12")(disch_12)

@overhead_button("fire_apu_indicator")
class fire_apu_indicator(Indicator):
    dataref: xp.Params = xp.Params["sim/operation/failures/rel_apu_fire"]


@overhead_button("apu_disch")
class apu_disch(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/cockpit2/engine/actuators/fire_extinguisher_on"] 
    index = 4
    enabled_val = "[,,,,1]"
    disabled_val = "[,,,,0]"


@overhead_button("fire_apu_closed_indicator")
class fire_apu_closed_indicator(Indicator):
    dataref: xp.Params = xp.Params["sim/cockpit/engine/APU_switch"]


@overhead_button("firebutton_2")
class firebutton_2(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/weapons/warhead_type"]
    index = 5
    enabled_val = "[,,,,,1]"
    disabled_val = "[,,,,,0]"


@overhead_button("fireindicator_2")
class fireindicator_2(Indicator):
    dataref: xp.Params = xp.Params["sim/cockpit2/annunciators/engine_fires"]
    index = 1


@overhead_button("disch_21")
class disch_21(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/cockpit2/engine/actuators/fire_extinguisher_on"] 
    index = 1
    enabled_val = "[,1]"
    disabled_val = "[,0]"


disch_22 = disch_21
overhead_button("disch_22")(disch_22)


@overhead_button("firebutton_3")
class firebutton_3(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/weapons/warhead_type"]
    index = 6
    enabled_val = "[,,,,,,1]"
    disabled_val = "[,,,,,,0]"


@overhead_button("fireindicator_3")
class fireindicator_3(Indicator):
    dataref: xp.Params = xp.Params["sim/cockpit2/annunciators/engine_fires"]
    index = 2


@overhead_button("disch_31")
class disch_31(TwoStateButton):
    dataref: xp.Params = xp.Params["sim/cockpit2/engine/actuators/fire_extinguisher_on"] 
    index = 2
    enabled_val = "[,,1]"
    disabled_val = "[,,0]"


disch_32 = disch_31
overhead_button("disch_32")(disch_32)

receive_task = None
send_task = None
receive_state_port = 1998
send_state_port = 1999

hardware_panel_items_receive = OrderedDict(
    firebutton_1=0,
    firebutton_2=1,
    firebutton_3=2,
    apu_disch=3,
    firerearcomp=4,
    firebagcomp=5,
    disch_11=6,
    disch_12=7,
    disch_21=8,
    disch_22=9,
    disch_31=10,
    disch_32=11
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
    disch_32=14
)

button_names = list(hardware_panel_items_receive.keys())
buttons_state_received_bytes = bytes(len(button_names))

panel_state_send_bytes = array.array('B', [0] * len(OverheadPanel.buttons))


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
                state = btn.get_state()
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
