import asyncio
import numpy as np

from instrument_panel import FloatStepper
import uso.uso_send as uso_send


class test_float_tester(FloatStepper):
    logic_left = -100
    logic_right = 100

    left_most_value = -10
    right_most_value = 10

    state = 0
    step = 0.1

    val_type = float


async def main():
    uso_send.create_packet(None)
    print("s")



asyncio.run(main())
