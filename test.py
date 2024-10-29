import asyncio

from instrument_panel import FloatStepper


class test_float_tester(FloatStepper):
    logic_left = -100
    logic_right = 100

    left_most_value = -10
    right_most_value = 10

    state = 0
    step = 0.1

    val_type = float


async def main():
    await test_float_tester.set_state(-50)
    print(test_float_tester.get_state())
    print("done")


asyncio.run(main())
