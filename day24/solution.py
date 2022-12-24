#!/usr/bin/env  python3

from dataclasses import dataclass
from operator import attrgetter
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



@dataclass
class Blizzard:
    position: Position
    direction: Position



def parser(data: str="data"):
    """
    """
    blizzards = []
    with open(data, mode="r", encoding="UTF8") as fin:
        fin = iter(map(str.strip, fin))
        line = next(fin)
        width = len(line) - 1
        start = Position(0, -1)
        for y, line in enumerate(fin):
            if line.startswith("##"):
                continue
            # Remove left board so the coordinates are [0, width).
            for x, v in enumerate(line, start=-1):
                if v in (".", "#"):
                    continue
                blizzards.append(Blizzard(Position(x, y), DIRECTIONS[v]))

    height = y - 1
    end = Position(width-1, height)
    return start, end, (width, height), blizzards



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
    step: int   # Number of step so far
    position: Position
    distance_to_end: int
    blizzards: List[Blizzard]

    @property
    def score(self) -> int:
        """
        """
        assert self.distance_to_end >= 0
        return self.step + self.distance_to_end

    def __lt__(self, other) -> bool:
        """
        """
        #return self.score < other.score and self.step < other.step
        return self.step < other.step and self.score < other.score



def distance(a: Position, b: Position) -> int:
    """
    """
    return abs(a.x-b.x) + abs(a.y-b.y)



def part1(data: str="data") -> int:
    """
    What is the fewest number of minutes required to avoid the blizzards and reach the goal?
    """
    start, end, (width, height), blizzards = parser(data)
    states = [State(
        step=0,
        position=start,
        distance_to_end=distance(start, end),
        blizzards=blizzards,
        )]
    while len(states) > 0:
        #heapq.heapify(states)
        state = heapq.heappop(states)
        print(len(states), state.score)

        if state.distance_to_end == 0:
            return state.step
        if state.position == end:
            return state.step
        #if state.position in set(map(attrgetter("position"), blizzards)):
        #    # We accidentally moved into a blizzard, skip it.
        #    continue


        blizzards = list(move_blizzards(blizzards, width, height))

        for position in map(lambda d: state.position+d, DIRECTIONS.values()):
            if position == end:
                assert False
            if 0 <= position.x < width and 0 <= position.y < height:
                # We are still in the valley.
                if position not in set(map(attrgetter("position"), blizzards)):
                    # There is no blizzard there.
                    heapq.heappush(
                            states,
                            State(
                                step=state.step+1,
                                position=position,
                                distance_to_end=distance(position, end),
                                blizzards=blizzards,
                                ))

    return 0



def part2(data: str="data") -> int:
    """
    """
    return 0





if __name__ == "__main__":
    assert (answer := part1("test")) == 18, answer
    answer = part1()
    print(f"Part1 answer: {answer}")
    assert answer == 69289

    assert (answer := part2("test")) == 301, answer
    answer = part2()
    print(f"Part2 answer: {answer}")
    assert answer == 205615
