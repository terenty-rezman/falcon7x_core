from aircraft_systems.synoptic_screen import SynopticScreen
from mfi.mfi import mfi_button_on_click, BOX


@mfi_button_on_click(
    "MID", BOX(5, 364, 84, 396)
)
async def synoptic_stat_click():
    await SynopticScreen.set_active_page("STAT")


@mfi_button_on_click(
    "MID", BOX(91, 364, 169, 396)
)
async def synoptic_eng_click():
    await SynopticScreen.set_active_page("ENG")


@mfi_button_on_click(
    "MID", BOX(176, 364, 256, 396)
)
async def synoptic_elec_click():
    await SynopticScreen.set_active_page("ELEC")


@mfi_button_on_click(
    "MID", BOX(262, 364, 340, 396)
)
async def synoptic_fuel_click():
    await SynopticScreen.set_active_page("FUEL")


@mfi_button_on_click(
    "MID", BOX(345, 364, 427, 396)
)
async def synoptic_hyd_click():
    await SynopticScreen.set_active_page("HYD")


@mfi_button_on_click(
    "MID", BOX(433, 364, 513, 396)
)
async def synoptic_ecs_click():
    await SynopticScreen.set_active_page("ECS")


@mfi_button_on_click(
    "MID", BOX(518, 364, 597, 396)
)
async def synoptic_bld_click():
    await SynopticScreen.set_active_page("BLD")


@mfi_button_on_click(
    "MID", BOX(518, 364, 597, 396)
)
async def synoptic_bld_click():
    await SynopticScreen.set_active_page("BLD")


@mfi_button_on_click(
    "MID", BOX(604, 364, 684, 396)
)
async def synoptic_fcs_click():
    await SynopticScreen.set_active_page("FCS")


@mfi_button_on_click(
    "MID", BOX(689, 364, 769, 396)
)
async def synoptic_test_click():
    await SynopticScreen.set_active_page("TEST")
