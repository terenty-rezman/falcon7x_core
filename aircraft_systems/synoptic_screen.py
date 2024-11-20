import xplane.master as xp


SynopcicPages = {
    "STAT": 0,
    "ENG": 1,
    "ELEC": 2,
    "FUEL": 3,
    "HYD": 4,
    "ECS": 5, 
    "BLD": 6,
    "FCS": 7,
    "TEST": 8
}


class SynopticScreen:
    @classmethod
    async def set_active_page(cls, page_name: str):
        page = SynopcicPages.get(page_name)
        if page is None:
            return False

        await xp.set_param(xp.Params["sim/cockpit/weapons/firing_rate"], page)
        return True
