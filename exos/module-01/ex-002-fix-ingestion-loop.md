# ex-002 — Fix the ingestion loop (Code exercise)

**Module:** 01 — Docker & Terraform · **Section:** NY Taxi Dataset and Data Ingestion (`05-data-ingestion.md`)
**Type:** Code exercise · **Difficulty:** ★★☆

## Objective

Write a safer, re-runnable ingestion loop, and spot bugs in a loop you did not write.

## Context

A colleague wrote this notebook cell to load the data:

```python
df_iter = pd.read_csv(
    prefix + "yellow_tripdata_2021-01.csv.gz",
    dtype=dtype,
    parse_dates=parse_dates,
    iterator=True,
    chunksize=100000,
)

for df_chunk in df_iter:
    print(len(df_chunk))

df_chunk.head(0).to_sql(name="yellow_taxi_data", con=engine, if_exists="replace")

for df_chunk in df_iter:
    df_chunk.to_sql(name="yellow_taxi_data", con=engine, if_exists="append")
    print("Inserted:", len(df_chunk))
```

It runs without any error, yet the table ends up with **almost no data**.

## Task

1. **Find the bug(s).** In a markdown cell, explain what each line does to `df_iter` and why the table is (nearly) empty. Hint on the scale of the problem: how many rows are in the table after this cell runs?
2. **Rewrite the cell** in your notebook (`practice/`) so that it:
   - creates the table schema from the first chunk (no data), then inserts **all** chunks, including the first one,
   - uses `tqdm` to show progress,
   - prints the number of rows inserted at the end (sum over chunks),
   - does **not** create the extra `index` column in Postgres,
   - can be run several times in a row and always leaves the table with the same content (idempotent).
3. Wrap the connection parameters (`user`, `password`, `host`, `port`, `db`) and the file name in **variables** at the top of the cell and build the URL and the engine from them with an f-string. No hardcoded `localhost` / `root` inside the `create_engine(...)` call.

> Stay in the notebook: turning this into a script with arguments comes in the next section.

## Acceptance criteria

- [ ] The explanation of the bug names the exhausted iterator and says what `df_chunk` contains at the `head(0)` line.
- [ ] Running your cell twice in a row gives the same `SELECT COUNT(*) FROM yellow_taxi_data;` both times.
- [ ] `\d yellow_taxi_data` in pgcli shows **no** `index` column.
- [ ] The total printed by your cell equals the count returned by Postgres.
- [ ] Your cell contains no duplicated `to_sql(...)` code for the first chunk vs. the other chunks, **or** you can justify why you kept the two-step approach.

<details>
<summary>Hint 1 — the bug</summary>

A pandas iterator can be consumed only once. After the first `for` loop, what is left in `df_iter`? And what is `df_chunk` after the loop finishes?

</details>

<details>
<summary>Hint 2 — the index column</summary>

Look at the `index` parameter of `to_sql`.

</details>

<details>
<summary>Hint 3 — idempotence</summary>

Two options are possible: recreate the table at each run (which operation of the tutorial does that?), or truncate it first. Think about which one also protects you if the schema changes.

</details>
