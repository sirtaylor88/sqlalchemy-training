# Training on SQLAlchemy

## Docker

Start PostgreSQL

```bash
    docker run --name postgresql -e POSTGRES_PASSWORD=testpassword -e POSTGRES_USER=testuser -e POSTGRES_DB=testuser -p 5432:5432 -d postgres:13.4-alpine
```
