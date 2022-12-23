#!/usr/bin/env  python3

from enum import Enum
from more_itertools import pairwise
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

import json
import re



class Direction(Enum):
    R = 0
    D = 1
    L = 2
    U = 3
TURNS = {
        Direction.R: {"R": Direction.D, "L": Direction.U},
        Direction.D: {"R": Direction.L, "L": Direction.R},
        Direction.L: {"R": Direction.U, "L": Direction.D},
        Direction.U: {"R": Direction.R, "L": Direction.L},
        }



class Position(NamedTuple):
    x: int
    y: int



class LocationInfo:
    """
    """
    def __init__(self, type:str):
        """
        """
        self.type = type
        self.neighbors: Dict[Direction, Tuple[Position, Direction]] = {
            Direction.R: None,
            Direction.D: None,
            Direction.L: None,
            Direction.U: None,
            }

    def __str__(self) -> str:
        """
        """
        n = "    ".join(f"{d}: {v}," for d, v in self.neighbors.items())
        return f"""LocationInfo(
    type={self.type},
    neighbors={
      {n}
                })"""

    def __repr__(self) -> str:
        return str(self)



class Instruction(NamedTuple):
    step: int
    turn: str



Instructions = List[Instruction]
Carte = Dict[Position, LocationInfo]



def parser(data: str="data") -> Tuple[Carte, Position, Instructions]:
    """
    """
    instruction_re = re.compile(r"(\d+)([RUDL]?)")
    G: Dict[Position, LocationInfo]={}
    start: Position=None
    with open(data, mode="r", encoding="UTF8") as fin:
        for y, line in enumerate(fin, start=1):
            line = line.strip("\n")
            if line == "":
                break
            for x, v in enumerate(line, start=1):
                if v == " ":
                    continue
                if start is None and v == ".":
                    start = Position(x, y)
                G[Position(x, y)] = LocationInfo(type=v)

        instructions = [
                Instruction(int(steps), direction)
                for steps, direction in instruction_re.findall(next(fin))
                ]

    return G, start, instructions



def wrap1(G: Carte) -> Carte:
    """
    """
    maxy = max(map(attrgetter("y"), G.keys()))
    for i in range(1, maxy):
        candidates = sorted(
                filter(lambda p: p.y == i, G.keys()),
                key=attrgetter("x"),
                )
        for a, b in pairwise(candidates + [candidates[0]]):
            if G[a].type != "#" and G[b].type != "#":
                G[a].neighbors[Direction.R] = (b, Direction.R)
                G[b].neighbors[Direction.L] = (a, Direction.L)

    maxx = max(map(attrgetter("x"), G.keys()))
    for i in range(1, maxx):
        candidates = sorted(
                filter(lambda p: p.x == i, G.keys()),
                key=attrgetter("y"),
                )
        for a, b in pairwise(candidates + [candidates[0]]):
            if G[a].type != "#" and G[b].type != "#":
                G[a].neighbors[Direction.D] = (b, Direction.D)
                G[b].neighbors[Direction.U] = (a, Direction.U)

    return G



def solve(carte: Carte, position: Position, instructions: Instructions) -> int:
    """
    """
    direction = Direction.R
    for instruction in instructions:
        for _ in range(instruction.step):
            neighbor = carte[position].neighbors[direction]
            if neighbor is None:
                break
            else:
                position, direction = neighbor
        if instruction.turn != '':
            direction = TURNS[direction][instruction.turn]

    print(position, direction)
    return 1000*position.y + 4*position.x + direction.value



def part1(data: str="data") -> int:
    """
    What is the final password?
    """
    carte, position, instructions = parser(data)
    carte = wrap1(carte)
    if False:
        print(*carte.items(), sep="\n")
        print(*instructions, sep="\n")
        print(position)

    return solve(carte, position, instructions)



