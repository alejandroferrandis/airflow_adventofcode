# airflow_adventofcode

[Advent of Code](https://adventofcode.com) solutions, orchestrated by **Airflow 3**
on the homelab k8s cluster, gated by a **CI/CD quality pipeline**.

It's a learning vehicle for the full loop: write code in VS Code → push → CI +
SonarCloud gate → merge (manual accept) → Airflow git-syncs `main` → run/schedule.

## Flow

```
VS Code ─push─► PR ─► GitHub Actions gate: ruff · black · mypy · pytest   (blocks merge)
                            │
                      Gitar (AI review + auto-fix, CI-failure analysis) on the PR ──► Linear issues
                            │
              merge to main  ◄── manual acceptance (PR review)
                            │
                    Airflow (git-sync main) picks up the DAG
                            │
              task pod: cache-first input (Postgres) ─► run part1/part2 ─► store results
```

Only the `git push` leaves the homelab. Inputs and the AoC session cookie never do.

## Layout

```
adventofcode/
  common/
    aoc_client.py   # fetch puzzle input (session from AOC_SESSION env / k8s Secret)
    db.py           # Postgres: cache inputs + store results (reuses `lab_pg` creds)
    runner.py       # cache-first input, run both parts, persist, time them
  y2024/
    day01/
      solution.py   # pure part1(data)->answer, part2(data)->answer
      test_day01.py # unit test against AoC's PUBLISHED example (safe to commit)
dags/
  aoc_pipeline.py   # TaskFlow DAG, dynamic task mapping over implemented days
```

Year folders are `y2024` (not `2024`) because a Python module / Postgres schema
can't start with a digit. The Postgres schema names match: `adventofcode.y2024`.

## Data model (Postgres db `adventofcode`, schema per year)

| table        | columns                                                    |
|--------------|------------------------------------------------------------|
| `input_data` | `day, input_text, fetched_at`  — one cached input per day  |
| `results`    | `day, part, answer, runtime_ms, is_correct, computed_at`   |

## Adding a day

1. `adventofcode/y<year>/day<NN>/solution.py` with `part1(data: str)` /
   `part2(data: str)`.
2. `test_day<NN>.py` next to it asserting the answers for AoC's **example**
   input (never your real input).
3. Open a PR → the gate runs → merge → Airflow picks it up on the next git-sync.
4. Trigger `aoc_pipeline` with params `{"year": <year>, "days": [<NN>]}` (or run
   the whole year — only implemented days are mapped).

## ⚠️ Advent of Code etiquette (please respect)

- **Never commit puzzle inputs** — they're per-user; AoC asks they stay private.
  Inputs live in Postgres; `.gitignore` blocks stray input files.
- **Don't republish puzzle prose.** Solutions are fine; the puzzle text is not.
- **Fetch each input once.** `runner.py` is cache-first and the client sends a
  descriptive `User-Agent` (per AoC's automation guidelines).

## CI/CD

- **GitHub Actions** (`.github/workflows/ci.yml`) — free hosted runners run the
  deterministic gate: ruff, black, mypy, pytest. No token needed.
- **AI review** — [**Gitar**](https://gitar.ai) is installed as a GitHub App on
  this repo. It reviews/auto-fixes PRs and analyzes CI failures, validating its
  fixes against the CI above, and files issues to **Linear**. It runs on the PR;
  there's nothing to configure in this repo.
- **Deploy** — pull-based **git-sync**: Airflow's dag-processor tracks `main`.
  Merging a reviewed PR is the deployment; there is no push access from CI into
  the cluster.
- SonarQube Cloud static analysis (a separate Sonar product) can be added later
  as an extra gate if you want coverage/quality-gate metrics.
