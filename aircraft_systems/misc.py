import asyncio

import enum

import common.xp_aircraft_state as xp_ac
import xplane.master as xp
import common.sane_tasks as sane_tasks
import overhead_panel.dc_supply as dc
import overhead_panel.engines_apu as eng_apu
import common.plane_control as pc
import cas.cas as cas

from aircraft_systems.system_base import System


class FlightRegime(System):
    FLIGHT_REGIME = xp.Params["sim/custom/7x/z_flight_regime"]

    regime = None
    next_wake_sleep_delay = 1

    @classmethod
    def start_condition(cls):
        # run every time
        return True

    @classmethod
    async def system_logic_task(cls):
        alt_above_ground = xp_ac.ACState.get_curr_param(xp.Params["sim/flightmodel/position/y_agl"]) or 0
        park_brake_enabled =  pc.pc_parkbrake.get_state() == 1
        n1 = xp_ac.ACState.get_curr_param(xp.Params["sim/cockpit2/engine/indicators/N1_percent[0]"]) or 0

        regime = cas.Regimes.PARK

        if alt_above_ground < 200: 
            if n1 > 65:
                regime = cas.Regimes.TO
            else:
                regime = cas.Regimes.LAND
        else:
            regime = cas.Regimes.CRUISE

        if alt_above_ground < 5:
            regime = cas.Regimes.TAXI

            if park_brake_enabled:
                regime = cas.Regimes.PARK
        
        if regime != cls.regime:
            cls.regime = regime
            await xp.set_param(cls.FLIGHT_REGIME, int(regime))
            print(regime)

        # send regime to cas all the time
        # await cas.set_regime(cls.regime) 

