# PYTHONPATH=. pytest unittest

from solution import (
        follow,
        Position,
        )

import pytest



@pytest.mark.parametrize(
        "head,tail,new_tail",
        (
            # Top
            (Position(0, 0), Position(-1, 2), Position(0, 1)),
            (Position(0, 0), Position(0, 2), Position(0, 1)),
            (Position(0, 0), Position(1, 2), Position(0, 1)),
            # Bottom
            (Position(0, 0), Position(-1, -2), Position(0, -1)),
            (Position(0, 0), Position(0, -2), Position(0, -1)),
            (Position(0, 0), Position(1, -2), Position(0, -1)),
            # Left
            (Position(0, 0), Position(-2, 1), Position(-1, 0)),
            (Position(0, 0), Position(-2, 0), Position(-1, 0)),
            (Position(0, 0), Position(-2, -1), Position(-1, 0)),
            # Right
            (Position(0, 0), Position(2, 1), Position(1, 0)),
            (Position(0, 0), Position(2, 0), Position(1, 0)),
            (Position(0, 0), Position(2, -1), Position(1, 0)),
            )
        )
def test_follow(head, tail, new_tail):
    assert follow(tail, head) == new_tail
