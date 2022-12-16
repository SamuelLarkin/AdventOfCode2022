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



MINUTES = 30
START = "AA"
valve_re = re.compile(r"Valve (?P<valve>..) has flow rate=(?P<flow>\d+); tunnels? leads? to valves? (?P<lead>.*)")



class State(NamedTuple):
    """
    """
    # Order of attributes matters to properly order the heapq.
    remaining_minutes: int
    score: int
    future_score: int
    pressure: int
    name: str
    open_valves: Set[str]=frozenset()

    @property
    def expected_score(self) -> int:
        """
        """
        return self.score + self.remaining_minutes*self.pressure + self.future_score

    def __lt__(self, other):
        """
        """
        return self.expected_score > other.expected_score



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
        remaining_minutes: int,
        ) -> int:
    """
    """
    remaining_valves = {k: v for k, v in ordered_valves.items() if k not in visited_valves}
    flow_minutes = zip(remaining_valves.values(), range(remaining_minutes, 0, -2))
    future_score = sum(flow*minutes for flow, minutes in flow_minutes)

    return future_score



def part1() -> int:
    """
    What is the most pressure you can release?
    """
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
        future_score=expected_future_score({START}, ordered_valves, MINUTES-0),
        pressure=0,
        open_valves=frozenset({START}),
        remaining_minutes=MINUTES,
        )]
    while len(visited) > 0:
        heapq.heapify(visited)
        current = heapq.heappop(visited)
        best = min(best, current.score)

        if current.remaining_minutes <= 0:
            print(len(visited))
            print(*sorted(visited, key=lambda s: s.score, reverse=True), sep="\n")
            return current.score

        if current.name not in current.open_valves:
            # Opening a valve.
            remaining_minutes = current.remaining_minutes - 1
            flow = G.nodes[current.name]["flow"]
            pressure = current.pressure + flow
            open_valves = frozenset(current.open_valves | {current.name})

            # TODO if all valve are open, compute final score
            if len(open_valves) == len(ordered_valves):
                current = State(
                        name=current.name,
                        score=current.score + pressure*(remaining_minutes+1),
                        future_score=0,
                        pressure=pressure,
                        open_valves=open_valves,
                        remaining_minutes=0,
                        )
                visited.append(current)
                continue
            else:
                current = State(
                        name=current.name,
                        score=current.score+pressure,
                        future_score=expected_future_score(open_valves, ordered_valves, remaining_minutes),
                        pressure=pressure,
                        open_valves=open_valves,
                        remaining_minutes=remaining_minutes,
                        )

            if current.expected_score > best:
                visited.append(current)

        if best > current.expected_score:
            """
            From this current state, even if we are optimistic, it is NOT
            possible to beat the best state so far.
            """
            continue

        for neighbor in nx.neighbors(G, current.name):
            # Moving to a neighbor.
            remaining_minutes = current.remaining_minutes - 1
            possible_valve = State(
                        name=neighbor,
                        remaining_minutes=remaining_minutes,
                        score=current.score+current.pressure,
                        # Note that the future score should be less because a minute pass.
                        future_score=expected_future_score(current.open_valves, ordered_valves, remaining_minutes),
                        pressure=current.pressure,
                        open_valves=current.open_valves,
                        )
            if current.expected_score > best:
                visited.append(possible_valve)

        if True:
            """
            It is critical not to add states that are already in the visited list.
            """
            visited = [state for state in set(visited) if state.expected_score > best]

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
