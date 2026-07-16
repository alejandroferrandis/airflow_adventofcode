"""Advent of Code pipeline (Airflow 3, TaskFlow + dynamic task mapping).

Trigger with params, e.g. {"year": 2024, "days": [1]} or leave defaults to run
every implemented day of the year. For each day it fans out one mapped task that
caches the input (fetch once, then Postgres), runs part1/part2 and stores results.

Deploy = git-sync from the repo's `main` branch; merging a PR is the promotion
gate. Nothing here needs a self-hosted runner.
"""

from __future__ import annotations

import pendulum
from airflow.decorators import dag, task


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
        """Keep only requested days that actually have a solution module.

        Layout-independent (works under git-sync, PVC, or installed package).
        """
        from adventofcode.common.discovery import implemented_days

        params = context["params"]
        return implemented_days(int(params["year"]), params["days"])

    @task
    def solve(item: dict) -> dict:
        from adventofcode.common.runner import run_day

        return run_day(item["year"], item["day"])

    solve.expand(item=list_days())


aoc_pipeline()
