# Setup — DE Zoomcamp (my fork)

How to rebuild my working environment from scratch.
Covers Module 01 up to **06 — Ingestion script**.

---

## 1. Prerequisites (Windows host)

| Tool | Notes |
|------|-------|
| WSL 2 + a Linux distro (Ubuntu/Debian) | All commands below run inside WSL |
| Docker Desktop | Settings → Resources → WSL integration → enable for the distro |
| VS Code + extensions *WSL*, *Python*, *Jupyter* | Open the repo from WSL: `code .` |
| Git | `git config --global core.autocrlf input` to avoid CRLF noise (see §8) |

Check:

```bash
docker run hello-world
git --version
```

## 2. Get the repo

```bash
git clone <my-fork-url> data-engineering-zoomcamp
cd data-engineering-zoomcamp
```

Layout: course folders (`01-docker-terraform/`, …) are read-only, my work goes in `practice/`, exercises in `exos/`.

## 3. Python environment with uv (section 02)

The uv project lives at the **repo root** (`pyproject.toml`, `uv.lock`, `.python-version` = 3.13).

```bash
pip install uv            # or: curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync                   # creates .venv/ and installs everything from uv.lock
uv run python -V          # → Python 3.13.x
```

What `uv sync` installs (already in `pyproject.toml`):

- runtime: `pandas`, `pyarrow`, `sqlalchemy`, `psycopg[binary,pool]`, `python-dotenv`, `tqdm`
- dev: `jupyter`, `pgcli`

To rebuild it by hand instead of `uv sync`:

```bash
uv init --python=3.13
uv add pandas pyarrow sqlalchemy "psycopg[binary,pool]" python-dotenv tqdm
uv add --dev jupyter pgcli
```

## 4. Environment variables (`.env`)

Copy the template at the repo root and adjust if needed:

```bash
cp .env.example .env
```

```dotenv
URL=https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/
DATA=yellow_tripdata_2021-01.csv.gz

DB_HOST=localhost
DB_PORT=5432
DB_NAME=ny_taxi
DB_PASSWORD=root
DB_USERNAME=root
```

`.env` is git-ignored (`**.env`). The code loads it with `load_dotenv()`.

## 5. Docker pipeline test (section 03)

```bash
cd practice
docker build -t test:pandas -f dockerfile .
docker run -it test:pandas 10
cd ..
```

## 6. Postgres in Docker (section 04)

Run in a dedicated terminal (keep it open):

```bash
docker run -it --rm \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v ny_taxi_postgres_data:/var/lib/postgresql \
  -p 5432:5432 \
  postgres:18
```

- Named volume `ny_taxi_postgres_data` → data survives `--rm`.
- Values must match `.env`.

Connect:

```bash
uv run pgcli -h localhost -p 5432 -u root -d ny_taxi
```

## 7. Ingestion

### Notebook (section 05)

```bash
uv run jupyter notebook     # or open practice/ingestion.ipynb in VS Code, kernel = .venv
```

Loads yellow taxi 2021-01 into `yellow_taxi_data` in chunks. Expected check in pgcli:

```sql
SELECT COUNT(*) FROM yellow_taxi_data;   -- 1369765
```

### Script with arguments (section 06)

Convert the notebook:

```bash
uv run jupyter nbconvert --to=script practice/ingestion.ipynb
```

The script uses `click`, which is **not yet** in `pyproject.toml`:

```bash
uv add click
```

Run:

```bash
uv run python practice/ingestion.py \
  --pg-user=root --pg-pass=root \
  --pg-host=localhost --pg-port=5432 \
  --pg-db=ny_taxi --target-table=yellow_taxi_data
```

## 8. VS Code / Git config

`.vscode/settings.json`:

- `"python.terminal.useEnvFile": true` → terminals load `.env`
- WSL terminal profile as default
- Copilot disabled

`.vscode/launch.json`: debug config *Python: current file* using `${workspaceFolder}/.venv/bin/python`.

Line endings: if `git status` suddenly shows hundreds of modified files, it is CRLF vs LF. Check with
`git diff --ignore-cr-at-eol --name-only` (lists only real changes).

---

<!-- Next sections are appended as the course progresses. -->
