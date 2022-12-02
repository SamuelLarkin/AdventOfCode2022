#!/usr/bin/env  python3

from enum import IntEnum
from itertools import starmap
from typing import (
        Iterable,
        Generator,
        Tuple,
        )
Score = int



class Hand(IntEnum):
    """
    """
    Rock     = 1
    Paper    = 2
    Scissors = 3



class Outcome(IntEnum):
    """
    """
    Lose = 1
    Draw = 2
    Win  = 3



def reader() -> Generator[Tuple[int, int], None, None]:
    """
    """
    with open("data", mode="r", encoding="UTF8") as fin:
        for line in map(str.strip, fin):
            other, you = line.split()
            other = ord(other) - ord("A") + 1
            you = ord(you) - ord("X") + 1
            assert 1 <= other <= 3
            assert 1 <= you <= 3

            yield other, you



def score(iterable: Iterable[Tuple[Hand, Hand]]) -> Generator[Score, None, None]:
    """
    Scores a game.
    """
    for other, you in iterable:
        if other == you:
            score = you + 3
        elif you == Hand.Rock:
            if other == Hand.Paper:
                score = you + 0
            else:
                score = you + 6
        elif you == Hand.Paper:
            if other == Hand.Rock:
                score = you + 6
            else:
                score = you + 0
        elif you == Hand.Scissors:
            if other == Hand.Rock:
                score = you + 0
            else:
                score = you + 6
        else:
            assert False
        #print(f"{line} {other} {you} {other.name} {you.name} {score}")
        yield score



def part1() -> Score:
    """
    What would your total score be if everything goes exactly according to your strategy guide?
    A, X => Rock
    B, Y => Paper
    C, Z => Scissors
    """
    def converter(other, you) -> Tuple[Hand, Hand]:
        """
        """
        return Hand(other), Hand(you)

    hand_hand = starmap(converter, reader())
    return sum(score(hand_hand))



def part2() -> Score:
    """
    What would your total score be if everything goes exactly according to your strategy guide?
    A => Rock
    B => Paper
    C => Scissors
    X => Lose
    Y => Draw
    Z => Win
    """
    def converter(other, you) -> Tuple[Hand, Outcome]:
        """
        """
        return Hand(other), Outcome(you)

    def myhand(iterable: Iterable[Tuple[Hand, Outcome]]) -> Generator[Tuple[Hand, Hand], None, None]:
        """
        What hand should I play to have the desired outcome.
        """
        for other, outcome in iterable:
            if outcome == Outcome.Lose:
                if other == Hand.Rock:
                    yield other, Hand.Scissors
                elif other == Hand.Paper:
                    yield other, Hand.Rock
                else:
                    yield other, Hand.Paper
            elif outcome == Outcome.Draw:
                if other == Hand.Rock:
                    yield other, Hand.Rock
                elif other == Hand.Paper:
                    yield other, Hand.Paper
                else:
                    yield other, Hand.Scissors
            elif outcome == Outcome.Win:
                if other == Hand.Rock:
                    yield other, Hand.Paper
                elif other == Hand.Paper:
                    yield other, Hand.Scissors
                else:
                    yield other, Hand.Rock
            else:
                assert False

    hand_outcome = starmap(converter, reader())
    hand_hand = myhand(hand_outcome)
    return sum(score(hand_hand))





if __name__ == "__main__":
    answer = part1()
    assert answer == 17189
    print(f"Part 1: {answer}")

    answer = part2()
    assert answer == 13490
    print(f"Part 2: {answer}")
