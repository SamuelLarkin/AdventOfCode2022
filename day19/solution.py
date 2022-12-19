#!/usr/bin/env  python3

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

import re



MINUTES = 24



class Material(NamedTuple):
    """
    """
    ore: int=0
    clay: int=0
    obsidian: int=0
    geode: int=0

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



class Blueprint(NamedTuple):
    """
    """
    bid: int
    robot_ore: Material
    robot_clay: Material
    robot_obsidian: Material
    robot_geode: Material



#Blueprint 10: Each ore robot costs 4 ore. Each clay robot costs 3 ore. Each obsidian robot costs 2 ore and 17 clay. Each geode robot costs 3 ore and 16 obsidian.
blueprint_re = re.compile(r"^Blueprint (?P<blueprint_id>\d+): Each ore robot costs (?P<ore_robot_ore>\d+) ore. Each clay robot costs (?P<clay_robot_ore>\d+) ore. Each obsidian robot costs (?P<obsidian_robot_ore>\d+) ore and (?P<obsidian_robot_clay>\d+) clay. Each geode robot costs (?P<geode_robot_ore>\d+) ore and (?P<geode_robot_clay>\d+) obsidian.")
def parser(data: str="data") -> Generator[Blueprint, None, None]:
    """
    """
    with open(data, mode="r", encoding="UTF8") as fin:
        for line in map(str.strip, fin):
            m = blueprint_re.match(line)
            assert m is not None, line
            yield Blueprint(
                    bid = int(m.group("blueprint_id")),
                    robot_ore = Material(ore=int(m.group("ore_robot_ore"))),
                    robot_clay = Material(ore=int(m.group("clay_robot_ore"))),
                    robot_obsidian = Material(
                        ore = int(m.group("obsidian_robot_ore")),
                        clay = int(m.group("obsidian_robot_clay")),
                        ),
                    robot_geode = Material(
                        ore  = int(m.group("geode_robot_ore")),
                        clay = int(m.group("geode_robot_clay")),
                        ),
                    )



def possible_robots(
        blueprint: Blueprint,
        material: Material,
        ) -> Generator[Tuple, None, None]:
    """
    """
    for r_ore, r_clay, r_obsidian, r_geode in product(range(3), repeat=4):
        #if r_ore == 0 and r_clay == 0 and r_obsidian == 0 and r_geode == 0:
        #    continue
        cost = Material()
        cost += blueprint.robot_ore * r_ore
        cost += blueprint.robot_clay * r_clay
        cost += blueprint.robot_obsidian * r_obsidian
        cost += blueprint.robot_geode * r_geode
        if cost < material:
            yield r_ore, r_clay, r_obsidian, r_geode




def extract_geodes(blueprint: Blueprint) -> int:
    """
    """
    class State(NamedTuple):
        material: Material=Material()
        robot_ore: int=1
        robot_clay: int=0
        robot_obsidian: int=0
        robot_geode: int=0
        minutes: int=0

    states = [State()]
    while len(states) > 0:
        state = states.pop()

        if state.minutes >= MINUTES:
            yield state

        # We have new material
        state = state._replace(
                material=Material(
                    ore=state.material.ore+state.robot_ore,
                    clay=state.material.clay+state.robot_clay,
                    obsidian=state.material.obsidian+state.robot_obsidian,
                    geode=state.material.geode+state.robot_geode,
                    ),
                minutes=state.minutes+1,
                )

        # Start building robots
        for r_ore, r_clay, r_obsidian, r_geode in possible_robots(blueprint, state.material):
            material = state.material \
                    - blueprint.robot_ore * r_ore \
                    - blueprint.robot_clay * r_clay \
                    - blueprint.robot_obsidian * r_obsidian \
                    - blueprint.robot_geode * r_geode
            states.append(State(
                material=material,
                robot_ore=state.robot_ore+r_ore,
                robot_clay=state.robot_clay+r_clay,
                robot_obsidian=state.robot_obsidian+r_obsidian,
                robot_geode=state.robot_geode+r_geode,
                minutes=state.minutes,
                ))

    pass



def part1() -> int:
    """
    What do you get if you add up the quality level of all of the blueprints in your list?
    """
    blueprints = list(parser("test"))
    #blueprints = list(parser())
    print(*blueprints, sep="\n")
    for blueprint in blueprints:
        geodes = list(extract_geodes(blueprint))
        print(blueprint.bid, geodes)

    return None



def part2() -> int:
    """
    """
    return 0





if __name__ == "__main__":
    answer = part1()
    print(f"Part1 answer: {answer}")
    assert answer == 69289

    answer = part2()
    print(f"Part2 answer: {answer}")
    assert answer == 205615
