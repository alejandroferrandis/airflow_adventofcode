"""Advent of Code 2024, Day 3 — Mull It Over.

Corrupted memory holds valid mul(X,Y) instructions among garbage. Part 1 sums
every valid multiplication. Part 2 adds do()/don't() toggles that enable or
disable the muls that follow; multiplication starts enabled.
"""

from __future__ import annotations

import re

MUL = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")
TOKEN = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don't\(\)")


def part1(data: str) -> int:
    return sum(int(a) * int(b) for a, b in MUL.findall(data))


def part2(data: str) -> int:
    total = 0
    enabled = True
    for match in TOKEN.finditer(data):
        token = match.group(0)
        if token == "do()":
            enabled = True
        elif token == "don't()":
            enabled = False
        elif enabled:
            total += int(match.group(1)) * int(match.group(2))
    return total
