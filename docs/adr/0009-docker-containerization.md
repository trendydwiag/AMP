# 0009. Use Docker for Containerization

**Status:** Accepted
**Date:** 2024-07-01

## Context

The application requires:

- Consistent environments across development, staging, and production
- PostgreSQL database service alongside the Django application
- Simplified onboarding for new developers
- Production deployment with non-root user and health checks

Manual environment setup leads to "works on my machine" issues and complex deployment scripts.

## Decision

We use **Docker** with a multi-stage `Dockerfile` and `docker-compose.yml` for local development.

### Dockerfile (Multi-stage)

```dockerfile
# Builder stage — install dependencies
FROM python:3.13-slim AS builder
WORKDIR /app
COPY requirements/base.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Runner stage — minimal runtime
FROM python:3.13-slim AS runner
WORKDIR /app
COPY --from=builder /opt/venv /opt/venv
COPY . /app/
RUN groupadd -g 1000 django && useradd -u 1000 -g django -s /bin/bash -m django
USER django
ENTRYPOINT ["/app/scripts/entrypoint.sh"]
```

### docker-compose.yml

```yaml
services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: kabulhaden_user
      POSTGRES_PASSWORD: kabulhaden_pass
      POSTGRES_DB: kabulhaden_db
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U $$POSTGRES_USER -d $$POSTGRES_DB"]

  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    depends_on:
      db:
        condition: service_healthy
    environment:
      - DATABASE_URL=postgres://kabulhaden_user:kabulhaden_pass@db:5432/kabulhaden_db
```

## Consequences

**Positive:**

- `docker-compose up --build` provides a fully working environment in one command.
- Multi-stage build produces a minimal runner image (~200MB vs ~500MB single-stage).
- Non-root `django` user in the container follows security best practices.
- PostgreSQL health check ensures the database is ready before Django starts.
- Consistent Python 3.13 runtime across all environments.

**Negative:**

- Docker adds a learning curve for developers unfamiliar with containers.
- Container networking adds complexity for debugging database connections.
- Docker images must be rebuilt when dependencies change.

**Mitigations:**

- `docker-compose.yml` uses sensible defaults so `docker-compose up` just works.
- `.env` file with `django-environ` handles environment-specific overrides.
- Entrypoint script handles migration and static file collection automatically.
