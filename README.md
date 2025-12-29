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
    docker run --name postgresql -e POSTGRES_PASSWORD=testpassword -e POSTGRES_USER=testuser -e POSTGRES_DB=testuser -p 5432:5432 -d postgres:13.4-alpine
```
