from aircraft_systems.fire_protection import APUFireProtection, RearCompFireProtection, BagCompFireProtection
from aircraft_systems.engine import EngineStart1, EngineStart2, EngineStart3, ApuStart, Engine1CustomSpecs
from aircraft_systems.elec import Gen1, Gen2, Gen3, Apu, ElecLinePower
from aircraft_systems.black_screens import LeftBlackScreen, RightBlackScreen, MiddleUpBlackScreen, MiddleDownBlackScreen, MiniBlackScreen


class Systems:
    all_systems = [
        APUFireProtection,
        RearCompFireProtection,
        BagCompFireProtection,
        EngineStart1, EngineStart2, EngineStart3, ApuStart,
        Gen1, Gen2, Gen3, Apu, ElecLinePower,
        LeftBlackScreen, RightBlackScreen, MiddleUpBlackScreen, MiddleDownBlackScreen, MiniBlackScreen,
        Engine1CustomSpecs
    ]

    @classmethod
    def update(cls):
        for s in cls.all_systems:
            s.update()
    
    @classmethod
    async def reset(cls):
        for s in cls.all_systems:
            await s.reset()
