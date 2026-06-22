# MiniTrello Architecture

MiniTrello follows a small service-layer architecture for a Django REST
Framework backend. Views stay thin, serializers translate request payloads, and
business rules live in service modules.

## Request Flow

```text
HTTP request
  -> config/urls.py
  -> app urls.py
  -> DRF view
  -> serializer
  -> DTO / service
  -> Django model / database
  -> response serializer
```

## Applications

### users

The `users` app owns authentication-facing user behavior:

- custom `User` model with unique email
- registration serializer and endpoint
- user list endpoint
- role helpers based on Django groups
- user creation service that assigns new users to the `MEMBER` group

### boards

The `boards` app owns the project domain:

- `Board`: a workspace owned by one user
- `BoardMembership`: many-to-many relationship between users and boards
- `Task`: work item with status, priority, due date, creator, and assignee
- `TaskActivity`: audit log for task creation and important field changes

## Service Layer

Business logic is concentrated in `boards/services`:

- `task_service.py`: task creation, updates, assignment validation, activity logging
- `board_service.py`: board member assignment
- `permission_service.py`: permission checks backed by Django permissions
- `activity_service.py`: creation of task activity records

This keeps views and serializers focused on HTTP and validation concerns.

## Permissions

The project uses Django groups and permissions:

- `SUPER_ADMIN`
- `MANAGER`
- `MEMBER`

Roles are created by:

```powershell
poetry run python manage.py setup_roles
```

Task assignment and board member management are protected by explicit permission
checks in the service layer.

## API Documentation

OpenAPI schema generation is provided by `drf-spectacular`.

- Swagger UI: `/api/docs/`
- Schema: `/api/schema/`

## Testing Strategy

The test suite uses `pytest` and `pytest-django` and covers:

- models
- serializers
- service-layer business rules
- permission helpers
- API views

Test fixtures automatically create the role groups and assign permissions, so
tests do not depend on manual local setup.
