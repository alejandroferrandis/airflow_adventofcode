"""Glue: fetch-or-cache the input, run both parts of a day, persist results.

Kept separate from the solution modules (which are pure functions) so the
puzzle logic stays trivially unit-testable without a DB or network.
"""

from __future__ import annotations

import importlib
import time


def run_day(year: int, day: int) -> dict:
    """Run day `day` of `year`: cache-first input, run part1/part2, store results.

    Returns a small summary dict (also pushed to XCom by the DAG task).
    Raises ModuleNotFoundError if the day has no solution yet — the DAG turns
    that into a skip.
    """
    from adventofcode.common import aoc_client, db

    db.ensure_schema(year)

    text = db.get_cached_input(year, day)
    if text is None:
        text = aoc_client.fetch_input(year, day)
        db.store_input(year, day, text)

    module = importlib.import_module(f"adventofcode.y{year}.day{day:02d}.solution")

    summary: dict[str, dict] = {}
    for part in (1, 2):
        fn = getattr(module, f"part{part}", None)
        if fn is None:
            continue
        started = time.perf_counter()
        answer = fn(text)
        runtime_ms = round((time.perf_counter() - started) * 1000, 3)
        db.store_result(year, day, part, answer, runtime_ms)
        summary[f"part{part}"] = {"answer": str(answer), "runtime_ms": runtime_ms}

    return {"year": year, "day": day, **summary}
