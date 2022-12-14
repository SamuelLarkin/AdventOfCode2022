#!/usr/bin/env  python3

from itertools import tee
from operator import attrgetter
from typing import (
        Callable,
        Dict,
        Generator,
        Iterable,
        List,
        NamedTuple,
        Sequence,
        Tuple,
        Union,
        )



class Position(NamedTuple):
    x: int
    y: int



# Order of directions is important
DIRECTIONS = (
        Position(0, 1),
        Position(-1, 1),
        Position(1, 1),
        )



def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)



CaveMap = Dict[Position, str]
def parser(data: str="data") -> CaveMap:
    """
    """
    def location(line: str) -> Generator[Position, None, None]:
        """
        """
        points = line.split("->")
        for point in points:
            x, y = point.strip().split(",")
            yield Position(
                    x=int(x),
                    y=int(y),
                    )

    cave_map: CaveMap = dict()
    with open(data, mode="r", encoding="UTF8") as fin:
        for line in map(str.strip, fin):
            # 503,4 -> 502,4 -> 502,9 -> 494,9
            for start, end in pairwise(location(line)):
                if start.x == end.x:
                    for y in range(min(start.y, end.y), max(start.y, end.y)+1):
                        cave_map[Position(start.x, y)] = "#"
                elif start.y == end.y:
                    for x in range(min(start.x, end.x), max(start.x, end.x)+1):
                        cave_map[Position(x, start.y)] = "#"
                else:
                    assert False

    return cave_map



def find_next_position(current: Position, cave: CaveMap) -> Union[Position, None]:
    """
    Tries to find the next position a grain of sand could go.
    """
    for next_position in map(lambda d: Position(current.x + d.x, current.y + d.y), DIRECTIONS):
        if next_position not in cave:
            return next_position

    return None



def part1() -> int:
    """
    How many units of sand come to rest before sand starts flowing into the abyss below?
    """
    source = Position(500, 0)
    cave = parser()
    max_height = max(map(attrgetter("y"), cave)) + 2
    for t in range(10_000):
        current_position = source
        for s in range(max_height):
            next_position = find_next_position(current_position, cave)
            if next_position is None:
                # Sand has come to a stand still.
                assert current_position not in cave
                cave[current_position] = "o"
                break
            else:
                current_position = next_position
        else:
            # Sand is flowing into the abyss because we could find a next position.
            return t

    return None



def part2() -> int:
    """
    How many units of sand come to rest?
    """
    source = Position(500, 0)
    cave = parser()
    max_height = max(map(attrgetter("y"), cave)) + 2
    for t in range(100_000):
        current_position = source
        for s in range(max_height+2):
            next_position = find_next_position(current_position, cave)
            if next_position is None:
                # Sand has come to a stand still.
                if current_position == source:
                    return t+1
                assert current_position not in cave
                cave[current_position] = "o"
                break
            else:
                if next_position.y < max_height:
                    current_position = next_position
                else:
                    # We have reached the cave's bottom floor.
                    assert current_position not in cave
                    cave[current_position] = "o"
                    break

    return None





if __name__ == "__main__":
    answer = part1()
    print(f"Part1 answer: {answer}")
    assert answer == 1001

    answer = part2()
    print(f"Part2 answer: {answer}")
    assert answer == 27976
