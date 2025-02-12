

import asyncio

import xplane.master as xp
import common.xp_aircraft_state as xp_ac
from cas import cas
from common.scenario import scenario
import overhead_panel.dc_supply as elec
import middle_pedestal.emergency as emergency
import overhead_panel.exterior_lights as exterior_lights
import overhead_panel.windshield_heat as windshield
import middle_pedestal.wings_config as wc
import synoptic_remote.param_overrides as synoptic_overrides
from xplane.params import Params

import middle_pedestal.engine as engine_panel


@scenario("NORMAL", None, "AFTER LANDING")
async def after_landing(ac_state: xp_ac.ACState):
    pass


@scenario("NORMAL", None, "AFTER START")
async def after_start(ac_state: xp_ac.ACState):
    pass


@scenario("NORMAL", None, "AT_RAMP")
async def at_ramp(ac_state: xp_ac.ACState):
    pass


@scenario("NORMAL", None, "BEFORE START")
async def before_start(ac_state: xp_ac.ACState):
    pass


@scenario("NORMAL", None, "COCKPIT PREPARATION")
async def cockpit_preparation(ac_state: xp_ac.ACState):
    pass


@scenario("NORMAL", None, "CRUISE")
async def cruise(ac_state: xp_ac.ACState):
    pass


@scenario("NORMAL", None, "DESCENT")
async def cruise(ac_state: xp_ac.ACState):
    pass


@scenario("NORMAL", None, "LANDING")
async def landing(ac_state: xp_ac.ACState):
    pass


@scenario("NORMAL", None, "POWER ON")
async def power_on(ac_state: xp_ac.ACState):
    await cas.set_regime(cas.Regimes.PARK)
    await cas.remove_all_messages()
    await asyncio.sleep(2)
    await cas.show_message_alarm(cas.NWS_OFF)
    await cas.show_message_alarm(cas.PARK_BRAKE_ON)
    await cas.show_message_alarm(cas.DOOR_PAX_NOT_SECURED_W)
    await cas.show_message_alarm(cas.CHECK_STATUS_A)

    await engine_panel.en_start.wait_state(1)

    async with synoptic_overrides.param_overrides([
        # Params["sim/cockpit2/engine/indicators/ITT_deg_C[0]"],
        # Params["sim/cockpit2/engine/indicators/ITT_deg_C[1]"],
        # Params["sim/cockpit2/engine/indicators/ITT_deg_C[2]"],
        Params["sim/cockpit2/engine/indicators/N2_percent[0]"],
        Params["sim/cockpit2/engine/indicators/N2_percent[1]"],
        Params["sim/cockpit2/engine/indicators/N2_percent[2]"],
        Params["sim/cockpit2/engine/indicators/fuel_flow_kg_sec[0]"],
        Params["sim/cockpit2/engine/indicators/fuel_flow_kg_sec[1]"],
        Params["sim/cockpit2/engine/indicators/fuel_flow_kg_sec[2]"],
        Params["sim/cockpit2/engine/indicators/oil_pressure_psi[0]"],
        Params["sim/cockpit2/engine/indicators/oil_pressure_psi[1]"],
        Params["sim/cockpit2/engine/indicators/oil_pressure_psi[2]"],
    ]) as _:
        # after engine start
        # start appears in 1 sec after engine start
        async def ff():
            await synoptic_overrides.linear_anim(Params["sim/cockpit2/engine/indicators/fuel_flow_kg_sec[0]"], 0, 0.001, 20)
            await synoptic_overrides.linear_anim(Params["sim/cockpit2/engine/indicators/fuel_flow_kg_sec[0]"], 0.001, 0.0377386, 16)

        async def N2():
            await synoptic_overrides.linear_anim(Params["sim/cockpit2/engine/indicators/N2_percent[0]"], 0, 1, 1)
            await synoptic_overrides.linear_anim(Params["sim/cockpit2/engine/indicators/N2_percent[0]"], 1, 2, 8)
            await synoptic_overrides.linear_anim(Params["sim/cockpit2/engine/indicators/N2_percent[0]"], 1, 52, 32)

        async def oil():
            await synoptic_overrides.linear_anim(Params["sim/cockpit2/engine/indicators/oil_pressure_psi[0]"], 0, 5, 19)
            await synoptic_overrides.linear_anim(Params["sim/cockpit2/engine/indicators/oil_pressure_psi[0]"], 5, 86, 50)
        
        await asyncio.gather(*[ff(), N2(), oil()])

        # ign appears after 15 sec after engine start or N2 == 17%

        await asyncio.sleep(5)

    print("done")


@scenario("NORMAL", None, "POWER OFF")
async def power_off(ac_state: xp_ac.ACState):
    pass


@scenario("NORMAL", None, "START")
async def start(ac_state: xp_ac.ACState):
    pass


@scenario("NORMAL", None, "TAKE-OFF")
async def take_off(ac_state: xp_ac.ACState):
    pass


@scenario("NORMAL", None, "TAXI")
async def taxi(ac_state: xp_ac.ACState):
    pass
