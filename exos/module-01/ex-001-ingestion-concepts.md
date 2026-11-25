# ex-001 — Why chunks, why explicit types? (Concept check)

**Module:** 01 — Docker & Terraform · **Section:** NY Taxi Dataset and Data Ingestion (`05-data-ingestion.md`)
**Type:** Concept check · **Difficulty:** ★☆☆

## Objective

Check that you understand *why* the ingestion notebook is written the way it is, not just *how*.

## Context

In the tutorial you read `yellow_tripdata_2021-01.csv.gz` with `dtype=...`, `parse_dates=...`, `iterator=True` and `chunksize=100000`. You then created the table with `head(0)` and appended the chunks.

## Task

Answer in a file `practice/answers/ex-001.md` (short answers, 2–4 sentences each):

1. Without `dtype`, pandas raised a `DtypeWarning` on column 6 (`store_and_fwd_flag`) when reading the full file. Why does it happen with the full file but not with `nrows=100`? Why is it a problem for a database load, even though it is "only a warning"?
2. What is the benefit of `chunksize=100000` over `pd.read_csv(...)` followed by a single `to_sql`? Name two concrete things that could go wrong with the single-shot approach on a much larger file (e.g. a full year of data).
3. Why do we create the table with `df.head(n=0).to_sql(..., if_exists="replace")` and not by inserting the first chunk directly with `if_exists="replace"`? What would happen to the table after the second chunk if we kept `replace` in the loop?
4. `to_sql` with its default arguments added a column to your table that is not in the CSV. Which one, and where does it come from? (Look at the table in pgcli with `\d yellow_taxi_data` to confirm.)
5. You re-run the whole ingestion cell twice by mistake. With the loop from the tutorial, what is the row count in the table after the second run, and why? Is this behaviour **idempotent**?

## Acceptance criteria

- [ ] All 5 questions answered in your own words.
- [ ] Question 4 is confirmed by looking at the real table, not guessed.
- [ ] For question 5, you state the exact count you expect before running anything (then you may check it in ex-003).

<details>
<summary>Hints</summary>

- Q1: how does pandas infer a column's type when it reads a file by blocks internally?
- Q3: what does `replace` do to a table that already exists?
- Q4: look at the signature of `DataFrame.to_sql` — which parameter defaults to `True`?
- Q5: January 2021 contains roughly 1.37 million rows.

</details>
