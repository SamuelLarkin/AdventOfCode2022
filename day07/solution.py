#!/usr/bin/env  python3

from collections import namedtuple
from typing import (
        Dict,
        Generator,
        List,
        NamedTuple,
        TextIO,
        Tuple,
        )



def parser() -> Dict:
    """
    """
    def subparser(fin: TextIO, subfilesystem: Dict):
        """
        """
        for line in map(str.strip, fin):
            if line.startswith("$"):
                _, cmd, *arg = line.split()
                if cmd == "ls":
                    pass
                elif cmd == "cd":
                    _, cmd, directory_name = line.split()
                    if directory_name == "/":
                        pass
                    elif directory_name == "..":
                        return
                    else:
                        subparser(fin, subfilesystem[directory_name])
                else:
                    assert False, line
            elif line.startswith("dir"):
                _, directory_name = line.split()
                subfilesystem[directory_name] = {}
            else:
                size, filename = line.split()
                size = int(size)
                subfilesystem[filename] = size

    filesystem = {}
    with open("data", mode="r", encoding="UTF8") as fin:
        subparser(fin, filesystem)

    return filesystem



class DirectoryInfo(NamedTuple):
    size: int
    name: str



def visitor(subfilesystem: Dict, directory_sizes: List[DirectoryInfo]) -> int:
    """
    """
    total = 0
    for name, v in subfilesystem.items():
        if isinstance(v, dict):
            # Directory
            directory_size = visitor(v, directory_sizes)
            directory_sizes.append(DirectoryInfo(name=name, size=directory_size))
            total += directory_size
        elif isinstance(v, int):
            # File
            total += v
        else:
            assert False

    return total



def part1(atmost: int=100000) -> int:
    """
    Find all of the directories with a total size of at most 100000.
    What is the sum of the total sizes of those directories?
    """
    filesystem = parser()
    if False:
        import json
        print(json.dumps(filesystem, indent=2, ensure_ascii=False))

    directories = []
    visitor(filesystem, directories)

    directory_sizes = map(lambda d: d.size, directories)
    small_directories = filter(lambda size: size<=atmost, directory_sizes)
    return sum(small_directories)



def part2() -> int:
    """
    Find the smallest directory that, if deleted, would free up enough space on
    the filesystem to run the update.
    What is the total size of that directory?
    """
    FILESYSTEM_SIZE = 70_000_000
    MINIMUM_REQUIRED_SPACE = 30_000_000

    filesystem = parser()
    directories = []
    root_size = visitor(filesystem, directories)

    atleast = root_size - (FILESYSTEM_SIZE - MINIMUM_REQUIRED_SPACE)
    candidates = list(filter(lambda s: s.size>=atleast, directories))
    candidates.sort(key=lambda e: e.size)

    return candidates[0].size





if __name__ == "__main__":
    answer = part1()
    print(f"Part1 answer: {answer}")
    assert answer == 1611443

    answer = part2()
    print(f"Part2 answer: {answer}")
    assert answer == 2086088
