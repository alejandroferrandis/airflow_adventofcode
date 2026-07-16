"""Discover which puzzle days have a solution module.

Kept as pure functions (no Airflow) so the DAG's day-selection logic is unit
tested in CI — importlib.util.find_spec RAISES ModuleNotFoundError when a
parent package (e.g. an unimplemented dayNN) is missing, rather than returning
None, so that case must be handled explicitly.
"""

from __future__ import annotations

import importlib.util
from collections.abc import Iterable


def has_solution(year: int, day: int) -> bool:
    module = f"adventofcode.y{year}.day{day:02d}.solution"
    try:
        return importlib.util.find_spec(module) is not None
    except ModuleNotFoundError:
        return False


def implemented_days(year: int, days: Iterable[int]) -> list[dict]:
    """Return [{year, day}, ...] for the requested days that have a solution."""
    return [
        {"year": year, "day": day}
        for day in sorted({int(d) for d in days})
        if has_solution(year, day)
    ]
