#!/usr/bin/env  python3

from typing import (
        Generator,
        List,
        Tuple,
        )



def parser(data: str="data") -> Generator[, None, None]:
    """
    """
    with open(data, mode="r", encoding="UTF8") as fin:
        for line in map(str.strip, fin):
            pass



def part1() -> int:
    """
    """
    return 0



def part2() -> int:
    """
    """
    return 0





if __name__ == "__main__":
    answer = part1()
    print(f"Part1 answer: {answer}")
    assert answer == 69289

    answer = part2()
    print(f"Part2 answer: {answer}")
    assert answer == 205615
