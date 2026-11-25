# DE Zoomcamp — Progress

## Current position
- Module: 01 — Docker & Terraform (`01-docker-terraform/`)
- Current section: Ingesting the NY Taxi data into Postgres (ingestion notebook done, script with arguments is next)
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

## Weak points to revisit
- Name the mechanism, not only the intuition (why `DtypeWarning`, why chunks: client RAM, single transaction).
- Idempotence: say *why* (table recreated with `replace`), not "same result each time". Also not atomic.
- Skipped small requirements in ex-002: total rows inserted not printed, URL not built with an f-string, file name not in a variable, `to_sql` written twice (`if i == 0`).
- Verify with `\d` in pgcli and write the expected count before running (ex-001).

## Exercises done
| # | Module | Topic | Result |
|---|--------|-------|--------|
| 001 | 01 | Why chunks, why explicit types (concept) | Partial: good intuitions, `head(0)` misunderstood, `\d` output missing |
| 002 | 01 | Fix the ingestion loop (code) | Validated by user. Exhausted-iterator bug found, `index=False`, idempotent, `tqdm`. Minor points left (see weak points) |
| 003 | 01 | Verify ingestion (hands-on) | Generated, not done yet |

## Common thread project
- Goal: a mini pipeline that grows with each module:
  NYC Taxi ingestion → Postgres → orchestration → warehouse → dbt → Spark → Kafka
- Status: started. Notebook (`practice/Untitled.ipynb`) loads yellow taxi 2021-01 (1,369,765 rows) into Postgres `yellow_taxi_data`, idempotent, config from `.env`. Next: turn it into a script with arguments, then Dockerize.
