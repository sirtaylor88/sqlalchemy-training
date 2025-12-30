# Training on SQLAlchemy

## Get start

This project need Python 3.12 and uses `uv` as dependency management.

```bash
python -m venv .venv
source .venv/bin/activate
uv sync
```

## Docker

Start PostgreSQL

```bash
    docker-compose up
```

## Migrations

Create migrations

```bash
    alembic revision --autogenerate -m "initial migration"
```

Apply migration

```bash
    alembic upgrade head
```

Downgrade to the previous migration

```bash
    alembic downgrade -1
```
