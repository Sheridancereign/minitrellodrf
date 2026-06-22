# MiniTrello

MiniTrello is a Django REST Framework API for a small Trello-like task board.
It supports user registration, JWT authentication, boards, board membership,
tasks, task assignment, role-based permissions, and task activity tracking.

## Tech Stack

- Python 3.12
- Django 6
- Django REST Framework
- PostgreSQL
- Simple JWT
- drf-spectacular / Swagger UI
- Pydantic DTOs
- Poetry
- pytest / pytest-django
- Ruff, Black, mypy, pre-commit

## Features

- Custom user model with unique email
- JWT authentication
- Board creation and membership
- Task CRUD with status, priority, due date, creator, and assignee
- Task assignment flow with permission checks
- Task activity history for creation, status changes, and assignee changes
- Role setup command for `SUPER_ADMIN`, `MANAGER`, and `MEMBER`
- Swagger/OpenAPI documentation
- Environment-based settings via `.env`
- Docker and Docker Compose setup for local development
- GitHub Actions CI for checks, linting, and tests

## Portfolio Highlights

This project is designed to demonstrate backend skills that are useful in real
business applications:

- service-layer business logic instead of putting rules directly in views
- role-based access control using Django groups and permissions
- PostgreSQL-backed relational modeling
- query-aware API views with `select_related`
- activity/audit logging for important domain events
- reproducible local setup with Docker Compose
- documented API surface with Swagger and curl examples

## Project Structure

```text
MiniTrello/
├── boards/
│   ├── dto/                    # Pydantic DTOs for task operations
│   ├── migrations/
│   ├── services/               # Business logic for boards, tasks, permissions, activity
│   ├── models.py               # Board, Task, TaskActivity, BoardMembership
│   ├── serializers.py          # DRF serializers
│   ├── urls.py                 # Board and task API routes
│   └── views.py                # DRF views
├── config/
│   ├── settings.py             # Django settings
│   └── urls.py                 # Root URL configuration
├── docs/
│   ├── architecture.md         # Architecture overview
│   └── api-examples.md         # Example API requests
├── tests/                      # pytest test suite
├── users/
│   ├── management/commands/
│   │   └── setup_roles.py      # Creates groups and assigns permissions
│   ├── services/
│   ├── models.py               # Custom User model
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
├── manage.py
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
└── pytest.ini
```

## Environment Variables

The project uses `python-decouple` to read configuration from a local `.env`
file. Create `.env` in the project root:

```env
SECRET_KEY=change-me
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:5174

DB_NAME=minitrello
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```

`SECRET_KEY`, database credentials, and other local secrets should not be
committed to Git. The repository `.gitignore` already ignores `.env` files.
Use `.env.example` as a safe template for local configuration.

## Installation

Clone the repository and install dependencies:

```powershell
git clone <repository-url>
cd MiniTrello
poetry install
```

Create and configure the `.env` file as shown above.

Make sure PostgreSQL is running and that the database from `DB_NAME` exists:

```sql
CREATE DATABASE minitrello;
```

Apply migrations:

```powershell
poetry run python manage.py migrate
```

Create system roles and permissions:

```powershell
poetry run python manage.py setup_roles
```

Create an admin user if needed:

```powershell
poetry run python manage.py createsuperuser
```

Run the development server:

```powershell
poetry run python manage.py runserver
```

The API will be available at:

```text
http://127.0.0.1:8000/
```

## Docker Setup

For a containerised local environment, copy the example environment file and
adjust values if needed:

```powershell
copy .env.example .env
```

Build and start the application with PostgreSQL:

```powershell
docker compose up --build
```

The `web` service runs migrations, configures roles, and starts Django at:

```text
http://127.0.0.1:8000/
```

## API Documentation

Swagger UI:

```text
GET /api/docs/
```

OpenAPI schema:

```text
GET /api/schema/
```

## Authentication

Register a user:

```text
POST /api/users/register/
```

Request body:

```json
{
  "username": "john",
  "last_name": "Doe",
  "email": "john@example.com",
  "password": "strong-password"
}
```

Get JWT tokens:

