---
applyTo: "djangobackend/**/*.py"
description: "Use when editing Django backend code, including models, DRF APIs, GraphQL schema, Channels consumers, Celery tasks, or tests in djangobackend/."
---

# Django Backend Instructions

- The backend is an ASGI Django app with `daphne`, `channels`, `graphene_django`, `drf-spectacular`, Celery, Redis, and RabbitMQ configured in [djangobackend/djangobackend/settings.py](djangobackend/djangobackend/settings.py).
- Core product apps are `tabledocuments`, `dbschemas`, `dbtables`, and `endpoints`. Changes in those apps often span models, `api/`, `graphql/`, `tasks.py`, `routing.py`, `consumers.py`, and tests.
- Keep REST endpoints under `/v1/` consistent with GraphQL behavior. If you change a model or business rule, inspect both surfaces before stopping.
- Websocket behavior is part of the product architecture. Read [djangobackend/djangobackend/asgi.py](djangobackend/djangobackend/asgi.py) and the app `routing.py` files before changing consumers or auth flow.
- Test discovery is configured in [djangobackend/pytest.toml](djangobackend/pytest.toml) and coverage settings live in [djangobackend/pyproject.toml](djangobackend/pyproject.toml).
- Use `cd djangobackend && pytest` as the default validation command. Narrow to affected tests when you can.
- Keep settings and env-sensitive changes minimal. The checked-in settings default to SQLite for local DB state, but Channels and Celery still depend on Redis and RabbitMQ settings.
- Files for deployment can be found in the root [docker-compose.yaml](docker-compose.yaml) and [djangobackend/Dockerfile](djangobackend/Dockerfile). Use those as references for env vars, mounted paths, and port configuration when relevant.
