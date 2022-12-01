# This is just an example to get you started. A typical binary package
# uses this file as the main entry point of the application.

import std/algorithm   # sorted
import std/sequtils   # foldl
import std/sugar   # collect
import strutils   # parseInt



iterator reader(data: File): seq[int] =
  var elf: seq[int] = @[]
  for line in data.lines():
    if line == "":
      yield elf
      elf.setLen(0)
    else:
      elf.add(parseInt(line))



# Failed attempt of doing caloriesPerBag(reader(data)) as an iterator using an iterator.
type Iterable[T] = iterator: T

iterator caloriesPerBag(bags: Iterable[seq[int]]): int =
  for bag in bags:
    yield bag.foldl(a+b)



proc part1(): int =
  ## How many total Calories is that Elf carrying?
  let data = open("data")
  defer: data.close()

  let calories: seq[int] = collect(newSeq):
    for elf in reader(data):
      elf.foldl(a+b)

  return max(calories)



proc part2(): int =
  ## How many Calories are those Elves carrying in total?
  let data = open("data")
  defer: data.close()

  let calories = collect(newSeq):
    for bag in reader(data):
      bag.foldl(a+b)

  let most_calories = sorted(calories, system.cmp[int])[^3..^1]

  return most_calories.foldl(a+b)





when isMainModule:
  var answer = part1()
  assert(answer == 69289)
  echo "Part1:", answer

  answer = part2()
  assert(answer == 205615)
  echo "Part2:", answer
