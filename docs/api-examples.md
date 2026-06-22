# API Examples

These examples assume the development server is running at:

```text
http://127.0.0.1:8000
```

## Register a User

```bash
curl -X POST http://127.0.0.1:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john",
    "last_name": "Doe",
    "email": "john@example.com",
    "password": "strong-password"
  }'
```

## Get JWT Tokens

```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john",
    "password": "strong-password"
  }'
```

Use the returned access token:

```bash
export ACCESS_TOKEN="<access_token>"
```

## Create a Board

```bash
curl -X POST http://127.0.0.1:8000/api/boards/ \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Product Roadmap",
    "description": "Planning board for product work"
  }'
```

## Create a Task

```bash
curl -X POST http://127.0.0.1:8000/api/boards/tasks/ \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Prepare API documentation",
    "description": "Document auth, board, task, and activity endpoints",
    "status": "TODO",
    "priority": "HIGH",
    "board": 1
  }'
```

## Update Task Status

```bash
curl -X PATCH http://127.0.0.1:8000/api/boards/tasks/1/ \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "IN_PROGRESS"
  }'
```

## Assign a Task

The current user must have the `boards.assign_task` permission.

```bash
curl -X POST http://127.0.0.1:8000/api/boards/tasks/1/assign/ \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "assignee": 2
  }'
```

## View Activity

```bash
curl -X GET http://127.0.0.1:8000/api/boards/activities/ \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```
