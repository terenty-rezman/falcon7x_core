

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
    await cas.show_message_alarm(cas.CHECK_STATUS)
    await cas.show_message_alarm(cas.PARK_BRAKE_ON)
    await cas.show_message_alarm(cas.NWS_OFF)
    await cas.show_message_alarm(cas.DOOR_PAX_NOT_SECURED)


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
