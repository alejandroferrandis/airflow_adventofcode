"""Unit tests for 2024 Day 1 using AoC's *published example* (safe to commit).

Never commit your real puzzle input — those are per-user and AoC asks that they
stay private. Real inputs live in Postgres, not in git.
"""

from adventofcode.y2024.day01.solution import part1, part2

EXAMPLE = """\
3   4
4   3
2   5
1   3
3   9
3   3
"""


def test_part1():
    assert part1(EXAMPLE) == 11


def test_part2():
    assert part2(EXAMPLE) == 31
