#!/usr/bin/env  python3

from more_itertools import chunked
from typing import (
        Generator,
        Tuple,
        )



def read() -> Generator[Tuple[str, str], None, None]:
    """
    """
    with open("data", mode="r", encoding="UTF8") as fin:
        for line in map(str.strip, fin):
            yield line



def convert(letter: str) -> int:
    """
    """
    if 'a' <= letter <= 'z':
        return ord(letter) - ord('a') + 1
    elif 'A' <= letter <= 'Z':
        return ord(letter) - ord('A') + 1 + 26
    else:
        assert False



def part1() -> int:
    """
    What is the sum of the priorities of those item types?
    """
    rucksacks = map(lambda r: (r[:len(r)//2], r[len(r)//2:]), read())
    rucksacks = map(lambda r: (set(r[0]), set(r[1])), rucksacks)
    share = map(lambda r: r[0] & r[1], rucksacks)
    share = map(lambda r: r.pop(), share)
    values = map(convert, share)

    return sum(values)



def part2() -> int:
    """
    What is the sum of the priorities of those item types?
    """
    g = chunked(read(), 3)
    h = map(lambda a: list(map(set, a)), g)   # Convert the rucksacks into sets of objects.
    i = map(lambda s: set.intersection(*s).pop(), h)   # What item is common amongst to 3 rucksacks?
    j = map(convert, i)   # Convert letters to values

    return sum(j)





if __name__ == "__main__":
    answer = part1()
    print(f"Part 1: {answer}")
    assert answer == 8139

    answer = part2()
    print(f"Part 2: {answer}")
    assert answer == 2668
