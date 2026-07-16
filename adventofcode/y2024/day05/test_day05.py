"""Unit tests for 2024 Day 5 using AoC's published example."""

from adventofcode.y2024.day05.solution import part1, part2

EXAMPLE = """\
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
"""


def test_part1():
    assert part1(EXAMPLE) == 143


def test_part2():
    assert part2(EXAMPLE) == 123