def wrap_test(carte: Carte) -> Carte:
    """
    """
    width = max(map(attrgetter("x"), carte.keys())) // 4
    for i in range(width):
        # A
        a = Position(width+1+i, width+1)
        b = Position(2*width+1, i+1)
        if carte[a].type == ".":
            carte[a].neighbors[Direction.U] = (b, Direction.R) if carte[b].type == "." else None
        if carte[b].type == ".":
            carte[b].neighbors[Direction.L] = (a, Direction.D) if carte[a].type == "." else None

        # B
        a = Position(i+1, width+1)
        b = Position(3*width-i, 1)
        if carte[a].type == ".":
            carte[a].neighbors[Direction.U] = (b, Direction.D) if carte[b].type == "." else None
        if carte[b].type == ".":
            carte[b].neighbors[Direction.U] = (a, Direction.D) if carte[a].type == "." else None

        # C
        a = Position(3*width+1+i, 2*width+1)
        b = Position(3*width, 2*width-i)
        if carte[a].type == ".":
            carte[a].neighbors[Direction.U] = (b, Direction.L) if carte[b].type == "." else None
        if carte[b].type == ".":
            carte[b].neighbors[Direction.R] = (a, Direction.D) if carte[a].type == "." else None

        # D
        a = Position(3*width, width-i)
        b = Position(4*width, 2*width+1+i)
        if carte[a].type == ".":
            carte[a].neighbors[Direction.R] = (b, Direction.L) if carte[b].type == "." else None
        if carte[b].type == ".":
            carte[b].neighbors[Direction.L] = (a, Direction.R) if carte[a].type == "." else None

        # E
        a = Position(2*width-i, 2*width)
        b = Position(2*width+1, 2*width+1+i)
        if carte[a].type == ".":
            carte[a].neighbors[Direction.D] = (b, Direction.R) if carte[b].type == "." else None
        if carte[b].type == ".":
            carte[b].neighbors[Direction.L] = (a, Direction.U) if carte[a].type == "." else None

        # F
        a = Position(1*width-i, 2*width)
        b = Position(2*width+1+i, 3*width)
        if carte[a].type == ".":
            carte[a].neighbors[Direction.U] = (b, Direction.D) if carte[b].type == "." else None
        if carte[b].type == ".":
            carte[b].neighbors[Direction.D] = (a, Direction.U) if carte[a].type == "." else None

        # G
        a = Position(1, 2*width-i)
        b = Position(3*width+1+i, 3*width)
        if carte[a].type == ".":
            carte[a].neighbors[Direction.L] = (b, Direction.U) if carte[b].type == "." else None
        if carte[b].type == ".":
            carte[b].neighbors[Direction.D] = (a, Direction.R) if carte[a].type == "." else None

    return carte



def wrap_data(carte: Carte) -> Carte:
    """
    """
    width = max(map(attrgetter("x"), carte.keys())) // 3
    assert width == 50
    for i in range(width):
        # A
        a = Position(2*width-i, 3*width)
        b = Position(1*width, 4*width-i)
        if carte[a].type == ".":
            carte[a].neighbors[Direction.D] = (b, Direction.L) if carte[b].type == "." else None
        if carte[b].type == ".":
            carte[b].neighbors[Direction.R] = (a, Direction.U) if carte[a].type == "." else None

        # B
        a = Position(0*width+1+i, 2*width+1)
        b = Position(1*width+1, 1*width+1+i)
        if carte[a].type == ".":
            carte[a].neighbors[Direction.U] = (b, Direction.R) if carte[b].type == "." else None
        if carte[b].type == ".":
            carte[b].neighbors[Direction.L] = (a, Direction.D) if carte[a].type == "." else None

        # C
        a = Position(0*width+1, 3*width-i)
        b = Position(1*width+1, 0*width+1+i)
        if carte[a].type == ".":
            carte[a].neighbors[Direction.L] = (b, Direction.R) if carte[b].type == "." else None
        if carte[b].type == ".":
            carte[b].neighbors[Direction.L] = (a, Direction.R) if carte[a].type == "." else None

        # D
        a = Position(0*width+1, 4*width-i)
        b = Position(2*width-i, 0*width+1)
        if carte[a].type == ".":
            carte[a].neighbors[Direction.L] = (b, Direction.D) if carte[b].type == "." else None
        if carte[b].type == ".":
            carte[b].neighbors[Direction.U] = (a, Direction.R) if carte[a].type == "." else None

        # E
        a = Position(1*width-i, 4*width)
        b = Position(3*width-i, 0*width+1)
        if carte[a].type == ".":
            carte[a].neighbors[Direction.D] = (b, Direction.D) if carte[b].type == "." else None
        if carte[b].type == ".":
            carte[b].neighbors[Direction.U] = (a, Direction.U) if carte[a].type == "." else None

        # F
        a = Position(2*width, 2*width+1+i)
        b = Position(3*width, 1*width-i)
        if carte[a].type == ".":
            carte[a].neighbors[Direction.R] = (b, Direction.L) if carte[b].type == "." else None
        if carte[b].type == ".":
            carte[b].neighbors[Direction.R] = (a, Direction.L) if carte[a].type == "." else None

        # G
        a = Position(2*width, 1*width+1+i)
        b = Position(2*width+1+i, 1*width)
        if carte[a].type == ".":
            carte[a].neighbors[Direction.R] = (b, Direction.U) if carte[b].type == "." else None
        if carte[b].type == ".":
            carte[b].neighbors[Direction.D] = (a, Direction.L) if carte[a].type == "." else None

    return carte



def part2(data: str="data") -> int:
    """
    Fold the map into a cube, then follow the path given in the monkeys' notes. What is the final password?
    """
    carte, position, instructions = parser(data)
    carte = wrap1(carte)
    if data == "test":
        carte = wrap_test(carte)
    else:
        carte = wrap_data(carte)
    if True:
        print(*carte.items(), sep="\n")
        print(*instructions, sep="\n")
        print("start position:", position)

    return solve(carte, position, instructions)





if __name__ == "__main__":
    assert (answer := part1("test")) == 6032, answer
    answer = part1()
    print(f"Part1 answer: {answer}")
    assert answer == 126350

    print()

    assert (answer := part2("test")) == 5031, answer
    answer = part2()
    print(f"Part2 answer: {answer}")
    assert answer == 205615  # too high
    # 64384  to low
    # Wrong 119103
