from aircraft_systems.fire_protection import APUFireProtection, RearCompFireProtection, BagCompFireProtection


class Systems:
    all_systems = [
        APUFireProtection,
        RearCompFireProtection,
        BagCompFireProtection
    ]

    @classmethod
    async def update(cls):
        for s in cls.all_systems:
            await s.update()
    
    @classmethod
    async def reset(cls):
        for s in cls.all_systems:
            await s.reset()
