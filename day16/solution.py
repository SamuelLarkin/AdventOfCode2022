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
            G.nodes[valve]["name"] = valve
            G.nodes[valve]["flow"] = flow

    if False:
        s = list(nx.single_source_shortest_path(G, START))
        print(data)
        print(len(s))
        print(*s, sep="\n")

    # Remove node that can't contribute to the flow.
    nodes_with_flow = list(filter(lambda n: n[1]["flow"] > 0 or n[0]=="AA", G.nodes(data=True)))
    rename = {k: 1<<v for v, k in enumerate(sorted(map(itemgetter(0), nodes_with_flow))) }

    # Create a fully connected graph of nodes with flow.
    # This is analoguous to going from A -> B -> C but without opening the valve at B.
    G2 = nx.Graph()
    for (u, ud), (v, vd) in combinations(nodes_with_flow, 2):
        # -1 because the path includes the first AND last node but we care
        # about the number of edges, not the number of nodes.
        # +1 because we add the time it takes to open the valve.  If we go to
        # node X, it is because we want to open valve X.
        travel_time = len(nx.shortest_path(G, u, v))-1+1
        u = rename[u]
        v = rename[v]
        G2.add_node(u, **ud)
        G2.add_node(v, **vd)
        G2.add_edge(u, v, time=travel_time)

    return G2, rename[START]



class State(NamedTuple):
    """
    """
    # Order of attributes matters to properly order the heapq.
    valve: str
    remaining_minutes: int
    score: int=0
    future_score: int=0
    opened_valves: int=0

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
        remaining_valves: int,
        remaining_minutes: int,
        ):
    """
    The future score is optimisitic.
    What if we could simultaneously open all remaining valves for the rest of the remaining minutes?
    """
    future_score = 0
    for next_valve in G.nodes:
        if next_valve & remaining_valves:
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
    G, start = parser(data)
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

    all_valves = sum(G.nodes)
    best = defaultdict(lambda: 0)
    states = [State(
        valve=start,
        score=0,
        future_score=compute_future_score(G, start, all_valves-start, MINUTES),
        remaining_minutes=MINUTES,
        opened_valves=start,
        )]

    while len(states) > 0:
        current = heapq.heappop(states)

        if current.remaining_minutes <= 0 or current.opened_valves == all_valves:
            #print(current)
            #print(len(states))
            #print(*sorted(states, key=attrgetter("score"), reverse=True), sep="\n")
            return current.score

        for next_valve in G.nodes:
            if next_valve & current.opened_valves:
                continue
            assert current.valve != next_valve, current.valve

            # Moving to the next valve and open it.
            flow = G.nodes[next_valve]["flow"]
            travel_time = G[current.valve][next_valve]["time"]
            if current.remaining_minutes > travel_time:
                remaining_minutes = current.remaining_minutes - travel_time
                future_score = compute_future_score(G, next_valve, all_valves-next_valve, remaining_minutes)
            else:
                future_score = 0
                remaining_minutes = 0

            possible_valve = State(
                        valve=next_valve,
                        score=current.score + remaining_minutes*flow,
                        future_score=future_score,
                        remaining_minutes=remaining_minutes,
                        opened_valves=current.opened_valves+next_valve,
                        )
            if possible_valve.score > best[possible_valve.opened_valves]:
                best[possible_valve.opened_valves] = possible_valve.score
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
        remaining_minutes: int
        score: int=0
        opened_valves: int=0

    MINUTES = 26
    G, start = parser(data)

    all_valves = sum(G.nodes)
    best = defaultdict(lambda: 0)
    states = [State(
        valve=start,
        score=0,
        remaining_minutes=MINUTES,
        opened_valves=start,
        )]

    while len(states) > 0:
        current = heapq.heappop(states)

        if current.remaining_minutes <= 0 or current.opened_valves == all_valves:
            continue

        for next_valve in G.nodes:
            if next_valve & current.opened_valves:
                continue
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
                        opened_valves=current.opened_valves + next_valve,
                        )
            assert possible_valve.opened_valves <= all_valves
            if possible_valve.score > best[possible_valve.opened_valves]:
                best[possible_valve.opened_valves] = possible_valve.score
                heapq.heappush(states, possible_valve)


    if False:
        #print(*((sorted(a), b) for a, b in best.items()), sep="\n")
        print(*sorted(best.items(), key=itemgetter(0)), sep="\n")
        print(len(best))
    answer = max(
            me_score + elephant_score
            for me, me_score in best.items()
            for elephant, elephant_score in best.items()
            if not ((me-start) & (elephant-start))
            )
    return answer





if __name__ == "__main__":
    assert (answer := part1("test")) == 1651, answer
    answer = part1()
    print(f"Part1 answer: {answer}")
    assert answer == 2124, answer

    print()

    #assert (answer := part2("test")) == 1707, answer
    answer = part2()
    print(f"Part2 answer: {answer}")
    assert answer == 2775, answer
