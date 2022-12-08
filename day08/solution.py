#!/usr/bin/env  python3

import numpy as np

from typing import (
        Generator,
        List,
        Tuple,
        )



def parser(data: str="data"): 
    """
    """
    with open(data, mode="r", encoding="UTF8") as fin:
        data = [ list(map(int, line)) for line in map(str.strip, fin) ]

    return np.asarray(data)


def part1() -> int:
    """
    How many trees are visible from outside the grid?
    """
    grid = parser()
    height, width = grid.shape
    count = 2 * (height + width - 2)
    for x in range (1, height-1):
        for y in range(1, width-1):
            tree = grid[x,y]
            down = grid[x, y+1:]
            up = grid[x, :y]
            left = grid[:x, y]
            right = grid[x+1:, y]
            assert 1 + len(up) + len(down) == height
            assert 1 + len(left) + len(right) == width
            if max(up) < tree \
                    or max(down) < tree \
                    or max(left) < tree \
                    or max(right) < tree:
                count += 1

    return count



def part2() -> int:
    """
    What is the highest scenic score possible for any tree?
    """
    def distance(tree: int, line_of_sight) -> int:
        """
        """
        for i, t in enumerate(line_of_sight, 1):
            if t >= tree:
                return i

        return i

    grid = parser()
    height, width = grid.shape
    max_scenic_score = 0
    for x in range (1, height-1):
        for y in range(1, width-1):
            tree = grid[x,y]
            down = grid[x, y+1:]
            up = grid[x, :y]
            left = grid[:x, y]
            right = grid[x+1:, y]
            assert 1 + len(up) + len(down) == height
            assert 1 + len(left) + len(right) == width
            scenic_score = distance(tree, down) \
                    * distance(tree, np.flip(up)) \
                    * distance(tree, right) \
                    * distance(tree, np.flip(left))

            max_scenic_score = max(scenic_score, max_scenic_score)

    return max_scenic_score





if __name__ == "__main__":
    answer = part1()
    print(f"Part1 answer: {answer}")
    assert answer == 1700

    answer = part2()
    print(f"Part2 answer: {answer}")
    assert answer == 470596
