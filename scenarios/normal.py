

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
import overhead_panel.engines_apu as overhead_engines


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

    async def engine_start_N(N2, ITT, IGN, OIL, FUEL, START, AB, fuel_flow_switch):
        APU_N1 = xp.Params["sim/cockpit2/electrical/APU_N1_percent"]

        def engine_start(ac_state: xp_ac.ACState):
            cond = [
                fuel_flow_switch.get_state() == 1,
                ac_state.get_curr_param(N2) < 5,
                overhead_engines.apu_master.get_state() == 1,
                ac_state.get_curr_param(APU_N1) > 90,
                engine_panel.en_start.get_state() == 1
            ]

            return all(cond)

        await xp_ac.ACState.data_condition(engine_start)

        async with synoptic_overrides.override_params([ITT, N2, FUEL, OIL,]):
            # after engine start
            # start appears in 1 sec after engine start
            async def ff():
                await synoptic_overrides._1d_table_anim(
                    FUEL,
                    [0, 20, 36], # time
                    [0, 0.001, 0.0377386] # 
                )

            async def N2_anim():
                await synoptic_overrides._1d_table_anim(
                    N2,
                    [0, 1, 8, 32], # time
                    [1, 1, 2, 52] # N2
                )

                await synoptic_overrides.disable_param_overrides([N2])

            async def itt():
                await xp_ac.ACState.wait_until_parameter_condition(IGN, lambda p: p == 1)
                itt_curr = xp_ac.ACState.get_curr_param(ITT)
                await synoptic_overrides._1d_table_anim(
                    ITT,
                    [0, 10], # time
                    [itt_curr, 700] # itt
                )

                await synoptic_overrides.disable_param_overrides([ITT])

            async def oil():
                await synoptic_overrides._1d_table_anim(
                    OIL,
                    [0, 19, 86], # time
                    [0, 5, 69] # 
                )
            
            async def ign():
                # show ign
                await asyncio.sleep(1)
                await xp_ac.ACState.wait_until_parameter_condition(N2, lambda p: p > 16)
                await xp.set_param(IGN, 1)
                # hide ign
                await xp_ac.ACState.wait_until_parameter_condition(N2, lambda p: p > 51)
                await xp.set_param(IGN, 0)
            
            async def start():
                # show start
                await asyncio.sleep(1)
                await xp.set_param(START, 1)
                # hide start
                await xp_ac.ACState.wait_until_parameter_condition(N2, lambda p: p > 51)
                await xp.set_param(START, 0)
            
            async def ab():
                await xp_ac.ACState.wait_until_parameter_condition(N2, lambda p: p > 40)
                await xp.set_param(AB, 1)
                await asyncio.sleep(2)
                await xp.set_param(AB, 0)
            
            await asyncio.gather(ff(), N2_anim(), oil(), itt(), start(), ign(), ab())

    N2 = xp.Params["sim/cockpit2/engine/indicators/N2_percent[0]"]
    ITT = Params["sim/cockpit2/engine/indicators/ITT_deg_C[0]"] 
    IGN = xp.Params["sim/custom/7x/z_syn_eng_ign1"]
    OIL = Params["sim/cockpit2/engine/indicators/oil_pressure_psi[0]"] 
    FUEL = Params["sim/cockpit2/engine/indicators/fuel_flow_kg_sec[0]"]
    START = xp.Params["sim/custom/7x/z_syn_eng_start1"]
    AB = xp.Params["sim/custom/7x/z_syn_eng_ab1"]

    eng1 = engine_start_N(
        N2, ITT, IGN, OIL, FUEL, START, AB,
        engine_panel.en_fuel_1
    )

    N2 = xp.Params["sim/cockpit2/engine/indicators/N2_percent[1]"]
    ITT = Params["sim/cockpit2/engine/indicators/ITT_deg_C[1]"] 
    IGN = xp.Params["sim/custom/7x/z_syn_eng_ign2"]
    OIL = Params["sim/cockpit2/engine/indicators/oil_pressure_psi[1]"] 
    FUEL = Params["sim/cockpit2/engine/indicators/fuel_flow_kg_sec[1]"]
    START = xp.Params["sim/custom/7x/z_syn_eng_start2"]
    AB = xp.Params["sim/custom/7x/z_syn_eng_ab2"]

    eng2 = engine_start_N(
        N2, ITT, IGN, OIL, FUEL, START, AB,
        engine_panel.en_fuel_2
    )

    N2 = xp.Params["sim/cockpit2/engine/indicators/N2_percent[2]"]
    ITT = Params["sim/cockpit2/engine/indicators/ITT_deg_C[2]"] 
    IGN = xp.Params["sim/custom/7x/z_syn_eng_ign3"]
    OIL = Params["sim/cockpit2/engine/indicators/oil_pressure_psi[2]"] 
    FUEL = Params["sim/cockpit2/engine/indicators/fuel_flow_kg_sec[2]"]
    START = xp.Params["sim/custom/7x/z_syn_eng_start3"]
    AB = xp.Params["sim/custom/7x/z_syn_eng_ab3"]

    eng3 = engine_start_N(
        N2, ITT, IGN, OIL, FUEL, START, AB,
        engine_panel.en_fuel_3
    )

    await asyncio.gather(eng1, eng2, eng3)

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
