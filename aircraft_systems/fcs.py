import asyncio

import enum

import common.xp_aircraft_state as xp_ac
import xplane.master as xp
import common.sane_tasks as sane_tasks
import overhead_panel.dc_supply as dc
import overhead_panel.engines_apu as eng_apu
import overhead_panel.hydraulics as hyd

from aircraft_systems.system_base import System
import aircraft_systems.engine as engine_sys
import xplane.master as xp
import aircraft_systems.elec as elec_sys

from common.util import LineColor


class FCScomputers(System):
    next_wake_sleep_delay = 1

    mfcc_1 = xp.Params["sim/custom/7x/z_fcs_mfcc_1"]
    mfcc_2 = xp.Params["sim/custom/7x/z_fcs_mfcc_2"]
    mfcc_3 = xp.Params["sim/custom/7x/z_fcs_mfcc_3"]

    sfcc_1 = xp.Params["sim/custom/7x/z_fcs_sfcc_1"]
    sfcc_2 = xp.Params["sim/custom/7x/z_fcs_sfcc_2"]
    sfcc_3 = xp.Params["sim/custom/7x/z_fcs_sfcc_3"]

    old_state = []

    @classmethod
    def start_condition(cls):
        return True

    @classmethod
    async def system_logic_task(cls):
        mfcc_1_state = 1
        mfcc_2_state = 1
        mfcc_3_state = 1

        sfcc_1_state = 1
        sfcc_2_state = 1
        sfcc_3_state = 1

        # mfcc_1_state = not (xp_ac.ACState.get_curr_param(cls.mfcc_1) or 0)

        new_state = [
            mfcc_1_state,
            mfcc_2_state,
            mfcc_2_state,
            sfcc_1_state,
            sfcc_2_state,
            sfcc_3_state
        ]

        if new_state != cls.old_state:
            cls.old_state = new_state

            await xp.set_param(cls.mfcc_1, int(mfcc_1_state))
            await xp.set_param(cls.mfcc_2, int(mfcc_2_state))
            await xp.set_param(cls.mfcc_3, int(mfcc_3_state))

            await xp.set_param(cls.sfcc_1, int(sfcc_1_state))
            await xp.set_param(cls.sfcc_2, int(sfcc_2_state))
            await xp.set_param(cls.sfcc_3, int(sfcc_3_state))
