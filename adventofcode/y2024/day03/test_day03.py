"""Unit tests for 2024 Day 3 using AoC's published examples."""

from adventofcode.y2024.day03.solution import part1, part2

EXAMPLE1 = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
EXAMPLE2 = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"


def test_part1():
    assert part1(EXAMPLE1) == 161


def test_part2():
    assert part2(EXAMPLE2) == 48
