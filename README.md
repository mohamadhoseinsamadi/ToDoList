# ToDoList

A task management system built with Python and OOP principles: organize work into **projects**, each containing groups of **tasks** with statuses (`todo`, `doing`, `done`). Ships with two interfaces — an interactive **CLI** and a **REST API** (FastAPI) — both backed by PostgreSQL through SQLAlchemy.

## Features

- **Project management:** create, edit, and delete projects (full CRUD).
- **Task management:** add, modify, and remove tasks within each project.
- **Status tracking:** `todo` → `doing` → `done`.
- **Cascade delete:** deleting a project removes its tasks.
- **Input validation:** name/description length limits and field validation.
- **Configurable limits:** maximum projects, tasks, and field lengths via environment variables.
- **Overdue auto-close:** a scheduled job closes overdue tasks.

## Requirements

- Python 3.10+
- PostgreSQL
- [Poetry](https://python-poetry.org/)

## Setup

```bash
poetry install
cp .env.example .env   # then set DATABASE_URL to your PostgreSQL instance
```

Database tables are created automatically at startup.

## Running

**REST API:**

```bash
poetry run uvicorn app.main:app --reload
```

- Interactive docs: http://127.0.0.1:8000/docs
- Endpoints are served under `/api/v1` (projects, tasks, all-tasks).

**CLI:**

```bash
poetry run python -m app.cli_run
```

## Configuration

Limits can be tuned in `.env` (defaults shown):

```
MAX_NUMBER_OF_PROJECTS=10
MAX_NUMBER_OF_TASKS=50
MAX_PROJECT_NAME_LENGTH=30
MAX_PROJECT_DESCRIPTION_LENGTH=150
MAX_TASK_NAME_LENGTH=30
MAX_TASK_DESCRIPTION_LENGTH=150
```

## Project Structure

```
app/
  api/          # FastAPI routers, controllers, request/response schemas
  cli/          # Interactive console interface
  services/     # Business logic
  repositories/ # SQLAlchemy data access
  models/       # ORM models (Project, Task)
  db/           # Engine, session, declarative base
  commands/     # Scheduled jobs (overdue auto-close)
  memory/       # Legacy in-memory storage (kept for reference)
```

## License

MIT — see [LICENSE](LICENSE).