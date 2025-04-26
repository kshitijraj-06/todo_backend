# Todo API Documentation

## Table of Contents
- [Base Information](#base-information)
- [Authentication](#authentication)
- [Error Handling](#error-handling)
- [Endpoints](#endpoints)
  - [Todos Collection](#todos-collection)
  - [Single Todo](#single-todo)
  - [Todo Completion](#todo-completion)
- [Examples](#examples)
- [Rate Limits](#rate-limits)

## Base Information
**Base URL**: `http://localhost:5000/api`  
**Content Type**: `application/json`

## Authentication
This API currently requires no authentication.

## Error Handling
All error responses follow this format:
```json
{
    "error": "Descriptive error message",
    "status": 400
}
```

Common status codes:
- `400` Bad Request
- `404` Not Found
- `500` Internal Server Error

## Endpoints

### Todos Collection

#### Get All Todos
`GET /todos`

**Response**  
`200 OK`
```json
[
    {
        "id": 1,
        "title": "Sample todo",
        "description": null,
        "completed": false,
        "created_at": "2023-01-01T00:00:00",
        "due_date": null
    }
]
```

#### Create Todo
`POST /todos`

**Request Body**:
```json
{
    "title": "Required todo title",
    "description": "Optional description",
    "due_date": "2023-12-31T23:59:59"
}
```

**Response**  
`201 Created`
```json
{
    "id": 2,
    "title": "Newly created todo",
    "description": "Optional description",
    "completed": false,
    "created_at": "2023-01-01T00:00:00",
    "due_date": "2023-12-31T23:59:59"
}
```

### Single Todo

#### Get Todo
`GET /todos/{id}`

**Response**  
`200 OK`
```json
{
    "id": 1,
    "title": "Specific todo",
    "description": "Its description",
    "completed": false,
    "created_at": "2023-01-01T00:00:00",
    "due_date": null
}
```

#### Update Todo
`PUT /todos/{id}`

**Request Body**:
```json
{
    "title": "Updated title",
    "completed": true,
    "due_date": "2024-01-01T00:00:00"
}
```

**Response**  
`200 OK`
```json
{
    "id": 1,
    "title": "Updated title",
    "description": "Existing description",
    "completed": true,
    "created_at": "2023-01-01T00:00:00",
    "due_date": "2024-01-01T00:00:00"
}
```

#### Delete Todo
`DELETE /todos/{id}`

**Response**  
`200 OK`
```json
{
    "message": "Todo deleted successfully"
}
```

### Todo Completion

#### Mark as Complete
`PUT /todos/{id}/complete`

**Response**  
`200 OK`
```json
{
    "id": 1,
    "title": "Sample todo",
    "completed": true
}
```

#### Mark as Incomplete
`PUT /todos/{id}/uncomplete`

**Response**  
`200 OK`
```json
{
    "id": 1,
    "title": "Sample todo",
    "completed": false
}
```

## Examples

### cURL Examples
```bash
# Get all todos
curl -X GET http://localhost:5000/api/todos

# Create todo
curl -X POST -H "Content-Type: application/json" \
-d '{"title":"New todo"}' \
http://localhost:5000/api/todos

# Update todo
curl -X PUT -H "Content-Type: application/json" \
-d '{"title":"Updated title"}' \
http://localhost:5000/api/todos/1
```

### Python Example
```python
import requests

BASE_URL = "http://localhost:5000/api"

# Create new todo
response = requests.post(
    f"{BASE_URL}/todos",
    json={"title": "Python created todo"}
)
print(response.json())
```

## Rate Limits
None currently enforced.

## Version
`v1.0.0`  
Last Updated: `2025-04-27`

