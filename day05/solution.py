#!/usr/bin/env  python3

from collections import namedtuple
from typing import (
        Generator,
        List,
        Tuple,
        )



# NOTE: the from_ & to_ are 1-based indexed.
Instruction = namedtuple("Instruction", ("move_", "from_", "to_"))



def parser() -> Tuple[List, Generator[Instruction, None, None]]:
    """
    [B]                     [N]     [H]
    [V]         [P] [T]     [V]     [P]
    [W]     [C] [T] [S]     [H]     [N]
    [T]     [J] [Z] [M] [N] [F]     [L]
    [Q]     [W] [N] [J] [T] [Q] [R] [B]
    [N] [B] [Q] [R] [V] [F] [D] [F] [M]
    [H] [W] [S] [J] [P] [W] [L] [P] [S]
    [D] [D] [T] [F] [G] [B] [B] [H] [Z]
     1   2   3   4   5   6   7   8   9

    move 2 from 8 to 1
    move 4 from 9 to 8
    move 2 from 1 to 6
    move 7 from 4 to 2
    move 10 from 2 to 7
    """
    def parse_move(line: str) -> Instruction:
        """
        """
        _, move_, _, from_, _, to_ = line.split()
        return Instruction(int(move_), int(from_), int(to_))

    stacks = [[] for _ in range(9)]
    fin = open("data", mode="r", encoding="UTF8")

    for line in map(str.strip, fin):
        if line == "" or line.startswith(" "):
            break
        for i in range(9):
            s = 4*i+1
            if s < len(line):
                l = line[s]
                if l != " ":
                    stacks[i].append(l)
    for s in stacks:
        s.reverse()

    def parser2():
        for line in map(str.strip, fin):
            yield parse_move(line)
        fin.close()

    return stacks, parser2()



def top_crate_message(stacks: List[List[str]]) -> str:
    """
    """
    return ''.join(s.pop() for s in stacks)



def part1() -> str:
    """
    After the rearrangement procedure completes, what crate ends up on top of each stack?
    """
    stacks, moves = parser()
    if False:
        print(stacks)
        print(*enumerate(moves), sep="\n")

    for m, f, t in moves:
        for _ in range(m):
            stacks[t-1].append(stacks[f-1].pop())

    return top_crate_message(stacks)



def part2() -> int:
    """
    After the rearrangement procedure completes, what crate ends up on top of each stack?
    """
    stacks, moves = parser()
    for m, f, t in moves:
        a = stacks[f-1][-m:]
        stacks[f-1] = stacks[f-1][:-m]
        stacks[t-1].extend(a)

    return top_crate_message(stacks)





if __name__ == "__main__":
    answer = part1()
    print(f"Part1 answer: {answer}")
    assert answer == "PSNRGBTFT"

    answer = part2()
    print(f"Part2 answer: {answer}")
    assert answer == "BNTZFPMMW"
