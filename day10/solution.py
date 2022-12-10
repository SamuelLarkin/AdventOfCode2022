#!/usr/bin/env  python3

from typing import (
        Generator,
        Iterable,
        List,
        Tuple,
        )



def parser(data: str="data") -> Generator[int, None, None]:
    """
    """
    with open(data, mode="r", encoding="UTF8") as fin:
        yield 0
        for line in map(str.strip, fin):
            op, *arg = line.split()
            if op == "noop":
                yield 0
            elif op == "addx":
                assert len(arg) == 1
                arg = arg[0]
                yield 0
                yield int(arg)
            else:
                assert False



def cumsum(strengths: Iterable[int], start: int=1) -> Generator[int, None, None]:
    """
    """
    for s in strengths:
        start += s
        yield start



def part1() -> int:
    """
    What is the sum of these six signal strengths?
    """
    signals = (20, 60, 100, 140, 180, 220)
    strengths = list(cumsum(parser()))
    if False:
        print(*enumerate(strengths, 1), sep="\n")

        for s in signals:
            print(s, strengths[s-1])

    return sum(strengths[s-1]* s for s in signals)



CRT_WIDTH = 40
def part2() -> None:
    """
    Render the image given by your program.
    What eight capital letters appear on your CRT?
    """
    strengths = list(cumsum(parser()))
    crt = ["." for _ in range(len(strengths))]
    for x, s in enumerate(strengths):
        xx = x % CRT_WIDTH
        if s-1 <= xx <= s+1:
            crt[x] = "#"

    for y in range(len(strengths)//CRT_WIDTH):
        print(''.join(crt[y*CRT_WIDTH:(y+1)*CRT_WIDTH]))





if __name__ == "__main__":
    answer = part1()
    print(f"Part1 answer: {answer}")
    assert answer == 12520

    part2()
    answer = "EHPZPJGL"
    print(f"Part2 answer: {answer}")
    #assert answer == 205615
