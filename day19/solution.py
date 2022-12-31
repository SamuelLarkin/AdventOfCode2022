#!/usr/bin/env  python3

from enum import Enum
from itertools import product
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

import heapq
import re



MINUTES = 24
class Robot(Enum):
    geode=0
    obsidian=1
    clay=2
    ore=3



class Material(NamedTuple):
    """
    """
    geode: int=0
    obsidian: int=0
    clay: int=0
    ore: int=0

    def __add__(self, other: "Material") -> "Material":
        """
        """
        return Material(
                ore=self.ore+other.ore,
                clay=self.clay+other.clay,
                obsidian=self.obsidian+other.obsidian,
                geode=self.geode+other.geode,
                )

    def __sub__(self, other: "Material") -> "Material":
        """
        """
        return Material(
                ore=self.ore-other.ore,
                clay=self.clay-other.clay,
                obsidian=self.obsidian-other.obsidian,
                geode=self.geode-other.geode,
                )

    def __mul__(self, factor: int) -> "Material":
        """
        """
        return Material(
                ore=factor*self.ore,
                clay=factor*self.clay,
                obsidian=factor*self.obsidian,
                geode=factor*self.geode,
                )

    def __ge__(self, other: "Material") -> bool:
        """
        """
        return self.ore >= other.ore \
                and self.clay >= other.clay \
                and self.obsidian >= other.obsidian \
                and self.geode >= other.geode



class Blueprint(NamedTuple):
    """
    """
    bid: int
    robots: List[Material]



#Blueprint 10: Each ore robot costs 4 ore. Each clay robot costs 3 ore. Each obsidian robot costs 2 ore and 17 clay. Each geode robot costs 3 ore and 16 obsidian.
blueprint_re = re.compile(r"^Blueprint (?P<blueprint_id>\d+): "
                          r"Each ore robot costs (?P<ore_robot_ore>\d+) ore. "
                          r"Each clay robot costs (?P<clay_robot_ore>\d+) ore. "
                          r"Each obsidian robot costs (?P<obsidian_robot_ore>\d+) ore and (?P<obsidian_robot_clay>\d+) clay. "
                          r"Each geode robot costs (?P<geode_robot_ore>\d+) ore and (?P<geode_robot_obsidian>\d+) obsidian.")
def parser(data: str="data") -> Generator[Blueprint, None, None]:
    """
    """
    with open(data, mode="r", encoding="UTF8") as fin:
        for line in map(str.strip, fin):
            m = blueprint_re.match(line)
            assert m is not None, line
            yield Blueprint(
                    bid = int(m.group("blueprint_id")),
                    robots = [
                        Material(
                            ore  = int(m.group("geode_robot_ore")),
                            obsidian = int(m.group("geode_robot_obsidian")),
                            ),
                        Material(
                            ore  = int(m.group("obsidian_robot_ore")),
                            clay = int(m.group("obsidian_robot_clay")),
                            ),
                        Material(ore=int(m.group("clay_robot_ore"))),
                        Material(ore=int(m.group("ore_robot_ore"))),
                        ]
                    )



class State(NamedTuple):
    """
    """
    minutes: int   # Number of minutes left.
    material: Material=Material()
    robots: List[int]=[0, 0, 0, 1]
    next_robot: Robot=None
    future_score: int=0

    @property
    def score(self) -> int:
        """
        """
        return self.robots[Robot.geode.value] + self.future_score


    def __lt__(self, other) -> bool:
        """
        """
        return self.score > other.score



def compute_future_score(num_geode_robots: int, minutes_left: int) -> int:
    """
    """
    return num_geode_robots * minutes_left



def find_max_robot_needed(blueprint: Blueprint):
    """
    There is no need to have more robots to mine some type of ore then what is
    request to build a robot.
    """
    max_robot_needed = [0 for _ in blueprint.robots]
    for robot in blueprint.robots:
        for material_id, material in enumerate(robot):
            max_robot_needed[material_id] = max(material, max_robot_needed[material_id])

    max_robot_needed[Robot.geode.value] = 99999

    return { r: mr for r, mr in zip(Robot, max_robot_needed) }



def extract_geodes(blueprint: Blueprint) -> int:
    """
    """
    max_robot_needed = find_max_robot_needed(blueprint)
    states = [ State(minutes=MINUTES) ]
    while len(states) > 0:
        print(len(states))
        state = heapq.heappop(states)

        if state.minutes <= 0:
            return state.material.geode

        if state.next_robot is None:
            # Here we simply select the next robot to build.
            for robot in Robot:
                if state.robots[robot.value] >= max_robot_needed[robot]:
                    # We don't need anymore of this type of robot.
                    continue
                new_state = state._replace(next_robot=robot)
                heapq.heappush(states, new_state)
        elif state.material >= blueprint.robots[state.next_robot.value]:
                # Do we have enough material to build our next robot?
                material = state.material - blueprint.robots[state.next_robot.value]
                robots = [ v for v in state.robots ]
                robots[state.next_robot.value] += 1
                new_state = State(
                        minutes=state.minutes,
                        material=material,
                        robots=robots,
                        next_robot=None,
                        future_score=compute_future_score(
                            robots[Robot.geode.value],
                            state.minutes,
                            )
                        )
                heapq.heappush(states, new_state)
        else:
            # We simply collect the new material.
            #material = Material(
            #        ore=state.material[0]+state.robots[0],
            #        clay=state.material[1]+state.robots[1],
            #        obsidian=state.material[2]+state.robots[2],
            #        geode=state.material[3]+state.robots[3],
            #        )
            material = Material(*[
                c+n for c, n in zip(state.material, state.robots)
                ])
            minutes = state.minutes - 1
            new_state = State(
                    minutes=minutes,
                    material=material,
                    robots=state.robots,
                    next_robot=state.next_robot,
                    future_score=compute_future_score(
                        state.robots[Robot.geode.value],
                        minutes,
                        )
                    )
            heapq.heappush(states, new_state)

    return None



def part1(data: str="data") -> int:
    """
    What do you get if you add up the quality level of all of the blueprints in your list?
    """
    blueprints = list(parser(data))

    quality_level = 0
    #print(*blueprints, sep="\n")
    for blueprint in blueprints:
        print(blueprint)
        num_geode = extract_geodes(blueprint)
        print(num_geode)
        quality_level += blueprint.bid * num_geode

    return quality_level



def part2() -> int:
    """
    """
    return 0





if __name__ == "__main__":
    assert (answer := part1("test")) == 9, answer
    answer = part1()
    print(f"Part1 answer: {answer}")
    assert answer == 69289

    print()

    assert (answer := part2("test")) == 152, answer
    answer = part2()
    print(f"Part2 answer: {answer}")
    assert answer == 205615
