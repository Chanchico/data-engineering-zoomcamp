# ex-003 — Verify and profile your ingested data (Hands-on)

**Module:** 01 — Docker & Terraform · **Section:** NY Taxi Dataset and Data Ingestion (`05-data-ingestion.md`)
**Type:** Hands-on · **Difficulty:** ★★★
**Common thread:** step 1 of the mini pipeline — *NYC Taxi ingestion → Postgres*

## Objective

Run the full ingestion on your machine and **prove** with queries that the data in Postgres matches the source file. Data quality checks are part of the job, not an extra.

## Context

Prerequisites: your Postgres container from the previous section is running (`root` / `root`, port `5432`, database `ny_taxi`), and your notebook from ex-002 works.

## Task

1. Make sure Postgres is up (`docker ps`) and run your idempotent ingestion cell from ex-002 on `yellow_tripdata_2021-01.csv.gz`.
2. In **pandas** (separately from the ingestion), compute from the source file the reference numbers:
   - total number of rows,
   - sum of `passenger_count` (ignore nulls),
   - earliest and latest `tpep_pickup_datetime`.

   Hint for memory: read the file in chunks again, don't load it at once.
3. In **pgcli**, run SQL queries giving the same four numbers from the `yellow_taxi_data` table. Compare.
4. Still in pgcli, answer these data questions on the table:
   - How many trips have `passenger_count = 0`?
   - How many trips have a pickup date **outside** January 2021? Show the earliest and latest ones.
   - What is the most frequent `payment_type`, and how many trips use it?
   - What is the largest `trip_distance`, and does it look realistic?
5. Run the ingestion cell a **second time**, then re-run your count. Compare it with your prediction from ex-001 question 5.
6. Save your reference numbers, your SQL queries and your observations in `practice/answers/ex-003.md`.

## Acceptance criteria

- [ ] Row count from pandas == row count from Postgres (about 1.37 million; give the exact number).
- [ ] The 4 reference numbers (pandas) and the 4 SQL results are in your answer file and match.
- [ ] The 4 data questions each have a query and a result.
- [ ] After the second run, the row count is unchanged, and you explain why (or fix your cell if it is not).
- [ ] At least **one data anomaly** is listed in your notes (weird date, zero passengers, extreme distance…) with a one-sentence opinion: should the ingestion step fix it, or should a later step handle it?

<details>
<summary>Hint 1 — reference numbers</summary>

You can accumulate counters while you loop over the chunks: `total += len(chunk)`, `pax += chunk["passenger_count"].sum()`, and track `min` / `max` of the datetime column.

</details>

<details>
<summary>Hint 2 — pgcli useful commands</summary>

`\dt` lists tables, `\d yellow_taxi_data` describes one, `\timing` shows query time. Remember `"PULocationID"`-style columns need double quotes because of capital letters.

</details>

<details>
<summary>Hint 3 — dates outside January</summary>

Use a `WHERE` on `tpep_pickup_datetime` with `<` and `>=` on literal timestamps, then `ORDER BY ... LIMIT`.

</details>
