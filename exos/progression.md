# DE Zoomcamp — Progress

## Current position
- Module: 01 — Docker & Terraform (`01-docker-terraform/`)
- Current section: Ingesting the NY Taxi data into Postgres (ingestion notebook done and verified, script with arguments is next)
- Last section completed: Exploring the NY Taxi dataset

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

## Weak points to revisit
- **Explaining "why"**: when asked why something happens, describe what the tool actually does. Example: `DtypeWarning` happens because pandas guesses the type of each internal block of the file separately, and the blocks disagree. "It can cause a problem" is not enough. (ex-003: the idempotence explanation needed 3 attempts before naming the mechanism.)
- **Idempotence vs configuration**: idempotence = same operation on the **same target** gives the same final state. Changing the `.env` (another database) is a different target and a different topic (configuration / portability).
- **Read the whole statement before saying done**: in ex-002 two requirements were forgotten; in ex-003 the first submission had the wrong metric (count of non-nulls instead of `SUM`), an inverted "outside January" query, and no stated opinion on the anomaly. Tick each acceptance criterion one by one.
- **Check, don't assume**: write the expected value before running (ex-001 prediction was missing), and sanity-check a result (a count equal to the whole table means the filter filters nothing). Still to do: `\d yellow_taxi_data` output in pgcli (ex-001).
- **Units and domain facts**: `trip_distance` is in miles, not feet. Check the data dictionary before judging a value.
- **Take a position**: when asked for an opinion, decide and justify ("it depends" is not an answer).

## Exercises done
| # | Module | Topic | Result |
|---|--------|-------|--------|
| 001 | 01 | Why chunks, why explicit types (concept) | Partial: good intuitions, `head(0)` misunderstood, `\d` output missing |
| 002 | 01 | Fix the ingestion loop (code) | Validated. Bug found, `index=False`, idempotent, `tqdm`, no duplicated `to_sql`, total rows checked against `COUNT(*)`, f-string URL. Minor: total printed inside the loop instead of at the end |
| 003 | 01 | Verify ingestion (hands-on) | Validated after corrections (2 rounds). pandas == SQL on 4 reference numbers (1,369,765 rows; `SUM` 1,794,610; min 2008-12-31; max 2021-02-22), 24 trips outside January, idempotence proven (count unchanged after 2nd run) and explained. Minor: stale table label, evasive opinion on the anomaly, whole file read at once instead of chunks |

## Common thread project
- Goal: a mini pipeline that grows with each module:
  NYC Taxi ingestion → Postgres → orchestration → warehouse → dbt → Spark → Kafka
- Status: started. Notebook (`practice/Untitled.ipynb`) loads yellow taxi 2021-01 (1,369,765 rows) into Postgres `yellow_taxi_data`, idempotent, config from `.env`. Load verified against the source (ex-003). Known anomalies kept raw on purpose: 24 trips outside January 2021 (earliest 2008-12-31), 26,726 trips with 0 passengers, 98,352 NULL `payment_type`, max `trip_distance` 263,163 miles. Next: turn the notebook into a script with arguments, then Dockerize.
