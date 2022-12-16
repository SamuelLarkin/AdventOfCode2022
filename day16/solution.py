#!/usr/bin/env  python3

from dataclasses import dataclass
from operator import itemgetter
from typing import (
        Callable,
        Generator,
        Iterable,
        List,
        NamedTuple,
        Sequence,
        Set,
        Tuple,
        Union,
        )

import heapq
import networkx as nx
import re



valve_re = re.compile(r"Valve (?P<valve>..) has flow rate=(?P<flow>\d+); tunnels? leads? to valves? (?P<lead>.*)")



class State(NamedTuple):
    """
    """
    # Order of attributes matters to properly order the heapq.
    minutes: int
    score: int
    future_score: int
    name: str
    open_valves: Set[str]=frozenset()

    @property
    def expected_score(self) -> int:
        """
        """
        return self.score + self.future_score



def parser(data: str="data") -> nx.Graph:
    """
    """
    G = nx.Graph()
    # Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
    with open(data, mode="r", encoding="UTF8") as fin:
        for line in map(str.strip, fin):
            m = valve_re.match(line)
            assert m is not None, line
            valve = m.group("valve")
            flow = int(m.group("flow"))
            leads = map(str.strip, m.group("lead").split(","))
            for destination in leads:
                G.add_edge(valve, destination)
            G.nodes[valve]["name"] = valve
            G.nodes[valve]["flow"] = flow

    return G



def expected_future_score(
        visited_valves,
        ordered_valves,
        minutes: int,
        ) -> int:
    """
    """
    remaining_valves = {k: v for k, v in ordered_valves.items() if k not in visited_valves}
    flow_minutes = zip(remaining_valves.values(), range(minutes, 0, -2))
    future_score = sum(flow*minutes for flow, minutes in flow_minutes)

    return future_score



def part1() -> int:
    """
    """
    MINUTES = 30
    START = "AA"
    G = parser("test")
    print(*G.nodes(data=True), sep="\n")
    ordered_valves = {
            k: v
            for k, v in sorted(
                map(lambda t: (t[0], t[1]["flow"]), G.nodes(data=True)),
                key=itemgetter(1),
                reverse=True,
                )
            }
    print(ordered_valves)

    best = 0
    visited = [State(
        name=START,
        score=0,
        future_score=-expected_future_score({START}, ordered_valves, MINUTES-0),
        open_valves=frozenset({START}),
        minutes=0,
        )]
    while len(visited) > 0:
        current = heapq.heappop(visited)

        if current.minutes >= MINUTES:
            print(len(visited))
            print(*sorted(visited, key=lambda s: s.score, reverse=True), sep="\n")
            return -current.score

        if current.name not in current.open_valves:
            # Opening a valve.
            minutes = current.minutes + 1
            flow = G.nodes[current.name]["flow"]
            open_valves=frozenset(current.open_valves | {current.name})
            current = State(
                    name=current.name,
                    score=current.score - flow * (MINUTES - minutes),
                    future_score=-expected_future_score(open_valves, ordered_valves, MINUTES-minutes),
                    open_valves=open_valves,
                    minutes=minutes,
                    )
            assert current.score <= 0
            best = min(best, current.score)
            heapq.heappush(visited, current)

        if best < current.expected_score:
            """
            From this current state, even if we are optimistic, it is NOT
            possible to beat the best state so far.
            """
            continue

        for neighbor in nx.neighbors(G, current.name):
            # Moving to a neighbor.
            possible_valve = State(
                        name=neighbor,
                        score=current.score,
                        future_score=current.future_score,
                        open_valves=current.open_valves,
                        minutes=current.minutes+1,
                        )
            assert possible_valve.score <= 0
            heapq.heappush(visited, possible_valve)

        if True:
            """
            It is critical not to add states that are already in the visited list.
            """
            visited = list(set(visited))
            heapq.heapify(visited)

    return None



def part2() -> int:
    """
    """
    return None





if __name__ == "__main__":
    answer = part1()
    print(f"Part1 answer: {answer}")
    assert answer == 69289

    answer = part2()
    print(f"Part2 answer: {answer}")
    assert answer == 205615
