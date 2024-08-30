#!/usr/bin/env  python3

from collections import defaultdict
from dataclasses import dataclass
from itertools import product
from operator import attrgetter
from tqdm import trange
from typing import (
        Callable,
        Generator,
        Iterable,
        List,
        NamedTuple,
        Sequence,
        Tuple,
        Union,
        )

import heapq
import math



StepNumber = int
Distance = int
BlizzardSetId = int



class Position(NamedTuple):
    x: int
    y: int

    def __add__(self, other) -> "Position":
        """
        """
        return Position(self.x+other.x, self.y+other.y)


DIRECTIONS = {
        "^": Position(0, -1),
        "v": Position(0, 1),
        "<": Position(-1, 0),
        ">": Position(1, 0),
        "DONT_MOVE": Position(0, 0),
        }
DIRECTION2SYMBOL = {v: k for k, v in DIRECTIONS.items()}
assert len(DIRECTIONS) == len(DIRECTION2SYMBOL)



class Blizzard(NamedTuple):
    position: Position
    direction: Position



def parser(data: str="data"):
    """
    """
    blizzards = []
    with open(data, mode="r", encoding="UTF8") as fin:
        fin = iter(map(str.strip, fin))
        line = next(fin)
        width = len(line) - 2
        start = Position(0, -1)
        for y, line in enumerate(fin):
            if line.startswith("##"):
                continue
            # Remove left board so the coordinates are [0, width).
            for x, v in enumerate(line, start=-1):
                if v in (".", "#"):
                    continue
                blizzards.append(Blizzard(Position(x, y), DIRECTIONS[v]))

    height = y
    end = Position(width-1, height)

    assert all(0 <= blizzard.position.x < width  for blizzard in blizzards)
    assert all(0 <= blizzard.position.y < height for blizzard in blizzards)

    return start, end, (width, height), tuple(blizzards)



def move_blizzards(
        blizzards: Iterable[Blizzard],
        width: int,
        height: int,
        ) -> Generator[Blizzard, None, None]:
    """
    """
    for blizzard in blizzards:
        x, y = blizzard.position + blizzard.direction
        yield Blizzard(
                position=Position(x%width, y%height),
                direction=blizzard.direction,
                )



class State(NamedTuple):
    step: StepNumber   # Number of step so far
    position: Position
    distance_to_end: Distance

    @property
    def score(self) -> int:
        """
        """
        assert self.distance_to_end >= 0
        return self.step + self.distance_to_end

    def __lt__(self, other) -> bool:
        """
        """
        return self.score < other.score



def distance(a: Position, b: Position) -> Distance:
    """
    """
    return abs(a.x-b.x) + abs(a.y-b.y)



def display_valley(blizzards: Sequence[Blizzard], width: int, height: int):
    """
    """
    assert all(0 <= blizzard.position.x < width  for blizzard in blizzards)
    assert all(0 <= blizzard.position.y < height for blizzard in blizzards)

    blizzards = { blizzard.position: blizzard for blizzard in blizzards }
    for y in range(height):
        for x in range(width):
            p = Position(x, y)
            if p in blizzards:
                print(DIRECTION2SYMBOL[blizzards[p].direction], sep="", end="")
            else:
                print(".", sep="", end="")
        print()



def test_move_blizzards():
    """
    """
    start, end, (width, height), blizzards = parser("test")
    for i in range(18):
        print(f"Step {i}")
        display_valley(blizzards, width, height)
        print()
        blizzards = list(move_blizzards(blizzards, width, height))



def solve(
        start: Position,
        ends: Position,
        width: int,
        height: int,
        blizzards: Tuple[Blizzard]) -> int:
    """
    """
    end = ends.pop()
    modulo = width * height // math.gcd(width, height)

    all_allowed_positions = []
    all_positions = frozenset(Position(x, y) for x, y in product(range(width), range(height)))
    all_positions = frozenset(all_positions | {start, end})
    for _ in trange(modulo, desc="Caching valid positions"):
        allowed_positions = frozenset(all_positions - set(map(attrgetter("position"), blizzards)))
        all_allowed_positions.append(allowed_positions)
        blizzards = tuple(move_blizzards(blizzards, width, height))

    best: Dict[Tuble[Position, BlizzardSetId], StepNumber] = defaultdict(lambda: math.inf)
    states = [State(
        step=0,
        position=start,
        distance_to_end=distance(start, end),
        )]
    while len(states) > 0:
        state = heapq.heappop(states)
        #print(f"#States: {len(states)}, State: {state}")

        if state.distance_to_end == 0:
            if len(ends) == 0:
                return state.step
            else:
                start = end
                assert state.position == start
                end = ends.pop()
                best = defaultdict(lambda: math.inf)
                states = [State(
                    step=step,
                    position=start,
                    distance_to_end=distance(start, end),
                    )]
                continue

        blizzard_set_id = state.step % modulo
        if state.step < best[(state.position, blizzard_set_id)]:
            best[(state.position, blizzard_set_id)] = state.step
        else:
            # We previously arrived here from a shorter path.
            continue

        # We accidentally moved into a blizzard, skip it.
        assert state.position in all_allowed_positions[blizzard_set_id]

        # Checking next step
        step = state.step + 1
        blizzard_set_id = step % modulo
        allowed_positions = all_allowed_positions[blizzard_set_id]

        for position in map(lambda d: state.position+d, DIRECTIONS.values()):
            if position in allowed_positions:
                # There is no blizzard there.
                next_state = State(
                        step=step,
                        position=position,
                        distance_to_end=distance(position, end),
                        )
                heapq.heappush(states, next_state)

    return None



def part1(data: str="data") -> int:
    """
    What is the fewest number of minutes required to avoid the blizzards and reach the goal?
    """
    start, end, (width, height), blizzards = parser(data)

    return solve(start, [end], width, height, blizzards)



def part2(data: str="data") -> int:
    """
    What is the fewest number of minutes required to reach the goal, go back to the start, then reach the goal again?
    """
    start, end, (width, height), blizzards = parser(data)

    return solve(start, [end, start, end], width, height, blizzards)





if __name__ == "__main__":
    #test_move_blizzards()
    #print(*part1(), sep="\n")

    assert (answer := part1("test")) == 18, answer
    answer = part1()
    print(f"Part1 answer: {answer}")
    assert answer == 288

    print()

    assert (answer := part2("test")) == 54, answer
    answer = part2()
    print(f"Part2 answer: {answer}")
    assert answer == 205615
    # 759 too low
