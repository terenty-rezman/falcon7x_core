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
    @classmethod
    async def on_enabled(cls):
        pass

    @classmethod
    async def on_disabled(cls):
        pass
    
    @classmethod
    async def set_enabled(cls, on=True):
        if on:
            await cls.on_enabled()
        else:
            await cls.on_disabled()

    @classmethod
    def get_state(cls):
        pass

    @classmethod
    async def click(cls):
        state = cls.get_state()
        if state == 0:
            await cls.set_enabled(True) 
        elif state == 1:
            await cls.set_enabled(False)


class Indicator:
    @classmethod
    def get_state(cls):
        pass


@overhead_button("firebutton_1")
class firebutton_1(TwoStateButton):
    @classmethod
    async def on_enabled(cls):
        await xp.set_param(xp.Params["sim/weapons/warhead_type"], "[,,,,1]" )

    @classmethod
    async def on_disabled(cls):
        await xp.set_param(xp.Params["sim/weapons/warhead_type"], "[,,,,0]" )

    @classmethod
    def get_state(cls):
        if xp_ac.ACState.param_available(xp.Params["sim/weapons/warhead_type"]):
            return xp_ac.ACState.curr_params[xp.Params["sim/weapons/warhead_type"]][4]


@overhead_button("fireindicator_1")
class fireindicator_1(Indicator):
    @classmethod
    def get_state(cls):
        if xp_ac.ACState.param_available(xp.Params["sim/cockpit2/annunciators/engine_fires"]):
            return xp_ac.ACState.curr_params[xp.Params["sim/cockpit2/annunciators/engine_fires"]][0]


@overhead_button("disch_11")
class disch_11(TwoStateButton):
    @classmethod
    async def on_enabled(cls):
        await xp.set_param(xp.Params["sim/cockpit2/engine/actuators/fire_extinguisher_on"], "[1]" )

    @classmethod
    async def on_disabled(cls):
        await xp.set_param(xp.Params["sim/cockpit2/engine/actuators/fire_extinguisher_on"], "[0]" )

    @classmethod
    def get_state(cls):
        if xp_ac.ACState.param_available(xp.Params["sim/cockpit2/engine/actuators/fire_extinguisher_on"]):
            return xp_ac.ACState.curr_params[xp.Params["sim/cockpit2/engine/actuators/fire_extinguisher_on"]][0]

disch_12 = disch_11
overhead_button("disch_12")(disch_12)

@overhead_button("fire_apu_indicator")
class fire_apu_indicator(Indicator):
    @classmethod
    def get_state(cls):
        if xp_ac.ACState.param_available(xp.Params["sim/operation/failures/rel_apu_fire"]):
            return xp_ac.ACState.curr_params[xp.Params["sim/operation/failures/rel_apu_fire"]]

@overhead_button("apu_disch")
class apu_disch(TwoStateButton):
    @classmethod
    async def on_enabled(cls):
        await xp.set_param(xp.Params["sim/weapons/mis_thrust3"], "[,,,,1]" )

    @classmethod
    async def on_disabled(cls):
        await xp.set_param(xp.Params["sim/weapons/mis_thrust3"], "[,,,,0]" )

    @classmethod
    def get_state(cls):
        if xp_ac.ACState.param_available(xp.Params["sim/weapons/mis_thrust3"]):
            return xp_ac.ACState.curr_params[xp.Params["sim/weapons/mis_thrust3"]][4]


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
