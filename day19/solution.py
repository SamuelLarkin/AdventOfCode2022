#!/usr/bin/env  python3

from collections import defaultdict
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

    def __add__(self, other: Union["Material", List[int]]) -> "Material":
        """
        """
        if isinstance(other, Sequence):
            assert len(other) == 4
            return Material(
                    ore=self.ore+other[Robot.ore.value],
                    clay=self.clay+other[Robot.clay.value],
                    obsidian=self.obsidian+other[Robot.obsidian.value],
                    geode=self.geode+other[Robot.geode.value],
                    )
        else:
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
        return self.material.geode + self.future_score


    def __lt__(self, other) -> bool:
        """
        """
        return self.score > other.score



def compute_future_score(max_robot_needed, robots, minutes_left: int) -> int:
    """
    """
    #return robots[Robot.geode.value] * minutes_left
    return robots[Robot.geode.value] * minutes_left \
            - 4 * max(0, max_robot_needed[Robot.ore] - robots[Robot.ore.value]) \
            - 2 * max(0, max_robot_needed[Robot.clay] - robots[Robot.clay.value]) \
            - 1 * max(0, max_robot_needed[Robot.obsidian] - robots[Robot.obsidian.value])



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
    print(max_robot_needed)
    max_possible_geode_so_far = defaultdict(lambda: 0)
    states = [
            State(minutes=MINUTES, next_robot=robot)
            for robot in Robot
            ]
    test = []
    while len(states) > 0:
        #print(len(states))
        state = heapq.heappop(states)

        if state.minutes <= 0:
            #print(state)
            test.append(state)
            continue
            return state.material.geode

        if state.robots[state.next_robot.value] >= max_robot_needed[state.next_robot]:
            # We don't need anymore of this type of robot.
            continue

        minutes = state.minutes - 1
        if state.material.geode < max_possible_geode_so_far[minutes]:
            continue
        else:
            max_possible_geode_so_far[minutes] = state.material.geode

        if state.material >= blueprint.robots[state.next_robot.value]:
            # Do we have enough material to build our next robot?
            material = state.material - blueprint.robots[state.next_robot.value]
            # We collect the new material.
            material = material + state.robots
            robots = [ v for v in state.robots ]
            robots[state.next_robot.value] += 1
            if True:
                for next_robot in Robot:
                    new_state = State(
                            minutes=minutes,
                            material=material,
                            robots=robots,
                            next_robot=next_robot,
                            future_score=compute_future_score(
                                max_robot_needed,
                                robots,
                                minutes,
                                ),
                            )
                    heapq.heappush(states, new_state)
            else:
                next_robot = Robot.ore
                new_state = State(
                        minutes=minutes,
                        material=material,
                        robots=robots,
                        next_robot=next_robot,
                        future_score=compute_future_score(
                            max_robot_needed,
                            robots,
                            minutes,
                            ),
                        )
                heapq.heappush(states, new_state)
        else:
            # We collect the new material.
            material = state.material + state.robots
            state = State(
                    minutes=minutes,
                    material=material,
                    robots=state.robots,
                    next_robot=state.next_robot,
                    future_score=compute_future_score(
                        max_robot_needed,
                        state.robots,
                        minutes,
                        ),
                    )
            heapq.heappush(states, state)

    return max(s.material.geode for s in test)



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
    assert (answer := part1("test")) == 33, answer
    answer = part1()
    print(f"Part1 answer: {answer}")
    assert answer == 1346

    print()

    assert (answer := part2("test")) == 152, answer
    answer = part2()
    print(f"Part2 answer: {answer}")
    assert answer == 205615
