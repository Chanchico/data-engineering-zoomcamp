# ex-005 — Write your ingestion script with `click` (Code exercise)

**Module:** 01 — Docker & Terraform · **Section:** Creating the Data Ingestion Script (`06-ingestion-script.md`)
**Type:** Code exercise · **Difficulty:** ★★☆
**Common thread:** step 2 of the mini pipeline — *notebook → script with arguments*

## Objective

Turn your notebook (`practice/Untitled.ipynb`) into a standalone script `practice/ingest_data.py` that takes its settings from the command line, keeping everything you already acquired: idempotence, explicit types, progress bar, total check.

## Context

The tutorial shows the `click` structure and the course repo has a reference script. Do **not** copy it blindly: it lacks things you already do in your notebook (see ex-004, question 4). Your script must be at least as good as your notebook.

`click` is not yet in your `practice/pyproject.toml` dependencies.

## Task

Create `practice/ingest_data.py`:

1. Add the dependency the right way with `uv` (do not `pip install`). Check that `pyproject.toml` changed.
2. A `click` command with these options and defaults:

   | Option | Type | Default |
   |--------|------|---------|
   | `--pg-user` | str | `root` |
   | `--pg-pass` | str | read from the `DB_PASSWORD` environment variable, **no hard-coded password in the code** |
   | `--pg-host` | str | `localhost` |
   | `--pg-port` | int | `5432` |
   | `--pg-db` | str | `ny_taxi` |
   | `--year` | int | `2021` |
   | `--month` | int | `1` |
   | `--target-table` | str | `yellow_taxi_data` |
   | `--chunksize` | int | `100000` |

3. Build the file URL **with an f-string** from `--year` and `--month` (file names look like `yellow_tripdata_2021-01.csv.gz`: month on 2 digits).
4. Reuse your logic from the notebook: `dtype`, `parse_dates`, chunked reading, `replace` on the first chunk then `append`, `index=False`, `tqdm` progress bar.
5. At the **end** of the run (not inside the loop), print the total number of rows inserted, then compare it with `SELECT COUNT(*)` on the target table and print `OK` or `MISMATCH`. If it is a mismatch, the script must exit with a **non-zero** code.
6. The script must be importable without running the ingestion (`if __name__ == '__main__'` guard).
7. Put the shared constants (`dtype`, `parse_dates`) at module level, not inside the function.

## Acceptance criteria

Tick them **one by one** before saying you are done.

- [ ] `uv run python ingest_data.py --help` lists the 9 options with a help text each.
- [ ] `pyproject.toml` contains `click`, added through `uv`.
- [ ] No password, user or host is hard-coded in a way that cannot be overridden; the password default comes from the environment.
- [ ] The URL is built with an f-string, and `--month=3` gives `...2021-03.csv.gz` (check with a `print`, without running the full ingestion).
- [ ] `index=False` is present.
- [ ] The total is printed once, after the loop, and the `COUNT(*)` check prints `OK` or `MISMATCH`.
- [ ] A mismatch makes the exit code non-zero (`echo $?` in bash, `$LASTEXITCODE` in PowerShell).
- [ ] `import ingest_data` in a Python shell does not start any download.
- [ ] The file is saved in `practice/` (not in `01-docker-terraform/`).

<details>
<summary>Hint 1 — environment variable as default</summary>

`click.option` has a parameter that links an option to an environment variable. Read `click`'s documentation for `envvar`.

</details>

<details>
<summary>Hint 2 — exit code</summary>

`sys.exit(1)` or `raise click.ClickException(...)` both end the process with a non-zero code. Choose one and be able to say why.

</details>

<details>
<summary>Hint 3 — month on 2 digits</summary>

An f-string format specifier can pad an integer with zeros: `f"{month:02d}"`.

</details>
