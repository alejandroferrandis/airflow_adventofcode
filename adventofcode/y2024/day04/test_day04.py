"""Unit tests for 2024 Day 4 using AoC's published example."""

from adventofcode.y2024.day04.solution import part1, part2

EXAMPLE = """\
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
"""


def test_part1():
    assert part1(EXAMPLE) == 18


def test_part2():
    assert part2(EXAMPLE) == 9
