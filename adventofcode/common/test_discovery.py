"""Regression test: day discovery must skip unimplemented days without raising.

Uses a non-existent *year* for the missing case so the test stays valid as more
days of a real year get implemented.
"""

from adventofcode.common.discovery import has_solution, implemented_days


def test_implemented_day_is_found():
    assert has_solution(2024, 1) is True


def test_missing_returns_false_not_raises():
    # No solutions exist for 1999 — find_spec raises ModuleNotFoundError for the
    # missing parent package, which has_solution must swallow.
    assert has_solution(1999, 1) is False


def test_implemented_days_filters_out_missing():
    assert implemented_days(2024, [1]) == [{"year": 2024, "day": 1}]
    assert implemented_days(1999, [1, 2, 3]) == []
