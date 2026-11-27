# DE Zoomcamp — Progress

## Plan (13 weeks, 2026-11-27 → 2027-02-26, ~5 h/day, 1 day off/week)
Daily: ~3 h tutorial (coding along) + ~45 min exercise + ~45 min SQL drill.

| Week | Start | Content | Status |
|------|-------|---------|--------|
| S1 | 2026-11-27 | Module 01, sections 07–13 + exam-01 | in progress |
| S2 | 2026-12-04 | Module 02 — Workflow orchestration + exam | |
| S3 | 2026-12-11 | Module 03 — Data warehouse + exam | |
| S4 | 2026-12-18 | Module 04 — Analytics engineering (dbt) + exam | |
| S5 | 2026-12-25 | Module 05 — Data platforms + exam | |
| S6 | 2027-01-01 | Modules 06 (batch) & 07 (streaming) + exams | |
| S7–S11 | 2027-01-08 | Kubernetes: deploy the common thread pipeline on kind/minikube + exam | |
| S12–S13 | 2027-02-12 | Final project: pipeline end-to-end on Kubernetes, documented on GitHub | |

Targets: course finished, SQL solid (CTEs, window functions, query plans), Kubernetes **operational** (Deployments, Services, ConfigMaps, Secrets, Jobs, `kubectl` debugging, Helm basics). If a week slips, cut exercise depth, not the course.

## Current position
- Module: 01 — Docker & Terraform (`01-docker-terraform/`)
- Current section: 07 — pgAdmin
- Last section completed: 06 — Creating the data ingestion script
- SQL drills: not started (next: sql-001)

## Acquired
- Why Docker (isolation, reproducibility)
- Creating a simple "data pipeline" in Docker (Dockerfile, build, run)
- Running Postgres locally with Docker (env vars, volumes, port mapping)
- Using pgcli to connect to the database
- Chunked ingestion with `pd.read_csv(..., chunksize=...)` and `to_sql` (`replace` then `append`, `index=False`)
- A pandas `TextFileReader` is a one-shot iterator: it is exhausted after one loop, and `next()` gets the first chunk
- Explicit `dtype` / `parse_dates` to avoid `DtypeWarning`
- Connection settings from environment variables (`os.environ`, `python-dotenv`)
- Progress display with `tqdm` (`tqdm.auto`, `total` needed for a real bar)
- Verifying a load: compare pandas reference numbers (row count, `SUM`, min/max date) with SQL results (`COUNT`, `SUM`, `MIN`, `MAX`)
- SQL filters: "outside a range" = `< start OR >= end` (not `AND`); several aggregates in one `SELECT`, no `JOIN` needed
- Profiling data quality in SQL (zero passengers, dates outside the month, NULL `payment_type`, extreme `trip_distance`)
- Idempotence mechanism: `replace` on the first chunk = `DROP` + `CREATE`, so the later `append`s start from an empty table
- Ingest raw, clean downstream: ingestion should stay faithful to the source
- Notebook → script: no Jupyter server, runs top to bottom (no hidden state), can be run by Docker/cron/orchestrator
- `if __name__ == '__main__'`: `__name__` is `'__main__'` for the entry file, the module name when imported; `import` runs all module-level code (proven with experiments)
- `to_sql` without `index=False` adds an `index` column + B-tree index; checked with `\d <table>` in pgcli
- `click` options for the script, defaults taken from `.env`

## Weak points to revisit
- **Explaining "why"**: when asked why something happens, describe what the tool actually does. Example: `DtypeWarning` happens because pandas guesses the type of each internal block of the file separately, and the blocks disagree. "It can cause a problem" is not enough. (ex-003: the idempotence explanation needed 3 attempts before naming the mechanism.)
- **Idempotence vs configuration**: idempotence = same operation on the **same target** gives the same final state. Changing the `.env` (another database) is a different target and a different topic (configuration / portability). **Repeated in ex-004 Q5**: said different arguments "break idempotency", and named the `append` line instead of the first-chunk `replace` line as the one that decides it.
- **Read what a parameter does in the code before predicting**: ex-004 Q5 assumed `--month` filters rows, while it selects which file is downloaded (`url = f'.../yellow_tripdata_{year}-{month:02d}.csv.gz'`). Also remember the reference number: January 2021 = 1,369,765 rows (not 1,369,740).
- **Security reasoning**: a password on the command line is visible to all users via `ps` / `/proc/<pid>/cmdline` while running, and in shell history. Prefer `.env` because it stays out of history, process list and Git (git-ignored), not because it is "quick".
- **Time management**: exercises took ~2 days each. Respect the time budget, rabbit holes (ex-004 Q2 self-import experiments) are fine only within it.
- **Read the whole statement before saying done**: in ex-002 two requirements were forgotten; in ex-003 the first submission had the wrong metric (count of non-nulls instead of `SUM`), an inverted "outside January" query, and no stated opinion on the anomaly. Tick each acceptance criterion one by one.
- **Check, don't assume**: write the expected value before running (ex-001 prediction was missing), and sanity-check a result (a count equal to the whole table means the filter filters nothing).
- **Units and domain facts**: `trip_distance` is in miles, not feet. Check the data dictionary before judging a value.
- **Take a position**: when asked for an opinion, decide and justify ("it depends" is not an answer).

## Exercises done
| # | Module | Topic | Result |
|---|--------|-------|--------|
| 001 | 01 | Why chunks, why explicit types (concept) | Partial: good intuitions, `head(0)` misunderstood, `\d` output missing |
| 002 | 01 | Fix the ingestion loop (code) | Validated. Bug found, `index=False`, idempotent, `tqdm`, no duplicated `to_sql`, total rows checked against `COUNT(*)`, f-string URL. Minor: total printed inside the loop instead of at the end |
| 003 | 01 | Verify ingestion (hands-on) | Validated after corrections (2 rounds). pandas == SQL on 4 reference numbers (1,369,765 rows; `SUM` 1,794,610; min 2008-12-31; max 2021-02-22), 24 trips outside January, idempotence proven (count unchanged after 2nd run) and explained. Minor: stale table label, evasive opinion on the anomaly, whole file read at once instead of chunks |
| 004 | 01 | Notebook → script (concept) | Partial, closed. Q1, Q2 (`__name__`, with experiments), Q4 (`index` column via `\d`) good. Q3 right risk but weak justification, missed `ps`. Q5 wrong: `--month` misread as a filter, final table = February only (first-chunk `replace`), idempotence confused with configuration. Q5 goes into exam-01 |
| 005–006 | 01 | Write / run the ingestion script | Dropped with the new fast-paced format: `practice/ingestion.py` already works with `click` arguments |

## Common thread project
- Goal: a mini pipeline that grows with each module:
  NYC Taxi ingestion → Postgres → orchestration → warehouse → dbt → Spark → Kafka
- Status: script stage. Notebook `practice/ingestion.ipynb` converted to `practice/ingestion.py` (`click` options, defaults from `.env`). It loads yellow taxi 2021-01 (1,369,765 rows) into Postgres `yellow_taxi_data`, idempotent, config from `.env`. Load verified against the source (ex-003). Known anomalies kept raw on purpose: 24 trips outside January 2021 (earliest 2008-12-31), 26,726 trips with 0 passengers, 98,352 NULL `payment_type`, max `trip_distance` 263,163 miles. Gap: `click` missing from `pyproject.toml`. Next: Dockerize the script (section 08), then docker-compose (section 09). Final target: the whole pipeline on Kubernetes (S7–S13).
