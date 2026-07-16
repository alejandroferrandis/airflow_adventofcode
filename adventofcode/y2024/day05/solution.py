"""Advent of Code 2024, Day 5 — Print Queue.

Ordering rules `X|Y` mean page X must precede page Y. Part 1 sums the middle
page of already-correct updates; part 2 reorders the incorrect ones (via a
rule-based comparator) and sums their middles.
"""

from __future__ import annotations

from collections.abc import Callable
from functools import cmp_to_key


def parse(data: str) -> tuple[set[tuple[int, int]], list[list[int]]]:
    rules_block, updates_block = data.strip().split("\n\n")
    rules = {(int(a), int(b)) for a, b in (line.split("|") for line in rules_block.splitlines())}
    updates = [[int(x) for x in line.split(",")] for line in updates_block.splitlines()]
    return rules, updates


def _comparator(rules: set[tuple[int, int]]) -> Callable[[int, int], int]:
    def compare(a: int, b: int) -> int:
        if (a, b) in rules:
            return -1
        if (b, a) in rules:
            return 1
        return 0

    return compare


def part1(data: str) -> int:
    rules, updates = parse(data)
    key = cmp_to_key(_comparator(rules))
    return sum(u[len(u) // 2] for u in updates if sorted(u, key=key) == u)


def part2(data: str) -> int:
    rules, updates = parse(data)
    key = cmp_to_key(_comparator(rules))
    total = 0
    for update in updates:
        ordered = sorted(update, key=key)
        if ordered != update:
            total += ordered[len(ordered) // 2]
    return total
