#!/usr/bin/env  python3

from collections import Counter
from dataclasses import dataclass
from enum import Enum
from itertools import (
        count,
        product,
        )
from operator import attrgetter
from typing import (
        Callable,
        Dict,
        Generator,
        Iterable,
        List,
        NamedTuple,
        Sequence,
        Set,
        Tuple,
        Union,
        )



class Position(NamedTuple):
    x: int
    y: int

    def __add__(self, direction: "Position") -> "Position":
        """
        """
        return Position(self.x+direction.x, self.y+direction.y)



DIRECTIONS = [
        Position(0, -1),   # N
        Position(0, 1),    # S
        Position(-1, 0),   # W
        Position(1, 0),    # E
        ]
POSITIONS_TO_CHECK = [
        (Position(-1, -1), Position(0, -1), Position(1, -1)),   # N
        (Position(-1, 1), Position(0, 1), Position(1, 1)),      # S
        (Position(-1, 1), Position(-1, 0), Position(-1, -1)),   # W
        (Position(1, 1), Position(1, 0), Position(1, -1)),      # E
        ]
SURROUNDING_POSITIONS = list(
        map(lambda p: Position(*p),
            filter(
                lambda p: p!=(0, 0),
                product(range(-1, 2), repeat=2)
                )
            )
        )



def parser(data: str="data") -> Generator[Position, None, None]:
    """
    """
    with open(data, mode="r", encoding="UTF8") as fin:
        for y, line in enumerate(map(str.strip, fin)):
            for x, v in enumerate(line):
                if v == "#":
                    yield Position(x, y)



def surrounding(
        position: Position,
        surroundings: Iterable[Position]=SURROUNDING_POSITIONS,
        ) -> Generator[Position, None, None]:
    """
    """
    for d in surroundings:
        yield position + d



def display(elves: Set[Position]):
    """
    """
    xs = sorted(map(attrgetter("x"), elves))
    ys = sorted(map(attrgetter("y"), elves))
    for y in range(ys[0], ys[-1]+1):
        for x in range(xs[0], xs[-1]+1):
            if Position(x, y) in elves:
                print("#", end='')
            else:
                print(".", end='')
        print()
    print()



def perform_round(elves: Set[Position], step: int) -> Set[Position]:
    """
    """
    new_elves = set()
    proposed_positions = Counter()
    next_positions: Dict[Position, Position] = dict()
    for position in elves:
        if len(set(surrounding(position)) & elves) == 0:
            """
            Each Elf considers the eight positions adjacent to themself. If
            no other Elves are in one of those eight positions, the Elf
            does not do anything during this round.
            """
            # This elf could not move.
            proposed_positions.update((position,))
            new_elves.add(position)
            continue
        """
        Otherwise, the Elf looks in each of four directions in the
        following order and proposes moving one step in the first valid
        direction
        """
        for i in range(4):
            direction_indice = (step+i)%4
            direction = DIRECTIONS[direction_indice]
            proposed_position = position + direction
            if len(set(surrounding(position, POSITIONS_TO_CHECK[direction_indice])) & elves) == 0:
                proposed_positions.update((proposed_position,))
                next_positions[position] = proposed_position
                break
        else:
            # This elf could not move.
            proposed_positions.update((position,))
            new_elves.add(position)

    assert len(next_positions)+len(new_elves) == len(elves)
    assert sum(proposed_positions.values()) == len(elves)

    """
    Simultaneously, each Elf moves to their proposed destination tile if
    they were the only Elf to propose moving to that position. If two or
    more Elves propose moving to the same position, none of those Elves
    move.
    """
    for position, next_position in next_positions.items():
        if proposed_positions[next_position] == 1:
            new_elves.add(next_position)
        else:
            new_elves.add(position)

    assert len(elves) == len(new_elves)
    elves = new_elves

    #display(elves)

    return elves



def part1(data: str="data", rounds: int=10) -> int:
    """
    Simulate the Elves' process and find the smallest rectangle that contains the Elves after 10 rounds.
    How many empty ground tiles does that rectangle contain?
    """
    elves = set(parser(data))
    if False:
        print(*elves, sep="\n")
        display(elves)

    for step in range(rounds):
        elves = perform_round(elves, step)

    xs = sorted(map(attrgetter("x"), elves))
    ys = sorted(map(attrgetter("y"), elves))
    #print(xs[0], xs[-1], ys[0], ys[-1])
    return (xs[-1]-xs[0]+1) * (ys[-1]-ys[0]+1) - len(elves)



def part2(data: str="data") -> int:
    """
    Figure out where the Elves need to go.
    What is the number of the first round where no Elf moves?
    """
    elves = set(parser(data))

    for step in count():
        new_elves = perform_round(elves, step)
        if new_elves == elves:
            break
        elves = new_elves

    return step+1





if __name__ == "__main__":
    assert (answer := part1("test")) == 110, answer
    answer = part1()
    print(f"Part1 answer: {answer}")
    assert answer == 4052

    print()

    assert (answer := part2("test")) == 20, answer
    answer = part2()
    print(f"Part2 answer: {answer}")
    assert answer == 978
