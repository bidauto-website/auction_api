# Repository Guidelines

## Project Structure & Module Organization
- `main.py` boots the FastAPI app and wires public v1 routers; `serve_rpc.py` runs the gRPC server.
- `routers/` holds HTTP endpoints (`routers/v1/*` for lots, filters, history, similar sales; `routers/health.py` for liveness).
- `services/`, `database/crud/`, and `database/models/` contain business logic, DB access, and SQLAlchemy models; `database/schemas/` and `schemas/` house Pydantic contracts.
- `request_schemas/` and `validators.py` define request payload validation; `auction_api/` wraps external auction calls.
- `alembic/` stores migrations; `scripts/init_db.py` seeds lookup tables from `scripts/src/*.csv`.

## Build, Test, and Development Commands
- Install dependencies: `poetry install` (uses Python 3.13).
- Run API locally: `poetry run uvicorn main:app --reload` (set `.env` values first).
- Run gRPC server: `poetry run python serve_rpc.py`.
- Apply migrations: `poetry run alembic upgrade head` (uses SQLite when `DEBUG=True`, Postgres otherwise).
- Seed static data: `poetry run python scripts/init_db.py`.
- Tests: `poetry run pytest` (CI tolerates “no tests found” but add coverage locally).

## Coding Style & Naming Conventions
- Follow PEP 8 with 4-space indentation; type hints required for public functions.
- Use Pydantic models for request/response contracts (`schemas/`, `request_schemas/`); prefer dataclass-like validation helpers in `validators.py`.
- Router files: `routers/v1/<feature>.py`; service modules: `services/<feature>.py`; migrations: timestamped under `alembic/versions/`.
- Keep logs structured via `core/logger.py`; avoid bare `print`.

## Testing Guidelines
- Framework: `pytest`; place tests under `tests/` mirroring package paths (`tests/routers/test_lots.py`, etc.).
- Name tests `test_*`; favor fixture-driven DB setup and cover both HTTP and gRPC surfaces.
- For DB-dependent tests, use SQLite in-memory or transactional fixtures; ensure Alembic migrations run before assertions.

## Commit & Pull Request Guidelines
- Commits: short, imperative summaries (e.g., “Add lot filter schema”, “Fix gRPC reflection toggle”) as seen in history.
- Pull requests should include: purpose/issue link, key changes, test evidence (`pytest` output), and any API contract notes (new endpoints, fields).
- Keep PRs scoped; update docs/migrations alongside code changes to avoid CI/ deploy drift.

## Security & Configuration Tips
- Configure `.env` using `config.Settings` fields (`DB_*`, `REDIS_URL`, `AUCTION_API_KEY`, `GRPC_SERVER_PORT`, `ROOT_PATH`, `ENVIRONMENT`).
- Never commit secrets or local SQLite files; prefer Postgres for non-debug runs.
- Verify health via `/health` and docs at `/docs` when `ENVIRONMENT=development`.
