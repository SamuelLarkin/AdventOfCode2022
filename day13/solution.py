#!/usr/bin/env  python3

from functools import cmp_to_key
from operator import itemgetter
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



class Pair(NamedTuple):
    left: Union[int, List]
    right: Union[int, List]



def parser(data: str="data") -> Generator[Pair, None, None]:
    """
    """
    with open(data, mode="r", encoding="UTF8") as fin:
        for left in map(str.strip, fin):
            if left == "":
                continue
            right = fin.readline().strip()
            yield Pair(
                    eval(left),
                    eval(right),
                    )



def cmp(left, right) -> int:
    """
    Returns:
    * 0 if no decision was made
    * a negative integer if in the correct order
    * a positive integer not in the correct order
    """
    if isinstance(left, int) and isinstance(right, int):
        return left - right
    elif isinstance(left, list) and isinstance(right, list):
        for l, r in zip(left, right):
            c = cmp(l, r)
            if c != 0:
                return c
        return len(left) - len(right)
    else:
        if isinstance(left, int):
            return cmp([left], right)
        else:
            return cmp(left, [right])

    return False



def part1() -> int:
    """
    What is the sum of the indices of those pairs?
    """
    pairs = parser()
    is_ordered = map(lambda p: cmp(*p), pairs)
    correct_order = filter(lambda x: x[1] <= 0, enumerate(is_ordered, start=1))

    return sum(map(itemgetter(0), correct_order))



def part2() -> int:
    """
    What is the decoder key for the distress signal?
    """
    def flat(iterable: Iterable[Pair]):
        """
        """
        for p in iterable:
            yield p.left
            yield p.right

    marker1 = [[2]]
    marker2 = [[6]]
    packets = list(flat(parser()))
    packets.append(marker1)
    packets.append(marker2)

    packets = sorted(packets, key=cmp_to_key(cmp))

    marker_positions = filter(lambda x: x[1] in (marker1, marker2), enumerate(packets, start=1))
    marker_positions = list(map(itemgetter(0), marker_positions))
    assert len(marker_positions) == 2

    return marker_positions[0] * marker_positions[1]





if __name__ == "__main__":
    answer = part1()
    print(f"Part1 answer: {answer}")
    assert answer == 5852

    answer = part2()
    print(f"Part2 answer: {answer}")
    assert answer == 24190
