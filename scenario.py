import asyncio

import xp_aircraft_state as xp_ac
import xplane as xp
from instrument_panel import CockpitPanel
import sane_tasks
import cas


scenarios = {}
scenario = lambda f: scenarios.setdefault(f.__name__, f)


class Scenario:
    current_scenario_task = None

    @classmethod
    async def clear_all(cls):
        # clear current task
        if cls.current_scenario_task:
            cls.current_scenario_task.cancel()
            try:
                await cls.current_scenario_task
            except asyncio.CancelledError:
                print(f"stoped task {cls.current_scenario_task.__name__}")
                cls.current_scenario_task = None

    @classmethod
    async def run_scenario_task(cls, task_name, ac_state: xp_ac.ACState):
        await cls.clear_all()
        
        task = sane_tasks.spawn(scenarios[task_name](ac_state))
        cls.current_scenario_task = task
        print(f"run task {task_name}")


@scenario
async def test_scenario_1(ac_state: xp_ac.ACState):
    def fly_height_200m(ac_state: xp_ac.ACState):
        elevation = "sim/flightmodel/position/elevation"
        if not ac_state.param_available(elevation):
            return False

        if ac_state.curr_params[elevation] - ac_state.initial_params[elevation] > 200:
            return True
    
    await ac_state.data_condition(fly_height_200m)

    print("fire the engine")
    # await xp.set_param(xp.Failures["sim/operation/failures/rel_engfir0"], 6)
    # await xp.set_param(xp.Failures["sim/operation/failures/rel_engfla0"], 6)

    # await asyncio.sleep(10)

    # press engine 1 shutoff button on overhead panel
    # await OverheadPanel["Fireclosed 0"].set_enabled(True)
    # await asyncio.sleep(5)

    # await OverheadPanel["dish 2 2 2 2"].set_enabled(True)
    # roll control, left control column jammed
    # await xp.set_param(xp.Failures["sim/operation/failures/rel_ail_L_jam"], 6)


@scenario
async def eng1_oil_too_low_press(ac_state: xp_ac.ACState):
    await asyncio.sleep(5)

    # RED CAS message + sound: 54 ENG 1 OIL TOO LOW PRESS
    cas.show_message_alarm("54 ENG 1 OIL TOO LOW PRESS")

    # PDU automatically shows ENG TRM
    await xp.set_param(xp.Params["sim/7x/choixtcas"], 1)

    await xp.set_param(xp.Params["sim/custom/7x/z_eng1_oil_press_override"], 1)
    await xp.set_param(xp.Params["sim/custom/7x/z_eng1_oil_press"], 0)

    N2 = xp.Params["sim/cockpit2/engine/indicators/N2_percent"]
    await xp_ac.ACState.wait_until_parameter_condition(N2, lambda p: p[0] < 10)

    # hide CAS msg ?
    
    # restore original oil pressure
    await xp.set_param(xp.Params["sim/custom/7x/z_eng1_oil_press_override"], 0)


import overhead_panel.flight_control as fc 
import overhead_panel.dc_supply as elec
import overhead_panel.windshield_heat as windshield
import audio_mkb.emergency as emergency
import overhead_panel.exterior_lights as exterior_lights

@scenario
async def fcs_direct_laws_active_1(ac_state: xp_ac.ACState):
    await asyncio.sleep(5)

    # RED CAS message: FCS: DIRECT LAWS ACTIVE
    print("FCS: DIRECT LAWS ACTIVE")

    await fc.airbrake_auto.wait_state(1)

    # YELLOW CAS message: FCS: MFCC FAULT
    print("FCS: MFCC FAULT")

    await fc.fcs_engage_stby.wait_state(1)

    # hide RED CAS message: FCS: DIRECT LAWS ACTIVE
    print("HIDE FCS: DIRECT LAWS ACTIVE")


@scenario
async def fcs_direct_laws_active_2(ac_state: xp_ac.ACState):
    await asyncio.sleep(5)

    # RED CAS message: FCS: DIRECT LAWS ACTIVE
    print("FCS: BOTH AILERONS FAIL")

    await fc.airbrake_auto.wait_state(1)

    # YELLOW CAS message: FCS: BOTH AILERONS FAIL
    print("FCS: BOTH AILERONS FAIL")


@scenario
async def elec_gen_2_fault(ac_state: xp_ac.ACState):
    await asyncio.sleep(5)

    # YELLOW CAS message
    cas.show_message_alarm("ELECT: GEN 2 FAULT")

    # light gen2 off
    await elec.gen2.set_state(1)

    # wait gen2 on
    await elec.gen2.wait_state(0)

    # light gen2 on unsuccessfull - light gen2 off again
    await elec.gen2.set_state(1)

    await elec.bus_tie.wait_state(1)

    # wind shield AUTO
    await windshield.windshield_lh.wait_state(0)
    await windshield.windshield_rh.wait_state(0)


@scenario
async def _36_elec_lh_rh_ess_pwr_lo(ac_state: xp_ac.ACState):
    await asyncio.sleep(5)

    # RED CAS message + sound
    cas.show_message_alarm("36 ELEC: LH+RH ESS PWR LO")

    # set elec rh + lh to isol
    await elec.lh_isol.set_state(1)
    await elec.rh_isol.set_state(1)
    # light gen2 off
    await elec.gen2.set_state(1)

    # wait for rh + lh TIED
    await elec.lh_isol.wait_state(0)
    await elec.rh_isol.wait_state(0)

    # wait gen2 on
    await elec.gen2.wait_state(0)

    cas.hide_message("36 ELEC: LH+RH ESS PWR LO")


@scenario
async def _26_elec_aft_dist_box_ovht(ac_state: xp_ac.ACState):
    await asyncio.sleep(5)

    # RED CAS message + sound
    cas.show_message_alarm("26 ELEC: AFT DIST BOX OVHT")

    await emergency.elec_rh_ess.wait_state(1)

    await elec.bus_tie.wait_state(0)

    await elec.rh_isol.wait_state(1)

    await elec.cabin_master.wait_state(1)

    # OFF
    await exterior_lights.el_landing_lh.wait_state(0)
    await exterior_lights.el_landing_rh.wait_state(0)

    # OFF
    await exterior_lights.el_taxi.wait_state(0)
    await exterior_lights.el_wing.wait_state(0)

    # OFF
    await windshield.windshield_lh.wait_state(1)
    await windshield.windshield_rh.wait_state(1)
