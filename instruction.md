# Debugging Task: Fix Expired Session Token Handling

## Overview

A FastAPI service manages user sessions stored in memory. Clients look up a session by
passing a token in the URL. The service must return:

| Condition             | Expected HTTP Status        |
|-----------------------|-----------------------------|
| Token valid           | `200 OK` + session JSON     |
| Token expired         | `401 Unauthorized`          |
| Token does not exist  | `404 Not Found`             |

## The Bug

**File:** `src/session_repo.py`

When `get_session()` is called with an expired token it raises `ExpiredTokenError`.
This exception is **never caught** anywhere in the request path, so FastAPI falls back
to its default unhandled-exception handler and returns `500 Internal Server Error`.

The expired-token case must return `401 Unauthorized` instead.

## Your Task

Find and fix the bug so that all three pytest tests in `tests/test_outputs.py` pass.

Before the fix, running the test suite produces:

```
PASSED  tests/test_outputs.py::test_valid_token_returns_200
FAILED  tests/test_outputs.py::test_expired_token_returns_401
PASSED  tests/test_outputs.py::test_missing_token_returns_404
```

After the fix, all three tests must pass.

## Constraints

- Do **not** modify any file inside `tests/`.
- You may edit `src/session_repo.py` and/or `src/main.py`.
- No external services are required — sessions live in an in-memory dictionary.

## Running Tests

```bash
cd /app
pytest tests/test_outputs.py --tb=short -v
```

## Project Layout

```
/app/
├── src/
│   ├── __init__.py
│   ├── main.py           # FastAPI application
│   └── session_repo.py   # Session lookup logic  ← bug is here
└── tests/
    └── test_outputs.py
```