```text
POST /api/token/
```

Request body:

```json
{
  "username": "john",
  "password": "strong-password"
}
```

Use the access token for protected endpoints:

```http
Authorization: Bearer <access_token>
```

Refresh token:

```text
POST /api/token/refresh/
```

## Main Endpoints

### Users

| Method | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/api/users/register/` | Register a new user |
| `GET` | `/api/users/` | List users |

### Boards

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/api/boards/` | List boards where the current user is a member |
| `POST` | `/api/boards/` | Create a board |
| `GET` | `/api/boards/<id>/` | Retrieve a board |
| `PUT/PATCH` | `/api/boards/<id>/` | Update a board |
| `DELETE` | `/api/boards/<id>/` | Delete a board |
| `POST` | `/api/boards/<id>/members/assign/` | Add a user to a board |

### Tasks

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/api/boards/tasks/` | List tasks from boards where the current user is a member |
| `POST` | `/api/boards/tasks/` | Create a task |
| `GET` | `/api/boards/tasks/<id>/` | Retrieve a task |
| `PUT/PATCH` | `/api/boards/tasks/<id>/` | Update a task |
| `DELETE` | `/api/boards/tasks/<id>/` | Delete a task |
| `POST` | `/api/boards/tasks/<id>/assign/` | Assign or clear a task assignee |

### Activities

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/api/boards/activities/` | List task activity for boards owned by the current user |

## Domain Rules

### Boards

- A board has an owner.
- The owner is automatically added as a board member when the board is created.
- Board membership is stored through `BoardMembership`.
- Each user can be added to the same board only once.
- Board details are protected by owner-level permissions.

### Tasks

- A task belongs to a board.
- A task has a status: `TODO`, `IN_PROGRESS`, or `DONE`.
- A task has a priority: `LOW`, `MEDIUM`, or `HIGH`.
- A task may have a due date.
- A task may have an assignee.
- A task stores the user who created it.
- A task cannot be created as `DONE` without an assignee.
- A task cannot use a due date in the past.
- A task assignee must be a member of the task board.
- A `DONE` task cannot be modified.
- Changing task status or assignee creates a `TaskActivity` record.

### Task Assignment

- Only users with the `boards.assign_task` permission, or superusers, can assign tasks.
- The selected assignee must be a member of the task board.
- Assigning a user to a `DONE` task is not allowed.
- Passing `null` as `assignee` clears the current assignee.

### Activities

- Task creation creates a `CREATED` activity.
- Status changes create a `STATUS_CHANGED` activity.
- Assignee changes create an `ASSIGNEE_CHANGED` activity.
- Activity entries store the actor, changed field, old value, new value, and timestamp.

## Roles and Permissions

Roles are configured with:

```powershell
poetry run python manage.py setup_roles
```

Current roles:

| Role | Purpose |
| --- | --- |
| `SUPER_ADMIN` | Full board/task/activity permissions |
| `MANAGER` | Can manage board members and assign tasks |
| `MEMBER` | Can view and work with accessible boards/tasks |

Newly registered users are automatically added to the `MEMBER` group.

## Development Commands

Run Django system checks:

```powershell
poetry run python manage.py check
```

Run tests:

```powershell
poetry run pytest
```

Run Ruff:

```powershell
poetry run ruff check .
```

Format code with Black:

```powershell
poetry run black .
```

Run pre-commit hooks:

```powershell
poetry run pre-commit run --all-files
```

## Architecture

The project keeps business logic in services instead of placing it directly in
views. A detailed architecture note is available in:

```text
docs/architecture.md
```

Example API requests are available in:

```text
docs/api-examples.md
```

## Testing

The test suite uses `pytest` and `pytest-django`.

Tests cover:

- model behavior
- serializers
- permission helpers
- board and task services
- API views
- task activity logging
- role-based assignment flows

Test configuration is stored in `pytest.ini`.

## Notes

- Registration expects the `MEMBER` group to exist, so run `setup_roles` after migrations.
- PostgreSQL is required by the current settings.
- The project is intended as a learning/pet project for DRF architecture, service-layer business logic, JWT authentication, and permission modeling.
