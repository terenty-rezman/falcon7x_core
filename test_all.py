import common.util as util


def test_dead_zone():
    assert util.dead_zone(0, -10, 10, 1) == 0
    assert util.dead_zone(-10, -10, 10, 1) == -10 
    assert util.dead_zone(10, -10, 10, 1) == 10 
    assert util.dead_zone(1, -10, 10, 1) == 0
    assert util.dead_zone(-1, -10, 10, 1) == 0
    assert util.dead_zone(-1, -10, 10, 1) == 0


def _all():
    test_dead_zone()


if __name__ == "__main__":
    _all()


