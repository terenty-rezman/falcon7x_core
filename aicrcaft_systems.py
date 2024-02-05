from apu import APUFireProtection


class Systems:
    all_systems = [
        APUFireProtection
    ]

    @classmethod
    async def update(cls):
        for s in cls.all_systems:
            await s.update()
    
    @classmethod
    async def reset(cls):
        for s in cls.all_systems:
            await s.reset()
