"""Advent of Code 2024, Day 4 — Ceres Search.

Part 1 counts every occurrence of XMAS in the grid across all 8 directions.
Part 2 counts X-MAS: two "MAS" (each forwards or backwards) crossing diagonally
on a shared central A.
"""

from __future__ import annotations

DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
WORD = "XMAS"
MS = {"M", "S"}


def part1(data: str) -> int:
    grid = data.strip().splitlines()
    rows, cols = len(grid), len(grid[0])

    def matches(r: int, c: int, dr: int, dc: int) -> bool:
        for i, ch in enumerate(WORD):
            nr, nc = r + dr * i, c + dc * i
            if not (0 <= nr < rows and 0 <= nc < cols) or grid[nr][nc] != ch:
                return False
        return True

    return sum(
        matches(r, c, dr, dc) for r in range(rows) for c in range(cols) for dr, dc in DIRECTIONS
    )


def part2(data: str) -> int:
    grid = data.strip().splitlines()
    rows, cols = len(grid), len(grid[0])
    count = 0
    for r in range(1, rows - 1):
        for c in range(1, cols - 1):
            if grid[r][c] != "A":
                continue
            diag1 = {grid[r - 1][c - 1], grid[r + 1][c + 1]}
            diag2 = {grid[r - 1][c + 1], grid[r + 1][c - 1]}
            if diag1 == MS and diag2 == MS:
                count += 1
    return count
