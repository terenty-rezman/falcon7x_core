from cas import cas
import xplane.master as xp
from xplane.master import Params, Commands
import middle_pedestal.engine as engine_panel
import aircraft_systems.engine as engine_system
import front_panel.warning as warning
import common.external_sound as sounds


async def reset_all_systems():
    await cas.remove_all_messages()
    await xp.run_command_once(Commands["sim/operation/fix_all_systems"])

    engine_system.EngineStart1.broken_start = engine_system.BrokenStart.NORMAL_START
    engine_system.EngineStart2.broken_start = engine_system.BrokenStart.NORMAL_START
    engine_system.EngineStart3.broken_start = engine_system.BrokenStart.NORMAL_START

    await engine_panel.en_fuel_digital_1.set_state(1)
    await engine_panel.en_fuel_digital_2.set_state(1)
    await engine_panel.en_fuel_digital_3.set_state(1)

    await warning.master_caution_lh.set_state(0)
    await warning.master_caution_rh.set_state(0)
    await warning.master_warning_lh.set_state(0)
    await warning.master_warning_rh.set_state(0)

    await sounds.stop_all_sounds()

    MAX_THRUST_1 = xp.Params["sim/custom/7x/z_thrust_purple_max_deg_1"]
    MAX_THRUST_2 = xp.Params["sim/custom/7x/z_thrust_purple_max_deg_2"]
    MAX_THRUST_3 = xp.Params["sim/custom/7x/z_thrust_purple_max_deg_3"]
    await xp.set_param(MAX_THRUST_1, 75)
    await xp.set_param(MAX_THRUST_2, 75)
    await xp.set_param(MAX_THRUST_3, 75)


