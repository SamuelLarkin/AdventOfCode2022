#!/usr/bin/env  python3

from dataclasses import dataclass
from itertools import tee
from typing import (
        Generator,
        List,
        NamedTuple,
        Tuple,
        )



class Position(NamedTuple):
    x: int
    y: int


class Direction(NamedTuple):
    x: int
    y: int


class Move(NamedTuple):
    direction: Direction
    step: int



def parser(data: str="data") -> Generator[Move, None, None]:
    """
    """
    with open(data, mode="r", encoding="UTF8") as fin:
        for line in map(str.strip, fin):
            d, step = line.split()
            step = int(step)
            if d == "U":
                yield Move(Direction(0, 1), step)
            elif d == "D":
                yield Move(Direction(0, -1), step)
            elif d == "R":
                yield Move(Direction(1, 0), step)
            elif d == "L":
                yield Move(Direction(-1, 0), step)
            else:
                assert False, line



def move_knot(knot: Position, direction: Direction) -> Position:
    """
    """
    return Position(knot.x + direction.x, knot.y + direction.y)



def follow_initial_implementation(tail: Position, head: Position) -> Position:
    """
    """
    x, y = tail

    if x - 2 == head.x and y - 2 == head.y:
        x -= 1
        y -= 1
    elif x + 2 == head.x and y - 2 == head.y:
        x += 1
        y -= 1
    elif x - 2 == head.x and y + 2 == head.y:
        x -= 1
        y += 1
    elif x + 2 == head.x and y + 2 == head.y:
        x += 1
        y += 1
    elif x - 2 == head.x:
        x -= 1
        y = head.y
    elif x + 2 == head.x:
        x += 1
        y = head.y
    elif y - 2 == head.y:
        y -= 1
        x = head.x
    elif y + 2 == head.y:
        y += 1
        x = head.x

    new_tail = Position(x, y)
    #assert is_touching(head, new_tail), f"H:{head} T:{tail} NT:{new_tail}"
    return new_tail



def follow(tail: Position, head: Position) -> Position:
    """
    """
    if is_touching(head, tail):
        return tail

    x, y = tail
    d = Position(tail.x - head.x, tail.y - head.y)
    d = Position(d.x/2 if abs(d.x)>1 else d.x, d.y/2 if abs(d.y)>1 else d.y)
    x -= d.x
    y -= d.y

    new_tail = Position(x, y)
    return new_tail



def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)



def is_touching(head: Position, tail: Position) -> bool:
    """
    """
    # We CANNOT use the Manhattan distance.
    #return (abs(tail.x - head.x) + abs(tail.y - head.y)) <= 2
    return -1 <= head.x - tail.x <= 1 and -1 <= head.y - tail.y <= 1



def part1() -> int:
    """
    How many positions does the tail of the rope visit at least once?
    """
    head = Position(0, 0)
    tail = Position(0, 0)
    visited = set((tail,))
    for move in parser():
        for _ in range(move.step):
            head = move_knot(head, move.direction)
            tail = follow(tail, head)
            assert is_touching(head, tail), f"H:{head} T:{tail}"
            visited.add(tail)

    return len(visited)



def part2() -> int:
    """
    How many positions does the tail of the rope visit at least once?
    """
    knots = [Position(0, 0) for _ in range(1+9)]
    visited = set((knots[-1],))
    for move in parser():
        for _ in range(move.step):
            knots[0] = move_knot(knots[0], move.direction)
            for (head, tail) in pairwise(range(1+9)):
                knots[tail] = follow(knots[tail], knots[head])
                assert is_touching(knots[head], knots[tail]), f"H:{knots[head]} T:{knots[tail]}"
            visited.add(knots[-1])

    return len(visited)





if __name__ == "__main__":
    answer = part1()
    print(f"Part1 answer: {answer}")
    assert answer == 5695

    answer = part2()
    print(f"Part2 answer: {answer}")
    assert answer == 2434
