# Inventory Manager

A modular Python application for the **SEN 401 – Software Configuration Management and Maintenance** labs at Miva Open University.

- **v1.0** (Lab 3 – Status Accounting & Auditing): console app with maintenance tasks, change log and CSA record.
- **v2.0** (Lab 4 – Re-engineering & Migration): reverse engineered, refactored into layers, data migrated from JSON to **SQLite**, exposed through a **FastAPI** REST API and deployed with **Docker Compose**.

## Project Structure (v2.0)

```
sen401-inventory-project/
├── app.py                    # Console entry point (calls inventory_app.cli)
├── inventory_app/
│   ├── __init__.py           # Package version
│   ├── config.py             # Settings from environment variables
│   ├── models.py             # Pydantic models: ItemCreate, ItemUpdate, Item, StockSummary
│   ├── controllers.py        # Business logic: CRUD, low stock, stock summary
│   ├── utils.py              # item_value(), total_value(), format_money()
│   ├── database.py           # SQLite schema and queries
│   ├── migrate.py            # JSON -> SQLite migration (idempotent)
│   ├── api.py                # FastAPI REST API
│   └── cli.py                # Console report / add / low-stock commands
├── data/
│   └── inventory.json        # Legacy data exported from v1.0 (migration source)
├── docker/
│   ├── api.Dockerfile        # API service image
│   ├── migrate.Dockerfile    # Migration job image
│   └── report.Dockerfile     # Console report client image
├── docker-compose.yml        # Orchestrates migrate, api, report and db-viewer
├── docs/
│   └── REVERSE_ENGINEERING.md # Module inventory, dependency diagrams, code smells
├── tests/                    # 14 unit tests (models, database, migration, API)
├── changelog.txt, CSA.md     # Lab 3 status accounting records
└── requirements.txt
```

## Architecture

```
cli.py / api.py  ->  controllers.py  ->  database.py  ->  SQLite (inventory.db)
                          |                  ^
                   models.py, utils.py   migrate.py <- data/inventory.json
```

See [docs/REVERSE_ENGINEERING.md](docs/REVERSE_ENGINEERING.md) for the full before/after diagrams.

## Run locally (Python 3.12+)

```bash
pip install -r requirements.txt
python -m inventory_app.migrate          # JSON -> data/inventory.db
python app.py                            # stock report
python app.py add "Webcam" 15 25000      # write a new item to SQLite
uvicorn inventory_app.api:app --reload   # API on http://localhost:8000/docs
python -m unittest discover -s tests -v  # run the tests
```

## Run with Docker Compose

```bash
docker compose up --build
```

| Service | Image | Purpose | URL |
|---------|-------|---------|-----|
| `migrate` | docker/migrate.Dockerfile | One-shot job: migrates JSON into SQLite, then exits | – |
| `api` | docker/api.Dockerfile | FastAPI REST API (waits for migrate; has a health check) | http://localhost:8000/docs |
| `report` | docker/report.Dockerfile | Calls the API at `http://api:8000` and prints the stock report | – |
| `db-viewer` | coleifer/sqlite-web | Web view of the SQLite database | http://localhost:8080 |

All services share the SQLite file through the `db-data` volume. Stop with `docker compose down` (add `-v` to delete the data).

## REST API

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| GET | `/items` | List all items |
| POST | `/items` | Create an item (201; 409 if the name exists; 422 if invalid) |
| GET | `/items/{id}` | Get one item (404 if missing) |
| PATCH | `/items/{id}` | Update some fields |
| DELETE | `/items/{id}` | Delete an item (204) |
| GET | `/items/low-stock?threshold=10` | Items at or below the threshold |
| GET | `/summary` | Totals, highest/lowest stock and low-stock items |

## Branches and releases

| Branch | Purpose |
|--------|---------|
| `main` | Stable, released code |
| `dev` | Lab 3 maintenance work (released as v1.0) |
| `reengineering` | Lab 4 re-engineering and migration work (released as v2.0) |

| Tag | Description |
|-----|-------------|
| v1.0 | Lab 3 – console app after corrective, adaptive, perfective and preventive maintenance |
| v2.0 | Lab 4 – layered package, SQLite, FastAPI and Docker Compose |

## Generating the change log

```bash
git log --all --pretty=format:"%h | %an | %ad | %d %s" --date=iso > changelog.txt
```
