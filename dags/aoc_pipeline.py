"""Advent of Code pipeline (Airflow 3, TaskFlow + dynamic task mapping).

Trigger with params, e.g. {"year": 2024, "days": [1]} or leave defaults to run
every implemented day of the year. For each day it fans out one mapped task that
caches the input (fetch once, then Postgres), runs part1/part2 and stores results.

Deploy = git-sync from the repo's `main` branch; merging a PR is the promotion
gate. Nothing here needs a self-hosted runner.
"""

from __future__ import annotations

from pathlib import Path

import pendulum
from airflow.decorators import dag, task

# Repo root is one level up from dags/ (git-sync checks out the whole repo).
REPO_ROOT = Path(__file__).resolve().parent.parent


@dag(
    dag_id="aoc_pipeline",
    schedule=None,
    start_date=pendulum.datetime(2024, 12, 1, tz="UTC"),
    catchup=False,
    tags=["adventofcode"],
    params={"year": 2024, "days": list(range(1, 26))},
    doc_md=__doc__,
)
def aoc_pipeline():
    @task
    def list_days(**context) -> list[dict]:
        """Keep only requested days that actually have a solution module."""
        params = context["params"]
        year = int(params["year"])
        requested = sorted({int(d) for d in params["days"]})
        year_dir = REPO_ROOT / "adventofcode" / f"y{year}"
        return [
            {"year": year, "day": day}
            for day in requested
            if (year_dir / f"day{day:02d}" / "solution.py").exists()
        ]

    @task
    def solve(item: dict) -> dict:
        from adventofcode.common.runner import run_day

        return run_day(item["year"], item["day"])

    solve.expand(item=list_days())


aoc_pipeline()
