from solution import (
        is_touching,
        Position,
        )
import pytest



@pytest.mark.parametrize(
        "head,tail,answer",
        (
            # Distance 1
            (Position(0, 0), Position(1, 1), True),
            (Position(0, 0), Position(1, 0), True),
            (Position(0, 0), Position(1, -1), True),
            (Position(0, 0), Position(-1, 1), True),
            (Position(0, 0), Position(-1, 0), True),
            (Position(0, 0), Position(-1, -1), True),
            (Position(0, 0), Position(0, 1), True),
            (Position(0, 0), Position(0, -1), True),
            # Distance 2
            (Position(0, 0), Position(-1, 2), False),
            (Position(0, 0), Position(0, 2), False),
            (Position(0, 0), Position(1, 2), False),
            (Position(0, 0), Position(-1, -2), False),
            (Position(0, 0), Position(0, -2), False),
            (Position(0, 0), Position(1, -2), False),
            (Position(0, 0), Position(-2, -1), False),
            (Position(0, 0), Position(-2, 0), False),
            (Position(0, 0), Position(-2, 1), False),
            (Position(0, 0), Position(2, -1), False),
            (Position(0, 0), Position(2, 0), False),
            (Position(0, 0), Position(2, 1), False),
            (Position(0, 0), Position(2, 2), False),
            (Position(0, 0), Position(2, -2), False),
            (Position(0, 0), Position(-2, 2), False),
            (Position(0, 0), Position(-2, -2), False),
            )
        )
def test_touching(head, tail, answer):
    """
    """
    assert is_touching(head, tail) == answer
