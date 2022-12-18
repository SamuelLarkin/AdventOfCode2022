#!/usr/bin/env  python3

from itertools import product
from operator import attrgetter
from tqdm import trange
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



DIRECTIONS = (
        (-1, 0, 0),
        (1, 0, 0),
        (0, -1 ,0),
        (0, 1, 0),
        (0, 0, -1),
        (0, 0, 1),
        )



class Position(NamedTuple):
    x: int
    y: int
    z: int

    def __add__(self, direction: Tuple[int, int, int]) -> "Position":
        """
        """
        return Position(
                self.x + direction[0],
                self.y + direction[1],
                self.z + direction[2],
                )



def parser(data: str="data") -> nx.Graph:
    """
    """
    G = nx.Graph()
    with open(data, mode="r", encoding="UTF8") as fin:
        for line in map(str.strip, fin):
            coordinates = Position(*(int(c) for c in line.split(",")))
            G.add_node(coordinates)

    for node in G:
        for potential_neighbor in map(lambda d: node+d, DIRECTIONS):
            if potential_neighbor in G:
                G.add_edge(node, potential_neighbor)


    return G



def part1() -> int:
    """
    What is the surface area of your scanned lava droplet?
    """
    lava = parser()

    return sum(6-len(list(lava.neighbors(n))) for n in lava)



def part2() -> int:
    """
    What is the exterior surface area of your scanned lava droplet?
    """
    lava = parser()

    # Find a bounding box.
    # Accommodate wiggle room
    minx = min(map(attrgetter("x"), lava))-2
    maxx = max(map(attrgetter("x"), lava))+2
    miny = min(map(attrgetter("y"), lava))-2
    maxy = max(map(attrgetter("y"), lava))+2
    minz = min(map(attrgetter("z"), lava))-2
    maxz = max(map(attrgetter("z"), lava))+2

    # Find the outside volume.
    p = Position(minx, miny, minz)
    outside = set()
    assert p not in lava, "Oups! Starting position is not outside the lava!"
    visited = {p}
    possible_candidates = [p]
    while len(possible_candidates) > 0:
        p = possible_candidates.pop()
        for candidate in map(lambda d: p+d, DIRECTIONS):
            if candidate in visited:
                continue
            visited.add(candidate)
            if minx <= candidate.x <= maxx \
                    and miny <= candidate.y <= maxy \
                    and minz <= candidate.z <= maxz:
                if candidate not in lava:
                    possible_candidates.append(candidate)
                    outside.add(candidate)

    # What surface of the lava touches the outside?
    surface = 0
    for l in lava:
        for c in map(lambda d: l+d, DIRECTIONS):
            surface += int(c in outside)

    return surface





if __name__ == "__main__":
    answer = part1()
    print(f"Part1 answer: {answer}")
    assert answer == 4332

    answer = part2()
    print(f"Part2 answer: {answer}")
    assert answer == 2524
