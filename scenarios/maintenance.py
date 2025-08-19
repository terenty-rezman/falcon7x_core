import asyncio

import xplane.master as xp
import common.xp_aircraft_state as xp_ac
from cas import cas
from common.scenario import scenario
import overhead_panel.dc_supply as elec
import middle_pedestal.emergency as emergency
import overhead_panel.exterior_lights as exterior_lights
import overhead_panel.windshield_heat as windshield
import overhead_panel.flight_control as fc 
import front_panel.warning as fpw
import overhead_panel.fire_panel as fp 
import overhead_panel.engines_apu as overhead_engines
import middle_pedestal.engine as engine_panel
import aircraft_systems.engine as engine_system

from common import plane_control as pc
from aircraft_systems import engine
import common.util as util

APU_N1 = xp.Params["sim/cockpit2/electrical/APU_N1_percent"]


@scenario("MAINTENANCE", "ENGINE", "AUTO SHUTDOWN ENG1 N1")
async def auto_shutdown_eng1_n1(ac_state: xp_ac.ACState):
    try:
        await engine_panel.en_fuel_digital_1.set_state(1)
        engine_system.EngineStart1.broken_start = True
        await asyncio.sleep(42)

    except asyncio.CancelledError:
        await engine_panel.en_fuel_digital_1.set_state(1)
    finally:
        engine_system.EngineStart1.broken_start = False
