"""Regression test: day discovery must skip unimplemented days without raising."""

from adventofcode.common.discovery import has_solution, implemented_days


def test_implemented_day_is_found():
    assert has_solution(2024, 1) is True


def test_missing_day_returns_false_not_raises():
    # day02 package does not exist — find_spec raises ModuleNotFoundError, which
    # has_solution must swallow.
    assert has_solution(2024, 2) is False


def test_implemented_days_filters_to_existing():
    assert implemented_days(2024, [1, 2, 3, 25]) == [{"year": 2024, "day": 1}]
