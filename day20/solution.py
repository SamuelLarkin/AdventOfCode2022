#!/usr/bin/env  python3

# https://github.com/copperfield42/Advent-of-Code-2022/blob/main/day20/aoc_utils.py

from collections import deque
from typing import (
        Any,
        Deque,
        Iterable,
        List,
        Tuple,
        )



def parser(filename: str="data") -> List[int]:
    """
    """
    with open(filename, mode="r", encoding="UTF8") as fin:
        data = list(map(int, map(str.strip, fin)))

    return data



def bad_part1a() -> int:
    """
    """
    data = parser("test")
    modulo = len(data)
    print(data)

    for index, (position, value) in enumerate(data):
        if value > 0:
            new_position = position + value
            for i, (p, v) in enumerate(data):
                if position < p <= new_position:
                    data[i][0] = (p - 1) % modulo
            data[index][0] = new_position
        elif value < 0:
            for i, (p, v) in enumerate(data):
                if position <= p <= position+modulo+value:
                    data[i][0] = (p + 1) % modulo
            data[index][0] = new_position

        print(data)
        assert all(p[0]>=0 for p in data)
        assert len(set(p[0] for p in data)) == modulo

    return 0



def bad_part1b() -> int:
    """
    What is the sum of the three numbers that form the grove coordinates?
    """
    #data[item_id] = item_offset
    item_offsets = parser()
    item_offsets = parser("test")
    modulo = len(item_offsets)
    print(item_offsets)

    #item_at_positions[0:modulo] = item_id
    item_at_positions = list(range(modulo))
    #where_is_items[item_id] = position
    where_is_items = list(range(modulo))
    for step in range(modulo):
        item_id = step % modulo
        item_offset = item_offsets[item_id]
        item_position = where_is_items[item_id]
        #print(item_offset, end=" ")
        if item_offset != 0:
            if item_offset < 0:
                #             7        -3          - 1 = 3
                item_offset = modulo + item_offset - 1

            #                 5           +    4       % 7      = 2
            new_position = (item_position + item_offset) % modulo
            if new_position < item_position:
                new_position += 1
                for position in range(item_position, new_position, -1):
                    item = item_at_positions[(position-1) % modulo]
                    item_at_positions[position % modulo] = item
                    where_is_items[item] = position
                where_is_items[item_id] = new_position
                item_at_positions[new_position] = item_id
            else:
                for position in range(item_position, new_position):
                    item = item_at_positions[(position+1) % modulo]
                    item_at_positions[position % modulo] = item
                    where_is_items[item] = position
                where_is_items[item_id] = new_position
                item_at_positions[new_position] = item_id

        #print(item_at_positions)
        #print([item_offsets[item] for item in item_at_positions])

    position_of_zero = where_is_items[item_offsets.index(0)]
    print(item_offsets)
    print(item_offsets.index(0))
    print([item_offsets[item] for item in item_at_positions])
    print(position_of_zero)

    return sum(item_offsets[item_at_positions[(p+position_of_zero) % modulo]] for p in (1000, 2000, 3000))



def delete_index(d:deque, index:int):
    """
    """
    d.rotate(-index)
    d.popleft()
    d.rotate(index)


    
def scramble(mask:Iterable[Any], data:Deque[Tuple[int, Any]]) -> Deque[Tuple[int, Any]]:
    """mix up the data deque according to the mask in-place
       the data must be a enumeration of the mask"""
    N = len(data)-1
    result = data
    for item in enumerate(mask):
        x = item[1]
        if not x:
            continue
        p = result.index( item )
        new = (p+x)%N
        delete_index(result,p)
        result.insert(new,item)

    return result        



def decrypt(data:Iterable[int], key:int=1, mix:int=1, check:Iterable[int]=(1000,2000,3000)) -> int:
    original = [key*n for n in data]
    result = deque(enumerate(original))
    for _ in range(mix):
        result = scramble(original,result)
    message = [x for _, x in result]
    offset = message.index(0)
    M = len(message)    
    return sum( message[(p+offset)%M] for p in check)



def debug_part1a() -> int:
    """
    https://github.com/copperfield42/Advent-of-Code-2022/blob/main/day20/aoc_utils.py
    """
    return decrypt(parser())



def debug_part1b() -> int:
    """
    https://github.com/terminalmage/adventofcode/blob/main/2022/day20.py
    """
    data = list(parser())
    z = (data.index(0), 0)
    data = deque(enumerate(data))
    original_order = list(data)
    for item in original_order:
        data.rotate(-data.index(item))
        data.rotate(-data.popleft()[1])
        data.appendleft(item)

    z = data.index(z)
    return sum(data[(z+p)%len(data)][1] for p in (1000, 2000, 3000))



def part1() -> int:
    """
    What is the sum of the three numbers that form the grove coordinates?
    """
    data = parser()
    modulo = len(data)
    zero = (data.index(0), 0)
    message = deque(enumerate(data))
    original_order = list(enumerate(data))
    assert zero[0] == message.index(zero)
    for item in original_order:
        position = message.index(item)
        message.remove(item)
        # modulo minus one for the item we've just removed
        message.insert((position+item[1])%(modulo-1), item)

    z = message.index(zero)
    answer = [message[(z+p)%modulo][1] for p in (1000, 2000, 3000)]
    print(answer)
    return sum(answer)



def part2() -> int:
    """
    What is the sum of the three numbers that form the grove coordinates?
    """
    key = 811589153
    data = [a*key for a in parser()]
    z = (data.index(0), 0)
    data = deque(enumerate(data))
    original_order = list(data)
    for _ in range(10):
        for item in original_order:
            data.rotate(-data.index(item))
            data.rotate(-data.popleft()[1])
            data.appendleft(item)

    z = data.index(z)
    return sum(data[(z+p)%len(data)][1] for p in (1000, 2000, 3000))





if __name__ == "__main__":
    answer = part1()
    print(f"Part1 answer: {answer}")
    assert answer == 9687

    answer = part2()
    print(f"Part2 answer: {answer}")
    assert answer == 1338310513297
