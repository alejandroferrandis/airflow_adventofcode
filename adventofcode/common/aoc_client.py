"""Fetch puzzle input from adventofcode.com.

AoC automation etiquette (https://www.reddit.com/r/adventofcode/wiki/faqs/automation):
  * identify yourself in the User-Agent (repo URL + contact),
  * never fetch the same input more than once — the caller caches inputs in
    Postgres and only calls this on a cache miss.

The session token is read from the AOC_SESSION env var (injected into task pods
from the `aoc-session` k8s Secret). It is a credential and must never be logged
or committed.
"""

from __future__ import annotations

import os
import urllib.error
import urllib.request

BASE = "https://adventofcode.com"

# Identifies this automation to AoC as their guidelines request.
USER_AGENT = os.environ.get(
    "AOC_USER_AGENT",
    "github.com/alejandroferrandis/airflow_adventofcode by alejandro.ferrandis@marvalanalytics.com",
)


class AoCError(RuntimeError):
    """Raised when input cannot be fetched (missing session, HTTP error)."""


def fetch_input(year: int, day: int, session: str | None = None) -> str:
    """Download the raw puzzle input for (year, day). Trailing newline preserved."""
    session = session or os.environ.get("AOC_SESSION")
    if not session:
        raise AoCError("AOC_SESSION is not set (expected from k8s Secret 'aoc-session')")

    url = f"{BASE}/{year}/day/{day}/input"
    req = urllib.request.Request(
        url,
        headers={"Cookie": f"session={session}", "User-Agent": USER_AGENT},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:  # noqa: S310 (trusted host)
            return resp.read().decode()
    except urllib.error.HTTPError as exc:  # 400 = bad/expired cookie, 404 = puzzle not live yet
        raise AoCError(f"AoC returned HTTP {exc.code} for {year} day {day}") from exc
    except urllib.error.URLError as exc:
        raise AoCError(f"could not reach adventofcode.com: {exc.reason}") from exc
