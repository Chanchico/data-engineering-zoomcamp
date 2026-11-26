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
- **Explaining "why"**: when asked why something happens, describe what the tool actually does. Example: `DtypeWarning` happens because pandas guesses the type of each internal block of the file separately, and the blocks disagree. "It can cause a problem" is not enough.
- **Idempotence**: running twice must give the same table. Here it works because `replace` drops and recreates the table at the start. Without it, `append` would double the rows. "It gives the same result" is not an explanation.
- **Read the whole statement before saying done**: in ex-002 two requirements were forgotten (print the total rows inserted, build the URL with an f-string). Tick each acceptance criterion one by one.
- **Check, don't assume**: write the expected row count before running, then check the table schema with `\d yellow_taxi_data` in pgcli (ex-001 had a `COUNT(*)` instead).

## Exercises done
| # | Module | Topic | Result |
|---|--------|-------|--------|
| 001 | 01 | Why chunks, why explicit types (concept) | Partial: good intuitions, `head(0)` misunderstood, `\d` output missing |
| 002 | 01 | Fix the ingestion loop (code) | Validated. Bug found, `index=False`, idempotent, `tqdm`, no duplicated `to_sql`, total rows checked against `COUNT(*)`, f-string URL. Minor: total printed inside the loop instead of at the end |
| 003 | 01 | Verify ingestion (hands-on) | Generated, not done yet |

## Common thread project
- Goal: a mini pipeline that grows with each module:
  NYC Taxi ingestion → Postgres → orchestration → warehouse → dbt → Spark → Kafka
- Status: started. Notebook (`practice/Untitled.ipynb`) loads yellow taxi 2021-01 (1,369,765 rows) into Postgres `yellow_taxi_data`, idempotent, config from `.env`. Next: turn it into a script with arguments, then Dockerize.
