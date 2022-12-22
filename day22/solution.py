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
        self.neighbors: Dict[Direction, Position] = {
            Direction.R: None,
            Direction.D: None,
            Direction.L: None,
            Direction.U: None,
            }

    def __str__(self) -> str:
        """
        """
        return f"LocationInfo(type={self.type}, neighbors={self.neighbors}"

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

    maxy = max(map(attrgetter("y"), G.keys()))
    for i in range(1, maxy):
        candidates = sorted(
                filter(lambda p: p.y == i, G.keys()),
                key=attrgetter("x"),
                )
        for a, b in pairwise(candidates + [candidates[0]]):
            if G[a].type != "#" and G[b].type != "#":
                G[a].neighbors[Direction.R] = b
                G[b].neighbors[Direction.L] = a

    maxx = max(map(attrgetter("x"), G.keys()))
    for i in range(1, maxx):
        candidates = sorted(
                filter(lambda p: p.x == i, G.keys()),
                key=attrgetter("y"),
                )
        for a, b in pairwise(candidates + [candidates[0]]):
            if G[a].type != "#" and G[b].type != "#":
                G[a].neighbors[Direction.D] = b
                G[b].neighbors[Direction.U] = a

    return G, start, instructions



def part1(data: str="data") -> int:
    """
    What is the final password?
    """
    carte, position, instructions = parser(data)
    if False:
        print(*carte.items(), sep="\n")
        print(instructions)
        print(position)

    direction = Direction.R
    for instruction in instructions:
        for _ in range(instruction.step):
            neighbor = carte[position].neighbors[direction]
            if neighbor is None:
                break
            else:
                position = neighbor
        if instruction.turn != '':
            direction = TURNS[direction][instruction.turn]

        delme = 4

    print(position, direction)
    return 1000*position.y + 4*position.x + direction.value



def part2(data: str="data") -> int:
    """
    """
    return 0





if __name__ == "__main__":
    assert (answer := part1("test")) == 6032, answer
    answer = part1()
    print(f"Part1 answer: {answer}")
    assert answer == 126350

    assert (answer := part2("test")) == 6032, answer
    answer = part2()
    print(f"Part2 answer: {answer}")
    assert answer == 205615
