#!/usr/bin/env  python3

from dataclasses import dataclass
from functools import (
        partial,
        reduce,
        )
from tqdm import trange
from typing import (
        Callable,
        Generator,
        List,
        Sequence,
        Tuple,
        )

import re



@dataclass
class Monkey:
    items: List[int]
    operation: Callable[[int], int]
    test: int
    positive: int
    negative: int
    inspected: int=0



items_re = re.compile(r"\s*Starting items: (.*)")
operation_re = re.compile(r"\s*Operation: new = old (?P<operator>[*+]) (?P<arg>\d+|old)")
test_re = re.compile(r"\s*Test: divisible by (\d+)")
positive_re = re.compile(r"\s*If true: throw to monkey (\d+)")
negative_re = re.compile(r"\s*If false: throw to monkey (\d+)")
def parser(data: str="data") -> Generator[Monkey, None, None]:
    """
    Monkey 0:
      Starting items: 79, 98
      Operation: new = old * 19
      Test: divisible by 23
        If true: throw to monkey 2
        If false: throw to monkey 3
    """
    with open(data, mode="r", encoding="UTF8") as fin:
        for line in map(str.strip, fin):
            if line == "":
                yield Monkey(
                        items=items,
                        operation=operation,
                        test=test,
                        positive=positive,
                        negative=negative,
                        )
                continue

            m = items_re.match(line)
            if m is not None:
                items = list(map(int, m.group(1).split(",")))
                continue

            m = operation_re.match(line)
            if m is not None:
                operator = m.group("operator")
                arg = m.group("arg")
                if arg == "old":
                    if operator == "*":
                        operation = lambda x: x * x
                    elif operator == "+":
                        operation = lambda x: x + x
                    else:
                        assert False, f"Unknown operator {operator}"
                else:
                    arg = int(arg)
                    if operator == "*":
                        operation = partial(lambda x, a: x * a, a=arg)
                    elif operator == "+":
                        operation = partial(lambda x, a: x + a, a=arg)
                    else:
                        assert False, f"Unknown operator {operator}"
                continue

            m = test_re.match(line)
            if m is not None:
                test = int(m.group(1))
                continue

            m = positive_re.match(line)
            if m is not None:
                positive = int(m.group(1))
                continue

            m = negative_re.match(line)
            if m is not None:
                negative = int(m.group(1))
                continue

        yield Monkey(
                items=items,
                operation=operation,
                test=test,
                positive=positive,
                negative=negative,
                )



def validate_monkeys(monkeys: Sequence[Monkey]):
    """
    """
    assert all(0 <= m.positive < len(monkeys) for m in monkeys), f"{[m.positive for m in monkeys]}"
    assert all(0 <= m.negative < len(monkeys) for m in monkeys), f"{[m.negative for m in monkeys]}"



def track(monkeys: Sequence[Monkey], num_rounds: int, level_manager: Callable[[int], int]) -> int:
    """
    Core algorithm.
    """
    for _ in range(num_rounds):
        for mid, monkey in enumerate(monkeys): 
            monkey.inspected += len(monkey.items)
            for item in monkey.items:
                item = monkey.operation(item)
                item = level_manager(item)
                if item % monkey.test == 0:
                    monkeys[monkey.positive].items.append(item)
                else:
                    monkeys[monkey.negative].items.append(item)
            monkey.items = []

    a, b, *_ = sorted((m.inspected for m in monkeys), reverse=True)
    return a * b



def part1() -> int:
    """
    What is the level of monkey business after 20 rounds of stuff-slinging simian shenanigans?
    """
    monkeys = list(parser())
    validate_monkeys(monkeys)

    return track(monkeys, 20, lambda l: l//3)



def part2() -> int:
    """
    What is the level of monkey business after 10000 rounds?
    """
    monkeys = list(parser())
    validate_monkeys(monkeys)

    modulo = reduce(lambda t, m: t*m.test, monkeys, 1)
    return track(monkeys, 10_000, lambda l: l % modulo)





if __name__ == "__main__":
    answer = part1()
    print(f"Part1 answer: {answer}")
    assert answer == 54253

    answer = part2()
    print(f"Part2 answer: {answer}")
    assert answer == 13_119_526_120
