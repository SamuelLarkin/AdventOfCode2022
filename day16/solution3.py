#!/usr/bin/env  python3

from collections import defaultdict
from dataclasses import dataclass
from operator import (
        attrgetter,
        itemgetter,
        )
from itertools import (
        combinations,
        product,
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
            #G.nodes[valve]["name"] = valve
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
    name: str
    score: int
    future_score: int
    remaining_minutes: int
    remaining_valves: Set[str]=frozenset()
    elephant: str=""   # part 2

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
        name: str,
        remaining_valves: Iterable[str],
        remaining_minutes: int,
        ):
    """
    The future score is optimisitic.
    What if we could simultaneously open all remaining valves for the rest of the remaining minutes?
    """
    future_score = 0
    for next_valve in remaining_valves:
        if name == next_valve:
            travel_time = 0
        else:
            travel_time = G[name][next_valve]["time"]
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
        name=START,
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
            assert current.name != next_valve, current.name

            # Moving to the next valve and open it.
            flow = G.nodes[next_valve]["flow"]
            remaining_valves = frozenset(current.remaining_valves - {next_valve})
            travel_time = G[current.name][next_valve]["time"]
            if current.remaining_minutes > travel_time:
                remaining_minutes = current.remaining_minutes - travel_time
                future_score = compute_future_score(G, next_valve, remaining_valves, remaining_minutes)
            else:
                future_score = 0
                remaining_minutes = 0

            possible_valve = State(
                        name=next_valve,
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



def part2() -> int:
    """
    With you and an elephant working together for 26 minutes, what is the most
    pressure you could release?
    """
    MINUTES = 26
    G, _ = parser("test")
    #G, _ = parser()
    #print(*G.nodes(data=True), sep="\n")
    #print(*G.edges(data=True), sep="\n")
    ordered_valves = {
            k: v
            for k, v in sorted(
                map(lambda t: (t[0], t[1]["flow"]), G.nodes(data=True)),
                key=itemgetter(1),
                reverse=True,
                )
            }
    print(ordered_valves)

    valves_with_flow = frozenset(
            map(
                itemgetter(0),
                filter(lambda v: v[1]["flow"] > 0, G.nodes(data=True))))
    print(valves_with_flow)

    valves_without_flow = frozenset(
            map(
                itemgetter(0),
                filter(lambda v: v[1]["flow"] == 0, G.nodes(data=True))))
    print(valves_without_flow)

    def expected_future_score(
            visited_valves,
            ordered_valves,
            remaining_minutes: int,
            ) -> int:
        """
        The future score is optimisitic.
        What if we could simultaneously open all remaining valves for the rest of the remaining minutes?
        """
        remaining_valves = {k: v for k, v in ordered_valves.items() if k not in visited_valves}
        future_score = sum(remaining_valves.values()) * remaining_minutes

        return future_score

    def finalize(state: State) -> State:
        """
        """
        if len(valves_with_flow - state.open_valves) == 0:
            return State(
                    name=state.name,
                    elephant=state.elephant,
                    open_valves=state.open_valves,
                    pressure=state.pressure,
                    future_score=0,
                    remaining_minutes=0,
                    score=state.score + state.pressure*(state.remaining_minutes-1),
                    )
        else:
            return state

    def generate_neighbors(current: State) -> Generator[State, None, None]:
        """
        """
        for name, elephant in product(nx.neighbors(G, current.name), nx.neighbors(G, current.elephant)):
            if name == elephant:
                continue
            # Moving to our neighbor.
            remaining_minutes = current.remaining_minutes - 1
            possible_valve = State(
                        name=name,
                        elephant=elephant,
                        remaining_minutes=remaining_minutes,
                        score=current.score + 1*current.pressure,
                        # Note that the future score should be less because a minute pass.
                        future_score=expected_future_score(current.open_valves, ordered_valves, remaining_minutes),
                        pressure=current.pressure,
                        open_valves=current.open_valves,
                        )
            yield possible_valve


    best = 0
    states = [State(
        name=START,
        elephant=START,
        pressure=0,
        score=0,
        future_score=expected_future_score({START}, ordered_valves, MINUTES),
        open_valves=frozenset({START} | valves_without_flow),
        remaining_minutes=MINUTES,
        )]
    while len(states) > 0:
        #best = min(best, current.score)
        best = min(best, min(state.score for state in states))
        heapq.heapify(states)
        current = heapq.heappop(states)

        if current.remaining_minutes <= 0:
            print(current)
            print(len(states))
            print(*sorted(states, key=lambda s: s.score, reverse=True), sep="\n")
            return current.score

        if best > current.expected_score:
            """
            From this current state, even if we are optimistic, it is NOT
            possible to beat the best state so far.
            """
            print(f"Dropping {current}")
            continue

        # We move to the neighbors without opening the valve.
        #states.extend(list(generate_neighbors(current)))

        # Both the elephant and I can act during the next minute.
        # We both visit our neighbors.
        states.extend(generate_neighbors(current))

        remaining_minutes = current.remaining_minutes - 1
        if current.name not in current.open_valves:
            # I open a valve while the elephant visit its neighbors.
            flow = G.nodes[current.name]["flow"]
            pressure = current.pressure+flow
            open_valves = frozenset(current.open_valves | {current.name})

            states.extend(
                    State(
                        name=current.name,
                        elephant=neighbor,
                        score=current.score + 1*pressure,
                        pressure=pressure,
                        open_valves=open_valves,
                        remaining_minutes=remaining_minutes,
                        future_score=expected_future_score(open_valves, ordered_valves, remaining_minutes),
                        )
                    for neighbor in nx.neighbors(G, current.elephant))

        if current.elephant not in current.open_valves:
            # Now the elephant is opening a valve while I move to a neighbor.
            flow = G.nodes[current.elephant]["flow"]
            pressure = current.pressure+flow
            open_valves = frozenset(current.open_valves | {current.elephant})

            states.extend(
                    State(
                        name=neighbor,
                        elephant=current.elephant,
                        score=current.score + 1*pressure,
                        pressure=pressure,
                        open_valves=open_valves,
                        remaining_minutes=remaining_minutes,
                        future_score=expected_future_score(open_valves, ordered_valves, remaining_minutes),
                        )
                    for neighbor in nx.neighbors(G, current.name))

        if current.name != current.elephant \
                and current.elephant not in current.open_valves \
                and current.name not in current.open_valves:
            # Now the elephant is opening a valve while I move to a neighbor.
            flow = G.nodes[current.elephant]["flow"]
            flow += G.nodes[current.name]["flow"]
            pressure = current.pressure+flow
            open_valves = frozenset(current.open_valves | {current.name, current.elephant})

            states.append(
                    State(
                        name=current.name,
                        elephant=current.elephant,
                        score=current.score + 1*pressure,
                        pressure=pressure,
                        open_valves=open_valves,
                        remaining_minutes=remaining_minutes,
                        future_score=expected_future_score(open_valves, ordered_valves, remaining_minutes),
                        ))

        if True:
            states = [finalize(state) for state in states]

        if True:
            """
            It is critical not to add states that are already in the states list.
            """
            presize = len(states)
            states = [state for state in set(states) if state.expected_score > best]
            #print(f"Dropped {presize-len(states)}")

    return None





if __name__ == "__main__":
    assert (answer := part1("test")) == 1651, answer
    answer = part1()
    print(f"Part1 answer: {answer}")
    assert answer == 2124

    print()

    assert (answer := part2("test")) == 1707, answer
    answer = part2()
    print(f"Part2 answer: {answer}")
    assert answer == 205615
