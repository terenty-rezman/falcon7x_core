from common.instrument_panel import add_to_panel, TwoStateButton, FloatStepper, NLocalStateButton
from xplane.params import Params, Commands
import xplane.master as xp
import common.xp_aircraft_state as xp_ac
import common.util as util
import math

import cas.cas as cas




# "O12_c31",  # Дым [K4 Верхний пульт] [Зона освещения] [Пульт инструктора]
@add_to_panel
class misc_smoke(NLocalStateButton):
    states = [0, 1]
    state = 0


# "O12_c29",  # Подача [K4 Верхний пульт] [Зона освещения] [Пульт инструктора]
@add_to_panel
class misc_supply(NLocalStateButton):
    states = [0, 1]
    state = 0


# "O12_c30",  # Вытяжка [K4 Верхний пульт] [Зона освещения] [Пульт инструктора]
@add_to_panel
class misc_extract(NLocalStateButton):
    states = [0, 1]
    state = 0
