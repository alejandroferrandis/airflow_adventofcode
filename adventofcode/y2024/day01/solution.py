"""Advent of Code 2024, Day 1 — Historian Hysteria.

Pure functions: each takes the raw puzzle input string and returns the answer.
No I/O here — that keeps them unit-testable against the published example.
"""

from __future__ import annotations

from collections import Counter


def parse(data: str) -> tuple[list[int], list[int]]:
    left: list[int] = []
    right: list[int] = []
    for line in data.strip().splitlines():
        a, b = line.split()
        left.append(int(a))
        right.append(int(b))
    return left, right


def part1(data: str) -> int:
    """Total distance: pair up sorted lists, sum absolute differences."""
    left, right = parse(data)
    return sum(abs(a - b) for a, b in zip(sorted(left), sorted(right), strict=True))


def part2(data: str) -> int:
    """Similarity score: each left value times its count in the right list."""
    left, right = parse(data)
    counts = Counter(right)
    return sum(value * counts[value] for value in left)
