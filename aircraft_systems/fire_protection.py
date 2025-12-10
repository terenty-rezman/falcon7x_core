import asyncio

import common.xp_aircraft_state as xp_ac
import xplane.master as xp
import common.sane_tasks as sane_tasks
import common.simulation as sim
import overhead_panel.fire_panel as fp 

from aircraft_systems.system_base import System


class APUFireProtection(System):
    @classmethod
    def start_condition(cls):
        # apu fire failure
        if xp_ac.ACState.get_curr_param(xp.Params["sim/operation/failures/rel_apu_fire"]) == 6:
            return True

    @classmethod
    async def system_logic_task(cls):
        await sim.sleep(3)
        return

        # Apu fire protection system automatically closes apu fsov
        await xp.set_param(xp.Params["sim/cockpit/engine/APU_switch"], 1)

        # wait until user presses apu extinguisher button 
        await fp.apu_disch.wait_state(1)

        await sim.sleep(2)

        # fire has been succesfully extinguished
        failure = xp.Params["sim/operation/failures/rel_apu_fire"]
        await xp.set_param(failure, 0)
        await xp_ac.ACState.wait_until_parameter_condition(failure, lambda p: p == 0)


class RearCompFireProtection(System):
    @classmethod
    def start_condition(cls):
        if xp_ac.ACState.get_curr_param(xp.Params["sim/operation/failures/rel_engfir3"]) == 6:
            return True

    @classmethod
    async def system_logic_task(cls):
        # wait until user presses apu extinguisher button 
        await fp.firerearcomp_button.wait_state(1)

        await sim.sleep(2)

        # fire has been succesfully extinguished
        failure = xp.Params["sim/operation/failures/rel_engfir3"]
        await xp.set_param(failure, 0)
        await xp_ac.ACState.wait_until_parameter_condition(failure, lambda p: p == 0)


class BagCompFireProtection(System):
    @classmethod
    def start_condition(cls):
        if xp_ac.ACState.get_curr_param(xp.Params["sim/operation/failures/rel_engfir4"]) == 6:
            return True

    @classmethod
    async def system_logic_task(cls):
        # wait until user presses apu extinguisher button 
        await fp.firebagcomp_button.wait_state(1)

        await sim.sleep(2)

        # fire has been succesfully extinguished
        failure = xp.Params["sim/operation/failures/rel_engfir4"]
        await xp.set_param(failure, 0)
        await xp_ac.ACState.wait_until_parameter_condition(failure, lambda p: p == 0)

