#!/usr/bin/env  python3

from collections import Counter
from more_itertools import windowed
from typing import (
        Generator,
        List,
        Tuple,
        )



def parser() -> str:
    """
    """
    with open("data", mode="r", encoding="UTF8") as fin:
        return fin.readline().strip()



def part1(marker_length: int=4) -> int:
    """
    How many characters need to be processed before the first start-of-packet marker is detected?
    """
    def is_marker(window: str) -> bool:
        """
        The start of a packet is indicated by a sequence of four characters
        that are all different.
        """
        assert len(window) == marker_length
        a, b, c, d = window
        return not (a == b or a == c or a == d \
                or b == c or b == d \
                or c == d)

    datastream = parser()
    for i, window in enumerate(windowed(datastream, marker_length)):
        if is_marker(window):
            return i + marker_length



def part2(marker_length: int=14) -> int:
    """
    How many characters need to be processed before the first start-of-message marker is detected?
    """
    def is_marker(window: str) -> bool:
        """
        A start-of-message marker is just like a start-of-packet marker, except
        it consists of 14 distinct characters rather than 4.
        """
        assert len(window) == marker_length
        c = Counter(window)
        # [('r', 4)]
        return c.most_common(1)[0][1] == 1

    datastream = parser()
    for i, window in enumerate(windowed(datastream, marker_length)):
        if is_marker(window):
            return i + marker_length





if __name__ == "__main__":
    answer = part1()
    print(f"Part1 answer: {answer}")
    assert answer == 1531

    answer = part2()
    print(f"Part2 answer: {answer}")
    assert answer == 205615
