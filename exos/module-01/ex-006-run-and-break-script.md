# ex-006 — Run your script, then try to break it (Hands-on)

**Module:** 01 — Docker & Terraform · **Section:** Creating the Data Ingestion Script (`06-ingestion-script.md`)
**Type:** Hands-on · **Difficulty:** ★★★
**Common thread:** step 2 of the mini pipeline — validate the script before Dockerizing it

## Objective

Prove that your `practice/ingest_data.py` (ex-005) gives exactly the same table as your notebook, behaves idempotently, and fails safely.

## Context

Prerequisites: ex-005 is done, your Postgres container is running (`root` / `root`, port `5432`, database `ny_taxi`), and the table `yellow_taxi_data` from the notebook still exists (1,369,765 rows). It is your **reference table**: do not overwrite it during this exercise.

## Task

1. **Prediction first.** In `practice/answers/ex-006.md`, write what you expect **before** running: row count of the new table after step 2, and what `\d` will show compared with the reference table.
2. Run the script on January 2021 into a **new table**, from the command line, with explicit arguments, for example `--target-table=yellow_taxi_check`.
3. **Compare with the reference.** In pgcli:
   - `\d yellow_taxi_data` and `\d yellow_taxi_check`: paste both outputs and state whether the columns and types are identical.
   - `COUNT(*)` on both tables.
   - A query proving that the **content** is the same, not only the count (for example `SUM(total_amount)` and `SUM(passenger_count)` on both, or a set operation between the two tables). Explain why a matching count alone is not enough.
4. **Idempotence.** Run the exact same command a second time. Re-run the count. Explain which line of your script keeps the count unchanged (mechanism, not "it gives the same result").
5. **Another month.** Before running, guess the order of magnitude of the row count of February 2021. Then run `--month=2 --target-table=yellow_taxi_feb` and check the real count. Was your guess right?
6. **Break it.** Run the script with a month that does not exist as a file (for example `--month=13` or `--year=2099`). Observe:
   - the error message and the **exit code**,
   - the state of the target table afterwards. Was it left intact, empty, or missing? Explain *why*, by looking at **when** your script calls `to_sql` relative to the download.
7. **Clean up.** Drop the two test tables `yellow_taxi_check` and `yellow_taxi_feb` (keep `yellow_taxi_data`). Write the `DROP` statements and the output of `\dt` in your answer file.

## Acceptance criteria

- [ ] The prediction of step 1 is written **before** the results, and the actual results are compared with it.
- [ ] Both `\d` outputs are pasted and the comparison is stated (no `index` column in either).
- [ ] Count and content checks on both tables match, with a sentence on why content matters.
- [ ] After the second run, the count is unchanged and the explanation names the mechanism.
- [ ] February: guess and real count are both reported.
- [ ] The failing run: error message, exit code and table state are reported, with an explanation.
- [ ] Final `\dt` shows `yellow_taxi_data` still there and the two test tables gone.
- [ ] Everything is saved in `practice/answers/ex-006.md` (queries, outputs, observations).

<details>
<summary>Hint 1 — running with arguments</summary>

From the `practice/` folder: `uv run python ingest_data.py --target-table=yellow_taxi_check`. Add options one by one with `--option=value`.

</details>

<details>
<summary>Hint 2 — comparing content</summary>

Aggregates (`SUM`, `MIN`, `MAX`) on a few numeric columns of both tables are a cheap content check. In pandas you can also compare a checksum of the two dataframes, but SQL is enough here.

</details>

<details>
<summary>Hint 3 — exit code in PowerShell</summary>

After the command, print `$LASTEXITCODE`. In bash, it is `echo $?`.

</details>
