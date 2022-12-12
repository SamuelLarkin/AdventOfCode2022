#!/usr/bin/env  python3

from typing import (
        Any,
        Callable,
        Generator,
        List,
        NamedTuple,
        Sequence,
        Tuple,
        )

import networkx as nx


class Direction(NamedTuple):
    x: int
    y: int



DIRECTIONS = (
        Direction(0, 1),
        Direction(0, -1),
        Direction(1, 0),
        Direction(-1, 0),
        )



def get_elevation_value(e: str) -> int:
    """
    """
    if e == "S":
        return get_elevation_value("a")
    elif e == "E":
        return get_elevation_value("z")

    return ord(e) - ord("a")



def parser(data: str="data") -> Tuple[Any, Tuple[int, int], Tuple[int, int]]:
    """
    """
    start = None
    end = None
    G = nx.DiGraph()
    # Create the nodes with attributes.
    with open(data, mode="r", encoding="UTF8") as fin:
        height = 0
        width  = None
        for p_y, yv in enumerate(map(str.strip, fin)):
            height += 1
            if width is None:
                width = len(yv)
            assert len(yv) == width

            for p_x, elevation_id in enumerate(yv):
                if elevation_id == "S":
                    # Found the start position
                    start = (p_x, p_y)
                    G.add_node(
                            (p_x, p_y),
                            elevation_value=get_elevation_value(elevation_id),   #0
                            elevation_id=elevation_id,
                            start=True,
                            )
                    continue

                if elevation_id == "E":
                    # Found the end position
                    end = (p_x, p_y)
                    G.add_node(
                            (p_x, p_y),
                            elevation_value=get_elevation_value(elevation_id),   # 25
                            elevation_id=elevation_id,
                            end=True,
                            )
                    continue

                G.add_node(
                        (p_x, p_y),
                        elevation_value=get_elevation_value(elevation_id),
                        elevation_id=elevation_id
                        )

    # Create the edges
    for p, p_a in G.nodes(data=True):
        p_e = p_a["elevation_value"]
        # Visit the potential neighbors.
        for neighbor in map(lambda d: (p[0]+d.x, p[1]+d.y), DIRECTIONS):
            if G.has_node(neighbor):
                n_e = G.nodes[neighbor]["elevation_value"]
                if n_e <= p_e+1:
                    G.add_edge(p, neighbor, elevations=(p_e, n_e))

    return G, start, end



def part1() -> int:
    """
    What is the fewest steps required to move from your current position to the
    location that should get the best signal?
    """
    G, start, end = parser()
    path = nx.shortest_path(G, source=start, target=end)

    return len(path) - 1



def part2() -> int:
    """
    What is the fewest steps required to move starting from any square with
    elevation a to the location that should get the best signal?
    """
    G, _, end = parser()
    #print(*G.nodes(data=True), sep="\n")
    starts = [node for node, attributes in G.nodes(data=True) if attributes["elevation_id"] == "a"]
    paths = []
    for start in starts:
        try:
            path = nx.shortest_path(G, source=start, target=end)
            paths.append(path)
        except:
            pass

    return sorted(map(len, paths))[0] - 1





if __name__ == "__main__":
    answer = part1()
    print(f"Part1 answer: {answer}")
    assert answer == 350

    answer = part2()
    print(f"Part2 answer: {answer}")
    assert answer == 349
