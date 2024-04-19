#!/usr/bin/env  python3

from enum import Enum
from more_itertools import pairwise
from operator import attrgetter
from typing import (
        List,
        NamedTuple,
        Tuple,
        )

import networkx as nx
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



class Instruction(NamedTuple):
    step: int
    turn: str



Carte = nx.Graph
Instructions = List[Instruction]




def parser(data: str="data") -> Tuple[Carte, Position, Instructions]:
    """
    """
    instruction_re = re.compile(r"(\d+)([RUDL]?)")
    G = nx.DiGraph()
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

    maxy = max(map(attrgetter("y"), G))
    for i in range(1, maxy):
        candidates = sorted(
                filter(lambda n: n[0].y == i, G.nodes(data=True)),
                key=lambda n: n[0].x,
                )
        for a, b in pairwise(candidates + [candidates[0]]):
            if a[1]["type"] != "#" and b[1]["type"] != "#":
                G.add_edge(a[0], b[0], direction=Direction.R, new_direction=Direction.R)
                G.add_edge(b[0], a[0], direction=Direction.L, new_direction=Direction.L)

    maxx = max(map(attrgetter("x"), G))
    for i in range(1, maxx):
        candidates = sorted(
                filter(lambda n: n[0].x == i, G.nodes(data=True)),
                key=lambda n: n[0].y,
                )
        for a, b in pairwise(candidates + [candidates[0]]):
            if a[1]["type"] != "#" and b[1]["type"] != "#":
                G.add_edge(a[0], b[0], direction=Direction.D, new_direction=Direction.D)
                G.add_edge(b[0], a[0], direction=Direction.U, new_direction=Direction.U)

    return G, start, instructions



def solve(carte: Carte, position: Position, instructions: Instructions) -> int:
    """
    """
    direction = Direction.R
    for instruction in instructions:
        for _ in range(instruction.step):
            neighbor = carte[position]
            neighbor = {
                    v["direction"]: {
                        "p": k,
                        "nd": v["new_direction"],
                        }
                    for k, v in neighbor.items()
                    }
            candidate = neighbor.get(direction, None)
            if candidate is None:
                break
            else:
                position = candidate["p"]
                direction = candidate["nd"]
        if instruction.turn != '':
            direction = TURNS[direction][instruction.turn]

    print(position, direction)
    return 1000*position.y + 4*position.x + direction.value



def part1(data: str="data") -> int:
    """
    What is the final password?
    """
    carte, start, instructions = parser(data)

    return solve(carte, start, instructions)



def wrap(carte: Carte) -> Carte:
    """
    """
    width = max(map(attrgetter("x"), carte)) // 4
    for i in range(width):
        # A
        a = Position(width+1+i, width+1)
        b = Position(2*width+1, i+1)
        if carte.nodes[a]["type"] != "#" and carte.nodes[b]["type"] != "#":
            carte.remove_edge(a, b)
            carte.remove_edge(b, a)
            carte.add_edge(a, b, direction=Direction.U, new_direction=Direction.R)
            carte.add_edge(b, a, direction=Direction.L, new_direction=Direction.D)

        # B
        a = Position(i+1, width+1)
        b = Position(3*width-i, 1)
        if carte.nodes[a]["type"] != "#" and carte.nodes[b]["type"] != "#":
            carte.remove_edge(a, b)
            carte.remove_edge(b, a)
            carte.add_edge(a, b, direction=Direction.U, new_direction=Direction.D)
            carte.add_edge(b, a, direction=Direction.U, new_direction=Direction.D)

        # C
        a = Position(3*width+1+i, 2*width+1)
        b = Position(3*width, 2*width-i)
        if carte.nodes[a]["type"] != "#" and carte.nodes[b]["type"] != "#":
            carte.remove_edge(a, b)
            carte.remove_edge(b, a)
            carte.add_edge(a, b, direction=Direction.U, new_direction=Direction.L)
            carte.add_edge(b, a, direction=Direction.R, new_direction=Direction.D)

        # D
        a = Position(3*width, width-i)
        b = Position(4*width, 2*width+1+i)
        if carte.nodes[a]["type"] != "#" and carte.nodes[b]["type"] != "#":
            carte.remove_edge(a, b)
            carte.remove_edge(b, a)
            carte.add_edge(a, b, direction=Direction.R, new_direction=Direction.L)
            carte.add_edge(b, a, direction=Direction.L, new_direction=Direction.R)

        # E
        a = Position(2*width-i, 2*width)
        b = Position(2*width+1, 2*width+1+i)
        if carte.nodes[a]["type"] != "#" and carte.nodes[b]["type"] != "#":
            carte.remove_edge(a, b)
            carte.remove_edge(b, a)
            carte.add_edge(a, b, direction=Direction.D, new_direction=Direction.R)
            carte.add_edge(b, a, direction=Direction.L, new_direction=Direction.U)

        # F
        a = Position(1*width-i, 2*width)
        b = Position(2*width+1+i, 3*width)
        if carte.nodes[a]["type"] != "#" and carte.nodes[b]["type"] != "#":
            carte.remove_edge(a, b)
            carte.remove_edge(b, a)
            carte.add_edge(a, b, direction=Direction.U, new_direction=Direction.D)
            carte.add_edge(b, a, direction=Direction.D, new_direction=Direction.U)

        # G
        a = Position(1, 2*width-i)
        b = Position(3*width+1+i, 3*width)
        if carte.nodes[a]["type"] != "#" and carte.nodes[b]["type"] != "#":
            carte.remove_edge(a, b)
            carte.remove_edge(b, a)
            carte.add_edge(a, b, direction=Direction.L, new_direction=Direction.U)
            carte.add_edge(b, a, direction=Direction.D, new_direction=Direction.R)

    return carte



def part2(data: str="data") -> int:
    """
    """
    carte, start, instructions = parser(data)
    carte = wrap(carte)
    print(*carte.edges(data=True), sep="\n")

    return solve(carte, start, instructions)





if __name__ == "__main__":
    assert (answer := part1("test")) == 6032, answer
    answer = part1()
    print(f"Part1 answer: {answer}")
    assert answer == 126350

    assert (answer := part2("test")) == 5031, answer
    answer = part2()
    print(f"Part2 answer: {answer}")
    assert answer == 205615
