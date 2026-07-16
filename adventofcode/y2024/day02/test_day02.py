"""Unit tests for 2024 Day 2 using AoC's published example."""

from adventofcode.y2024.day02.solution import part1, part2

EXAMPLE = """\
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""


def test_part1():
    assert part1(EXAMPLE) == 2


def test_part2():
    assert part2(EXAMPLE) == 4
