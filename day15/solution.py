#!/usr/bin/env  python3

from functools import reduce
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


import re


sensor_re = re.compile(r"Sensor at x=(?P<sx>-?\d+), y=(?P<sy>-?\d+): closest beacon is at x=(?P<bx>-?\d+), y=(?P<by>-?\d+)")



class Range(NamedTuple):
    """
    """
    m: int   # min
    M: int   # max

    def __post_init__(self):
        """
        """
        if self.M < self.m:
            self.m, self.M = self.M, self.m

    def length(self) -> int:
        """
        """
        return self.M - self.m

    def merge(self, other: "Range") -> List["Range"]:
        """
        """
        a, b = self, other
        if b < a:
            a, b = b, a

        if a.M+1 >= b.m:
            return [Range(m=min(a.m,b.m), M=max(a.M,b.M))]
        else:
            return [a, b]



class Position(NamedTuple):
    """
    """
    x: int
    y: int



class Sensor(NamedTuple):
    """
    """
    p: Position
    d: int    # distance

    def inside(self, beacon: Position) -> bool:
        """
        """
        return abs(self.p.x-beacon.x)+abs(self.p.y-beacon.y) <= self.d


    def range(self, y: int) -> Range:
        """
        """
        if not self.inside(Position(self.p.x, y)):
            return None

        dy = abs(self.p.y - y)
        l = self.d - dy

        return Range(m=self.p.x-l, M=self.p.x+l)



def merge_ranges(ranges: Sequence[Range]) -> List[Range]:
    """
    """
    ranges = sorted(ranges)

    all_merged: List[Range]=[]
    merged: Range=ranges[0]
    for s in ranges[1:]:
        m = merged.merge(s)
        if len(m) == 1:
            merged = m[0]
        else:
            all_merged.append(m[0])
            merged = m[1]
    all_merged.append(merged)

    return all_merged



def parser(data: str="data") -> Generator[Sensor, None, None]:
    """
    """
    # Sensor at x=-13, y=2: closest beacon is at x=15, y=3
    with open(data, mode="r", encoding="UTF8") as fin:
        for line in map(str.strip, fin):
            m = sensor_re.match(line)
            assert m is not None
            sx = int(m.group("sx"))
            sy = int(m.group("sy"))
            bx = int(m.group("bx"))
            by = int(m.group("by"))
            yield Sensor(p=Position(x=sx, y=sy), d=abs(sx-bx)+abs(sy-by))



def part1(y: int=2_000_000) -> int:
    """
    In the row where y=2000000, how many positions cannot contain a beacon?
    """
    sensors = list(parser())

    ranges = map(lambda s: s.range(y), sensors)
    within_range = filter(lambda r: r is not None, ranges)

    merged = merge_ranges(within_range)
    assert len(merged) == 1

    return merged[0].length()



def part2(c: int=4_000_000) -> int:
    """
    What is its tuning frequency?
    """
    sensors = list(parser())
    for y in trange(c):
        ranges = map(lambda s: s.range(y), sensors)
        within_range = filter(lambda r: r is not None, ranges)

        merged = merge_ranges(within_range)
        if len(merged) > 1:
            assert len(merged) == 2
            p = Position(merged[0].M+1, y)
            break

    return c * p.x + p.y





if __name__ == "__main__":
    answer = part1()
    print(f"Part1 answer: {answer}")
    assert answer == 5508234

    answer = part2()
    print(f"Part2 answer: {answer}")
    assert answer == 10457634860779
