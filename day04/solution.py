#!/usr/bin/env  python3


from collections import namedtuple
from typing import (
        Generator,
        Tuple,
        )

Tasks = namedtuple("Tasks", ("min", "max"))


def parse() -> Generator[Tuple[Tasks, Tasks], None, None]:
    """
    2-4,6-8
    2-3,4-5
    5-7,7-9
    2-8,3-7
    6-6,4-6
    2-6,4-8
    """
    def createTask(l: str) -> Tasks:
        return Tasks(*map(int, l.split("-")))

    with open("data", mode="r", encoding="UTF8") as fin:
        for line in map(str.strip, fin):
            one, two = line.split(",")
            yield createTask(one), createTask(two)



def part1() -> int:
    """
    In how many assignment pairs does one range fully contain the other?
    """
    def overlap(t1: Tasks, t2: Tasks) -> bool:
        """
        """
        if t1.max - t1.min < t2.max - t2.min:
            """
            t1 is the biggest of the two.
            """
            t1, t2 = t2, t1
        assert t1.max - t1.min >= t2.max - t2.min

        if t1.min <= t2.min:
            return t2.max <= t1.max

        return False

    return len(list(filter(lambda t: overlap(*t), parse())))



def part2() -> int:
    """
    In how many assignment pairs do the ranges overlap?
    """
    def overlap(t1: Tasks, t2: Tasks) -> bool:
        """
        t1 and t2 don't overlap when either t1 is ALL to left of t2 or t1 is completely all to the right of t2.
        """
        return not ( t1.max < t2.min or t2.max < t1.min)

    return len(list(filter(lambda t: overlap(*t), parse())))



if __name__ == "__main__":
    answer = part1()
    print(f"Part1 answer: {answer}")
    assert answer == 509

    answer = part2()
    print(f"Part2 answer: {answer}")
    assert answer == 870
