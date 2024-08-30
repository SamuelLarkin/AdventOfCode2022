from solution import (
        Blizzard,
        Position,
        move_blizzards,
        )

import pytest


@pytest.mark.parametrize(
        "blizzard,width,height,answer",
        (
            (Blizzard(Position(0, 0), Position(1, 0)),  3, 1, Position(1, 0)),
            (Blizzard(Position(1, 0), Position(1, 0)),  3, 1, Position(2, 0)),
            (Blizzard(Position(2, 0), Position(1, 0)),  3, 1, Position(0, 0)),
            (Blizzard(Position(0, 0), Position(-1, 0)), 3, 1, Position(2, 0)),

            (Blizzard(Position(0, 0), Position(0, 1)),  1, 3, Position(0, 1)),
            (Blizzard(Position(0, 1), Position(0, 1)),  1, 3, Position(0, 2)),
            (Blizzard(Position(0, 2), Position(0, 1)),  1, 3, Position(0, 0)),
            (Blizzard(Position(0, 0), Position(0, -1)), 1, 3, Position(0, 2)),
            )
        )
def test_move_blizzards(
        blizzard: Blizzard,
        width: int,
        height: int,
        answer: Position,
        ):
    blizzard = next(move_blizzards((blizzard,), width, height))
    assert blizzard.position == answer
