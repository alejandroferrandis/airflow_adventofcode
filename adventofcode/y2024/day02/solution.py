"""Advent of Code 2024, Day 2 — Red-Nosed Reports.

A report (a line of levels) is safe when the levels are strictly monotonic and
every adjacent step is between 1 and 3 inclusive. Part 2 adds the Problem
Dampener: a report also counts as safe if removing a single level makes it safe.
"""

from __future__ import annotations


def parse(data: str) -> list[list[int]]:
    return [[int(x) for x in line.split()] for line in data.strip().splitlines()]


def is_safe(levels: list[int]) -> bool:
    diffs = [b - a for a, b in zip(levels, levels[1:], strict=False)]
    return all(1 <= d <= 3 for d in diffs) or all(-3 <= d <= -1 for d in diffs)


def is_safe_dampened(levels: list[int]) -> bool:
    if is_safe(levels):
        return True
    return any(is_safe(levels[:i] + levels[i + 1 :]) for i in range(len(levels)))


def part1(data: str) -> int:
    return sum(is_safe(report) for report in parse(data))


def part2(data: str) -> int:
    return sum(is_safe_dampened(report) for report in parse(data))
