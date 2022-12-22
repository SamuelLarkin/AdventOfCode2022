#!/usr/bin/env  python3

from more_itertools import pairwise
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

import networkx as nx
import re



class Position(NamedTuple):
    x: int
    y: int

    def __add__(self, other) -> "Position":
        return Position(self.x+other.x, self.y+other.y)



R = Position(1, 0)
D = Position(0, 1)
L = Position(-1 ,0)
U = Position(0, -1)
TURNS = {
        R: {"R": D, "L": U},
        D: {"R": L, "L": R},
        L: {"R": U, "L": D},
        U: {"R": R, "L": L},
        }
DIRECTION_SCORE = {
        R: 0,
        D: 1,
        L: 2,
        U: 3,
        }



class Instruction(NamedTuple):
    step: int
    turn: str



Instructions = List[Instruction]




def parser(data: str="data") -> Tuple[nx.Graph, Position, Instructions]:
    """
    """
    instruction_re = re.compile(r"(\d+)([RUDL]?)")
    G = nx.Graph()
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
                G.add_node(Position(x, y), type=v)

        instructions = [
                Instruction(int(steps), direction)
                for steps, direction in instruction_re.findall(next(fin))
                ]

    def symlink(candidates) -> None:
        """
        """
        for a, b in pairwise(candidates + [candidates[0]]):
            if a[1]["type"] != "#" and b[1]["type"] != "#":
                G.add_edge(a[0], b[0])

    for i in range(1, y):
        candidates = sorted(
                filter(lambda n: n[0].y == i, G.nodes(data=True)),
                key=lambda n: n[0].x,
                )
        symlink(candidates)

    for i in range(1, x):
        candidates = sorted(
                filter(lambda n: n[0].x == i, G.nodes(data=True)),
                key=lambda n: n[0].y,
                )
        symlink(candidates)

    return G, start, instructions



def part1(data: str="data") -> int:
    """
    What is the final password?
    """
    carte, position, instructions = parser(data)
    print(*carte.nodes(data=True), sep="\n")
    print(*carte.edges, sep="\n")
    print(instructions)
    print(position)
    direction = Position(1, 0)
    for instruction in instructions:
        for _ in range(instruction.step):
            neighbor = position + direction
            if neighbor not in carte[position]:
                break
            else:
                position = neighbor
        if instruction.turn != '':
            direction = TURNS[direction][instruction.turn]

        delme = 4

    return 1000*position.x + 4*position.y + DIRECTION_SCORE[direction]



def part2(data: str="data") -> int:
    """
    """
    return 0





if __name__ == "__main__":
    assert (answer := part1("test")) == 6032, answer
    answer = part1()
    print(f"Part1 answer: {answer}")
    assert answer == 69289

    answer = part2()
    print(f"Part2 answer: {answer}")
    assert answer == 205615
