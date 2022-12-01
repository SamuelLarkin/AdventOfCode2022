#!/usr/bin/python3

from typing import (
        Generator,
        Iterable,
        List,
        )

def reader(iterable: Iterable) -> Generator[List[int], None, None]:
    """
    Iterates of each elf's bag and return a list of snacks' calories.
    """
    data = []
    for line in map(str.strip, iterable):
        if line == "":
            yield data
            data = []
        else:
            data.append(int(line))
    if len(data) > 0:
        yield data



def part1() -> int:
    """
    How many total Calories is that Elf carrying?
    """
    with open("data", mode="r", encoding="UTF8") as data:
        calories_per_elf = map(sum, reader(data))
        return max(calories_per_elf)



def part2(top_elves: int=3) -> int:
    """
    How many Calories are those Elves carrying in total?
    """
    with open("data", mode="r", encoding="UTF8") as data:
        calories_per_elf = map(sum, reader(data))
        most_calories = sorted(calories_per_elf)[-top_elves:]
        return sum(most_calories)





if __name__ == "__main__":
    answer = part1()
    assert answer == 69289
    print(f"Part1 answer: {answer}")

    answer = part2()
    assert answer == 205615
    print(f"Part2 answer: {answer}")
