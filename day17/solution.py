#!/usr/bin/env  python3

from itertools import (
        count,
        cycle,
        groupby,
        )
from operator import (
        attrgetter,
        itemgetter,
        )
from tqdm import trange
from typing import (
        Callable,
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
    """
    """
    x: int
    y: int

    def __add__(self, other) -> "Position":
        """
        """
        return Position(self.x+other.x, self.y+other.y)



class Block(NamedTuple):
    """
    """
    position: Set[Position]
    width: int
    height: int

    def move(self, position: Position) -> "Block":
        """
        """
        return Block(
                set(p+position for p in self.position),
                self.width,
                self.height,
                )



def generate_block() -> Block:
    """
    """
    # -
    yield Block((
            Position(0, 0),
            Position(1, 0),
            Position(2, 0),
            Position(3, 0),
            ),
            4,
            1,
            )
    # +
    yield Block((
            Position(1, 0),
            Position(0, 1),
            Position(1, 1),
            Position(2, 1),
            Position(1, 2),
            ),
            3,
            3,
            )
    # L
    yield Block((
            Position(0, 0),
            Position(1, 0),
            Position(2, 0),
            Position(2, 1),
            Position(2, 2),
            ),
            3,
            3,
            )
    # I
    yield Block((
            Position(0, 0),
            Position(0, 1),
            Position(0, 2),
            Position(0, 3),
            ),
            1,
            4,
            )
    # #
    yield Block((
            Position(0, 0),
            Position(1, 0),
            Position(0, 1),
            Position(1, 1),
            ),
            2,
            2,
            )



def parser(data: str="data") -> Generator[Position, None, None]:
    """
    """
    with open(data, mode="r", encoding="UTF8") as fin:
        for line in map(str.strip, fin):
            for direction in line:
                if direction == "<":
                    yield Position(-1, 0)
                elif direction == ">":
                    yield Position(1, 0)
                else:
                    assert False, line



def display_cave(cave: Set[Position]):
    """
    """
    lines = sorted(cave, key=attrgetter("y"), reverse=True)
    lines = groupby(lines, key=attrgetter("y"))
    for y, positions in lines:
        d = ["."] * 7
        for p in positions:
            d[p.x] = "#"
        print(''.join(d))
    print()



def find_repeating_pattern(steps: int, directions: Iterable[Position]) -> int:
    """
    0 Position(x=0, y=0) 0
    8668 Position(x=0, y=13313) 13313
    17343 Position(x=0, y=26648) 13335
    26018 Position(x=0, y=39983) 13335
    34693 Position(x=0, y=53318) 13335
    43368 Position(x=0, y=66653) 13335
    52043 Position(x=0, y=79988) 13335
    """
    WIDTH = 7

    num_direction = len(directions)
    num_block = 5

    blocks = cycle(generate_block())
    winds  = cycle(directions)

    top    = Position(0, 0)
    offset = Position(2, 3)
    # Cave's floor
    cave: Set[Position]=set((
            Position(0, -1),
            Position(1, -1),
            Position(2, -1),
            Position(3, -1),
            Position(4, -1),
            Position(5, -1),
            Position(6, -1),
            ))
    last = top
    wind_id=0
    for step in range(steps):
        block = next(blocks)
        block = block.move(top+offset)
        for _ in count():
            if wind_id % (num_direction * num_block) == 0:
                print(step, top, top.y - last.y)
                last = top

            wind = next(winds)
            wind_id+=1

            # If any movement would cause any part of the rock to move into the
            # walls, floor, or a stopped rock, the movement instead does not
            # occur.
            pushed_block = block.move(wind)
            if all(0 <= p.x < WIDTH for p in pushed_block.position) \
                    and len(pushed_block.position & cave) == 0:
                block = pushed_block

            # If a downward movement would have caused a falling rock to move
            # into the floor or an already-fallen rock, the falling rock stops
            # where it is (having landed on something) and a new rock
            # immediately begins falling.
            down_block = block.move(Position(0, -1))
            if len(down_block.position & cave) == 0:
                block = down_block
            else:
                cave.update(block.position)
                top = Position(
                        0,
                        max(p.y for p in cave) + 1,
                        )
                #display_cave(cave)
                break
        else:
            assert False

    return None



def part1(steps: int=2022) -> int:
    """
    How many units tall will the tower of rocks be after 2022 rocks have stopped falling?
    """
    WIDTH = 7

    directions = list(parser())
    blocks = cycle(generate_block())
    winds  = cycle(directions)

    top    = Position(0, 0)
    offset = Position(2, 3)
    # Cave's floor
    cave: Set[Position]=set((
            Position(0, -1),
            Position(1, -1),
            Position(2, -1),
            Position(3, -1),
            Position(4, -1),
            Position(5, -1),
            Position(6, -1),
            ))
    for _ in trange(steps):
        block = next(blocks)
        block = block.move(top+offset)
        for _ in count():
            wind = next(winds)

            # If any movement would cause any part of the rock to move into the
            # walls, floor, or a stopped rock, the movement instead does not
            # occur.
            pushed_block = block.move(wind)
            if all(0 <= p.x < WIDTH for p in pushed_block.position) \
                    and len(pushed_block.position & cave) == 0:
                block = pushed_block

            # If a downward movement would have caused a falling rock to move
            # into the floor or an already-fallen rock, the falling rock stops
            # where it is (having landed on something) and a new rock
            # immediately begins falling.
            down_block = block.move(Position(0, -1))
            if len(down_block.position & cave) == 0:
                block = down_block
            else:
                cave.update(block.position)
                top = Position(
                        0,
                        max(p.y for p in cave) + 1,
                        )
                #display_cave(cave)
                break
        else:
            assert False


    return top.y



def part2() -> int:
    """
    How tall will the tower be after 1000000000000 rocks have stopped?

    0 Position(x=0, y=0) 0
    8668 Position(x=0, y=13313) 13313
    17343 Position(x=0, y=26648) 13335
    26018 Position(x=0, y=39983) 13335
    34693 Position(x=0, y=53318) 13335
    43368 Position(x=0, y=66653) 13335
    """
    STEPS = 1_000_000_000_000
    #find_repeating_pattern(STEPS, list(parser()))
    first_step = 8668
    repeating_steps = 8675   # 26018-17343
    num_repeating = (STEPS - first_step) // repeating_steps
    remaining_steps = (STEPS - first_step) % repeating_steps
    assert 8668 + repeating_steps*num_repeating + remaining_steps == STEPS
    last_block = part1(first_step + remaining_steps)

    return 13313 + 13335 * num_repeating + (last_block - 13313)






if __name__ == "__main__":
    if True:
        answer = part1()
        print(f"Part1 answer: {answer}")
        assert answer == 3106

    if True:
        answer = part2()
        print(f"Part2 answer: {answer}")
        assert answer == 1537175792495
