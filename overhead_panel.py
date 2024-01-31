import array
import asyncio
from collections import OrderedDict

import xplane as xp
import aircraft as ac
from aioudp import open_local_endpoint


def overhead_button(name):
    def add_button(cls):
        OverheadPanel.buttons.setdefault(name, cls)
    return add_button


class Custom(type):
    def __getitem__(self, button_name):
       return self.buttons[button_name] 


class OverheadPanel(metaclass=Custom):
    buttons = {}

    @classmethod
    async def reset_to_default_state(cls):
        await cls["Fireclosed 0"].set_enabled(False)
        await OverheadPanel["dish 2 2 2 2"].set_enabled(False)


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
        

@overhead_button("Fireclosed 0")
class Fireclosed0(TwoStateButton):
    @classmethod
    async def on_enabled(cls):
        await xp.set_param(xp.Params["sim/weapons/warhead_type"], "[,,,,1]" )

    @classmethod
    async def on_disabled(cls):
        await xp.set_param(xp.Params["sim/weapons/warhead_type"], "[,,,,0]" )

    @classmethod
    def get_state(cls):
        if ac.ACState.param_available("sim/weapons/warhead_type"):
            return ac.ACState.curr_xplane_state["sim/weapons/warhead_type"][4]


@overhead_button("dish 2 2 2 2")
class Dish2222(TwoStateButton):
    @classmethod
    async def on_enabled(cls):
        await xp.set_param(xp.Params["sim/cockpit2/engine/actuators/fire_extinguisher_on"], "[1]" )

    @classmethod
    async def on_disabled(cls):
        await xp.set_param(xp.Params["sim/cockpit2/engine/actuators/fire_extinguisher_on"], "[0]" )

    @classmethod
    def get_state(cls):
        if ac.ACState.param_available("sim/cockpit2/engine/actuators/fire_extinguisher_on"):
            return ac.ACState.curr_xplane_state["sim/cockpit2/engine/actuators/fire_extinguisher_on"][0]


hardware_panel_reader_task = None
hardware_overhead_buttons_port = 1998

buttons_state = OrderedDict(
    firebutton_1=0,
    firebutton_2=0,
    firebutton_3=0,
    fireapu=0,
    firerearcomp=0,
    firebagcomp=0,
    disch_11=0,
    disch_12=0,
    disch_21=0,
    disch_22=0,
    disch_31=0,
    disch_32=0
)

button_names = list(buttons_state.keys())
buttons_state_udp = bytes(len(button_names))


async def pressed_calback(button_idx, state):
    print(button_names[button_idx], "pressed")

async def released_callback(button_idx, state):
    print(button_names[button_idx], "released")

async def read_hardware_overhead_panel_buttons(udp_endpoint):
    global buttons_state_udp

    while True:
        new_state, (host, port) = await udp_endpoint.receive()

        new_state = array.array('B', new_state)

        for i, (o, n) in enumerate(zip(buttons_state_udp, new_state)):
            if n != o:
                if n != 0:
                    await pressed_calback(i, n)
                else:
                    await released_callback(i, n)

        buttons_state_udp = new_state


async def run_udp_server_for_hardware_overhead_buttons_task():
    endpoint = await open_local_endpoint(port=hardware_overhead_buttons_port)
    print(f"The UDP overhead panel server is running on port {endpoint.address[1]}...")

    global hardware_panel_reader_task
    hardware_panel_reader_task = asyncio.create_task(read_hardware_overhead_panel_buttons(endpoint))    
