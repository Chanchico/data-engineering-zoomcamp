# ex-004 — From notebook to script: what changes? (Concept check)

**Module:** 01 — Docker & Terraform · **Section:** Creating the Data Ingestion Script (`06-ingestion-script.md`)
**Type:** Concept check · **Difficulty:** ★☆☆
**Common thread:** preparing step 2 of the mini pipeline — *notebook → script with arguments*

## Objective

Understand why the tutorial turns your notebook into a script with command-line arguments, and read a script you did not write with a critical eye.

## Context

The tutorial gives this core of `pipeline/ingest_data.py` (course repo, `01-docker-terraform/pipeline/ingest_data.py`):

```python
@click.command()
@click.option('--pg-user', default='root', help='PostgreSQL user')
@click.option('--pg-pass', default='root', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default=5432, type=int, help='PostgreSQL port')
@click.option('--pg-db', default='ny_taxi', help='PostgreSQL database name')
@click.option('--year', default=2021, type=int, help='Year of the data')
@click.option('--month', default=1, type=int, help='Month of the data')
@click.option('--target-table', default='yellow_taxi_data', help='Target table name')
@click.option('--chunksize', default=100000, type=int, help='Chunk size for reading CSV')
def run(pg_user, pg_pass, pg_host, pg_port, pg_db, year, month, target_table, chunksize):
    ...
    for df_chunk in tqdm(df_iter):
        if first:
            df_chunk.head(0).to_sql(name=target_table, con=engine, if_exists='replace')
            first = False

        df_chunk.to_sql(name=target_table, con=engine, if_exists='append')

if __name__ == '__main__':
    run()
```

Your own notebook reads its settings from a `.env` file instead.

## Task

Answer in your own words. For every "why", describe **what the tool actually does**, not only that "it can be a problem".

1. A notebook already works. Give **two concrete things** a script with arguments allows that the notebook does not (think: who runs it, from where, how many times, with which data).
2. `if __name__ == '__main__': run()` — what is `__name__` when you run `python ingest_data.py`, and what is it when another file does `import ingest_data`? What would happen at import time without this guard?
3. The script takes `--pg-pass=root` on the command line, while your notebook reads `DB_PASSWORD` from `.env`. Name **one concrete risk** of a password on the command line (where does the command line end up?). Which approach do you prefer for the script, and why?
4. Compare this script with your ex-002 loop. It does **not** use `index=False`. What will be different in the table compared with your `yellow_taxi_data`? Which tool do you use to confirm it (not a `COUNT(*)`)?
5. You run the script with `--month=1`, then again with `--month=2`, **same `--target-table`**. Write down, **before running anything**, the final content of the table (which months, roughly how many rows). Is running the script twice with *different* arguments idempotent? Is running it twice with the *same* arguments idempotent? Explain with the mechanism (which line of the code decides it).

## Acceptance criteria

- [ ] The 5 questions are answered, each "why" names a mechanism (what the tool does).
- [ ] Question 4 names the extra column **and** the pgcli command used to check it (you may run it to confirm).
- [ ] Question 5 contains your prediction written before any run, with a number or an order of magnitude.
- [ ] The answers are saved in `practice/answers/ex-004.md`.

<details>
<summary>Hint 1 — Q2</summary>

Python sets the special variable `__name__` of a module depending on how the file is started. Print it in a two-line file and run it both ways.

</details>

<details>
<summary>Hint 2 — Q3</summary>

Think about your shell history and what other users or tools on the machine can list about running processes.

</details>

<details>
<summary>Hint 3 — Q5</summary>

Look at `if_exists='replace'` and at which chunk it applies to. The table name is the same in both runs.

</details>
