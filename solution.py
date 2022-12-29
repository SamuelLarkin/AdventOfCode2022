#!/usr/bin/env  python3

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



def parser(data: str="data") -> Generator[, None, None]:
    """
    """
    with open(data, mode="r", encoding="UTF8") as fin:
        for line in map(str.strip, fin):
            pass



def part1(data: str="data") -> int:
    """
    """
    return 0



def part2(data: str="data") -> int:
    """
    """
    return 0





if __name__ == "__main__":
    assert (answer := part1("test")) == 152, answer
    answer = part1()
    print(f"Part1 answer: {answer}")
    assert answer == 69289, answer

    assert (answer := part2("test")) == 301, answer
    answer = part2()
    print(f"Part2 answer: {answer}")
    assert answer == 205615, answer
