#!/usr/bin/env  python3

from dataclasses import dataclass
from typing import (
        Callable,
        Dict,
        Generator,
        Union,
        )



@dataclass
class OpBinary:
    left: int
    right: int



@dataclass
class OpAddition(OpBinary):
    op: Callable[[int, int], int] = lambda a, b: a+b
    op_inv: Callable[[int, int], int] = lambda a, b: a-b



@dataclass
class OpSubstraction(OpBinary):
    op: Callable[[int, int], int] = lambda a, b: a-b
    op_inv: Callable[[int, int], int] = lambda a, b: a+b



@dataclass
class OpMultiply(OpBinary):
    op: Callable[[int, int], int] = lambda a, b: a*b
    op_inv: Callable[[int, int], int] = lambda a, b: a//b



@dataclass
class OpDivide(OpBinary):
    op: Callable[[int, int], int] = lambda a, b: a//b
    op_inv: Callable[[int, int], int] = lambda a, b: a*b



@dataclass
class OpEqual(OpBinary):
    op: Callable[[int, int], int] = lambda a, b: a or b
    op_inv: Callable[[int, int], int] = lambda a, b: a or b



Node = Union[OpBinary, int]



def parser(data: str="data") -> Generator[Tuple[str, Node], None, None]:
    """
    """
    with open(data, mode="r", encoding="UTF8") as fin:
        for line in map(str.strip, fin):
            name, *args = line.split()
            name = name[:-1]
            if len(args) == 1:
                operation = int(args[0])
            elif len(args) == 3:
                left, op, right = args
                assert len(left) == 4
                assert len(right) == 4
                if op == "+":
                    operation = OpAddition(left=args[0], right=args[2])
                elif op == "-":
                    operation = OpSubstraction(left=args[0], right=args[2])
                elif op == "*":
                    operation = OpMultiply(left=args[0], right=args[2])
                elif op == "/":
                    operation = OpDivide(left=args[0], right=args[2])
                else:
                    assert False, line
            else:
                assert False, line

            yield (name, operation)



def evaluate(node_name: str, tree: Dict[str, Node]) -> int:
    """
    """
    node = tree[node_name]
    if isinstance(node, int):
        return node
    else:
        return int(node.op(evaluate(node.left, tree), evaluate(node.right, tree)))



def part1(data: str="data") -> int:
    """
    What number will the monkey named root yell?
    """
    tree = dict(parser(data))
    #print(*tree.items(), sep="\n")

    return evaluate("root", tree)



def solver(node_name: str, tree: Dict[str, Node]):
    """
    """
    node = tree[node_name]
    if isinstance(node, OpBinary):
        return node.op(solver(node.left, tree), solver(node.right, tree))
    else:
        return node



def part2(data: str="data") -> int:
    """
    What number do you yell to pass root's equality test?
    """
    from sympy.solvers import solve
    from sympy import Symbol

    tree = dict(parser(data))
    x = Symbol('x')
    tree["humn"] = x
    root = tree["root"]
    return int(solve(solver(root.left, tree) - solver(root.right, tree), x)[0])



def part2b(data: str="data") -> int:
    """
    My initial though was to start from the root then try to solve the left and
    right branches.  Only the branch that contains no variable would evaluate.
    Given that, rebalance the tree so that the failed branch's node becomes the
    root.  Its arguments are update to be `(operator, left, constant inv_op
    right)`.  In other words, one branch is constant, the other is variable,
    keep the variable on one side and move all constants on the other side.
    """
    def evaluate(node_name: str, tree: Dict[str, Node]) -> int:
        """
        """
        if node_name == "humn":
            # This mark the fact that we've found the variable.
            assert False

        node = tree[node_name]
        if isinstance(node, int):
            return node
        else:
            return int(node.op(evaluate(node.left, tree), evaluate(node.right, tree)))

    def solver(node_name: str, tree: Dict[str, Node], result: int) -> int:
        """
        """
        if node_name == "humn":
            return result

        node = tree[node_name]
        if isinstance(node, OpBinary):
            try:
                value = evaluate(node.right, tree)
                return solver(node.left, tree, node.op_inv(result, value))
            except:
                value = evaluate(node.left, tree)
                if isinstance(node, OpDivide):
                    return solver(node.right, tree, node.op_inv(value, result))
                elif isinstance(node, OpSubstraction):
                    return solver(node.right, tree, -node.op(result, value))
                else:
                    return solver(node.right, tree, node.op_inv(result, value))
        else:
            return node

    def alter_tree(tree: Dict[str, OpBinary]) -> Dict[str, OpBinary]:
        """
        """
        node = tree["root"]
        tree["root"] = OpEqual(left=node.left, right=node.right)
        return tree

    tree = alter_tree(dict(parser(data)))
    return solver("root", tree, 0)





if __name__ == "__main__":
    assert (answer := part1("test")) == 152, answer
    answer = part1()
    print(f"Part1 answer: {answer}")
    assert answer == 54_703_080_378_102

    assert (answer := part2b("test")) == 301, answer
    assert (answer := part2b()) == 3_952_673_930_912, answer

    assert (answer := part2("test")) == 301, answer
    answer = part2()
    print(f"Part2 answer: {answer}")
    assert answer == 3_952_673_930_912
