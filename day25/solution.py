#!/usr/bin/env  python3

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



BASE = 5



lookup = {
        "=": -2,
        "-": -1,
        "0": 0,
        "1": 1,
        "2": 2,
        }
rev_lookup = { v: k for k, v in lookup.items() }



def parser(data: str="data") -> Generator[str, None, None]:
    """
    """
    with open(data, mode="r", encoding="UTF8") as fin:
        for line in map(str.strip, fin):
            yield line



def snafu2dedimal(snafu: str) -> int:
    """
    """
    total = 0
    for i, v in enumerate(reversed(snafu)):
        total += lookup[v] * pow(BASE, i)

    return total



class Info(NamedTuple):
    factor: int
    zero: int
    one: int
    two: int



def decimal2snafu(decimal: int) -> str:
    """
    """
    answer = ""
    delme = 0
    cache: List[Info]=[]
    for i in range(20):
        factor = pow(BASE, i)
        zero = delme
        delme += factor
        one = delme
        delme += factor
        two = delme
        cache.append(Info(factor, zero, one, two))
        if decimal <= delme:
            break

    for info in reversed(cache):
        if decimal > 0:
            if decimal <= info.zero:
                answer += "0"
                decimal -= 0*info.factor
                continue
            if decimal <= info.one:
                answer += "1"
                decimal -= 1*info.factor
                continue
            if decimal <= info.two:
                answer += "2"
                decimal -= 2*info.factor
                continue
        else:
            if decimal >= -info.zero:
                answer += "0"
                decimal += 0*info.factor
                continue
            if decimal >= -info.one:
                answer += "-"
                decimal += 1*info.factor
                continue
            if decimal >= -info.two:
                answer += "="
                decimal += 2*info.factor
                continue

    return answer



def part1(data: str="data") -> int:
    """
    """
    snafu = list(parser(data))
    decimal = list(map(snafu2dedimal, snafu))
    #print(*zip(snafu, decimal), sep="\n")
    total = sum(decimal)

    total_snafu = decimal2snafu(total)
    return (total, total_snafu)



def part2(data: str="data") -> int:
    """
    """
    return 0





if __name__ == "__main__":
    assert (answer := decimal2snafu(2022)) == "1=11-2", answer

    assert (answer := part1("test")) == (4890, "2=-1=0"), answer
    answer = part1()
    print(f"Part1 answer: {answer}")
    assert answer[1] == "2-121-=10=200==2==21"

    print()

    assert (answer := part2("test")) == 301, answer
    answer = part2()
    print(f"Part2 answer: {answer}")
    assert answer == 205615
