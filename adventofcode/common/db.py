"""Postgres persistence for Advent of Code runs.

Layout: database `adventofcode`, one schema per year (`y2024`, `y2025`, ...),
each with two tables:
  * input_data(day, input_text, fetched_at)  -- one cached input per day
  * results(day, part, answer, runtime_ms, is_correct, computed_at)

Credentials are reused from the Airflow connection `lab_pg` (same server), we
just target the `adventofcode` database. Nothing here logs the password.
"""

from __future__ import annotations

import psycopg2

DB_NAME = "adventofcode"


def _conn() -> psycopg2.extensions.connection:
    # Imported lazily so pure-logic unit tests don't need Airflow installed.
    from airflow.hooks.base import BaseHook

    c = BaseHook.get_connection("lab_pg")
    return psycopg2.connect(
        host=c.host,
        port=c.port or 5432,
        user=c.login,
        password=c.password,
        dbname=DB_NAME,
    )


def ensure_schema(year: int) -> None:
    """Create the per-year schema and tables if a new year is added. Idempotent."""
    schema = f"y{year}"
    ddl = f"""
    CREATE SCHEMA IF NOT EXISTS {schema};
    CREATE TABLE IF NOT EXISTS {schema}.input_data (
        day        smallint PRIMARY KEY CHECK (day BETWEEN 1 AND 25),
        input_text text        NOT NULL,
        fetched_at timestamptz NOT NULL DEFAULT now()
    );
    CREATE TABLE IF NOT EXISTS {schema}.results (
        day         smallint NOT NULL CHECK (day BETWEEN 1 AND 25),
        part        smallint NOT NULL CHECK (part IN (1, 2)),
        answer      text,
        runtime_ms  numeric,
        is_correct  boolean,
        computed_at timestamptz NOT NULL DEFAULT now(),
        PRIMARY KEY (day, part)
    );
    """
    with _conn() as conn, conn.cursor() as cur:
        cur.execute(ddl)


def get_cached_input(year: int, day: int) -> str | None:
    with _conn() as conn, conn.cursor() as cur:
        cur.execute(f"SELECT input_text FROM y{year}.input_data WHERE day = %s", (day,))
        row = cur.fetchone()
        return row[0] if row else None


def store_input(year: int, day: int, text: str) -> None:
    with _conn() as conn, conn.cursor() as cur:
        cur.execute(
            f"""INSERT INTO y{year}.input_data (day, input_text) VALUES (%s, %s)
                ON CONFLICT (day) DO UPDATE
                SET input_text = EXCLUDED.input_text, fetched_at = now()""",
            (day, text),
        )


def store_result(year: int, day: int, part: int, answer: object, runtime_ms: float) -> None:
    with _conn() as conn, conn.cursor() as cur:
        cur.execute(
            f"""INSERT INTO y{year}.results (day, part, answer, runtime_ms) VALUES (%s, %s, %s, %s)
                ON CONFLICT (day, part) DO UPDATE
                SET answer = EXCLUDED.answer,
                    runtime_ms = EXCLUDED.runtime_ms,
                    computed_at = now()""",
            (day, part, str(answer), runtime_ms),
        )
