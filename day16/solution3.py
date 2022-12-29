#!/usr/bin/env  python3

from collections import defaultdict
from dataclasses import dataclass
from itertools import (
        combinations,
        product,
        )
from operator import (
        attrgetter,
        itemgetter,
        )
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



START = "AA"
valve_re = re.compile(r"^Valve (?P<valve>..) has flow rate=(?P<flow>\d+); tunnels? leads? to valves? (?P<lead>.*)$")



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
                G.add_edge(valve, destination, time=1)
            G.nodes[valve]["flow"] = flow

    if False:
        s = list(nx.single_source_shortest_path(G, START))
        print(data)
        print(len(s))
        print(*s, sep="\n")

    # Remove node that can't contribute to the flow.
    nodes_with_flow = list(filter(lambda n: n[1]["flow"] > 0 or n[0]=="AA", G.nodes(data=True)))

    # Create a fully connected graph of nodes with flow.
    # This is analoguous to going from A -> B -> C but without opening the valve at B.
    G2 = nx.Graph()
    for (u, ud), (v, vd) in combinations(nodes_with_flow, 2):
        G2.add_node(u, **ud)
        G2.add_node(v, **vd)
        # -1 because the path includes the first AND last node but we care
        # about the number of edges, not the number of nodes.
        # +1 because we add the time it takes to open the valve.  If we go to
        # node X, it is because we want to open valve X.
        G2.add_edge(u, v, time=len(nx.shortest_path(G, u, v))-1+1)

    return G2



class State(NamedTuple):
    """
    """
    # Order of attributes matters to properly order the heapq.
    valve: str
    score: int
    future_score: int
    remaining_minutes: int
    remaining_valves: Set[str]=frozenset()

    @property
    def expected_score(self) -> int:
        """
        """
        return self.score + self.future_score

    def __lt__(self, other):
        """
        """
        return self.expected_score > other.expected_score



def compute_future_score(
        G: nx.Graph,
        valve: str,
        remaining_valves: Iterable[str],
        remaining_minutes: int,
        ):
    """
    The future score is optimisitic.
    What if we could simultaneously open all remaining valves for the rest of the remaining minutes?
    """
    future_score = 0
    for next_valve in remaining_valves:
        if valve == next_valve:
            travel_time = 0
        else:
            travel_time = G[valve][next_valve]["time"]
        future_score += G.nodes[next_valve]["flow"] * max(0, remaining_minutes-travel_time)

    return future_score



def part1(data: str="data") -> int:
    """
    What is the most pressure you can release?
    """
    MINUTES = 30
    G = parser(data)
    if False:
        print(*G.nodes(data=True), sep="\n")
        print(*G.edges(data=True), sep="\n")
        import matplotlib.pyplot as plt
        pos = nx.circular_layout(G)
        nx.draw(G, pos, with_labels=True)
        #node_labels = nx.get_node_attributes(G, "time")
        #nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=10)
        edge_labels = nx.get_edge_attributes(G, "time")
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        plt.savefig("cave.png")

    best = defaultdict(lambda: 0)
    remaining_valves = frozenset(G.nodes - {START})
    states = [State(
        valve=START,
        score=0,
        future_score=compute_future_score(G, START, remaining_valves, MINUTES),
        remaining_minutes=MINUTES,
        remaining_valves=remaining_valves,
        )]

    while len(states) > 0:
        current = heapq.heappop(states)

        if current.remaining_minutes <= 0 or len(current.remaining_valves) == 0:
            #print(current)
            #print(len(states))
            #print(*sorted(states, key=attrgetter("score"), reverse=True), sep="\n")
            return current.score

        for next_valve in current.remaining_valves:
            assert current.valve != next_valve, current.valve

            # Moving to the next valve and open it.
            flow = G.nodes[next_valve]["flow"]
            remaining_valves = frozenset(current.remaining_valves - {next_valve})
            travel_time = G[current.valve][next_valve]["time"]
            if current.remaining_minutes > travel_time:
                remaining_minutes = current.remaining_minutes - travel_time
                future_score = compute_future_score(G, next_valve, remaining_valves, remaining_minutes)
            else:
                future_score = 0
                remaining_minutes = 0

            possible_valve = State(
                        valve=next_valve,
                        score=current.score + remaining_minutes*flow,
                        future_score=future_score,
                        remaining_minutes=remaining_minutes,
                        remaining_valves=remaining_valves,
                        )
            if possible_valve.score > best[possible_valve.remaining_valves]:
                best[possible_valve.remaining_valves] = possible_valve.score
                heapq.heappush(states, possible_valve)


    print(current)
    print(len(states))
    print(*sorted(states, key=lambda s: s.score, reverse=True), sep="\n")
    return None



def part2(data: str="data") -> int:
    """
    With you and an elephant working together for 26 minutes, what is the most
    pressure you could release?
    """
    class State(NamedTuple):
        """
        """
        # Order of attributes matters to properly order the heapq.
        valve: str
        score: int
        remaining_minutes: int
        opened_valves: Set[str]=frozenset()

    MINUTES = 26
    G = parser(data)

    best = defaultdict(lambda: 0)
    states = [State(
        valve=START,
        score=0,
        remaining_minutes=MINUTES,
        opened_valves=frozenset(),
        )]

    while len(states) > 0:
        current = heapq.heappop(states)

        if current.remaining_minutes <= 0 or current.opened_valves == set(G.nodes):
            continue

        for next_valve in set(G.nodes) - {START} - current.opened_valves:
            assert current.valve != next_valve, current.valve

            # Moving to the next valve and open it.
            flow = G.nodes[next_valve]["flow"]
            travel_time = G[current.valve][next_valve]["time"]
            if current.remaining_minutes > travel_time:
                remaining_minutes = current.remaining_minutes - travel_time
            else:
                remaining_minutes = 0

            possible_valve = State(
                        valve=next_valve,
                        score=current.score + remaining_minutes*flow,
                        remaining_minutes=remaining_minutes,
                        opened_valves=frozenset(current.opened_valves | {next_valve}),
                        )
            if possible_valve.score > best[possible_valve.opened_valves]:
                best[possible_valve.opened_valves] = possible_valve.score
                heapq.heappush(states, possible_valve)


    if False:
        print(*((sorted(a), b) for a, b in best.items()), sep="\n")
        print(len(best))
    answer = max(
            me_score + elephant_score
            for me, me_score in best.items()
            for elephant, elephant_score in best.items()
            if not (me & elephant)
            )
    return answer





if __name__ == "__main__":
    assert (answer := part1("test")) == 1651, answer
    answer = part1()
    print(f"Part1 answer: {answer}")
    assert answer == 2124

    print()

    #assert (answer := part2("test")) == 1707, answer
    answer = part2()
    print(f"Part2 answer: {answer}")
    assert answer == 2775
