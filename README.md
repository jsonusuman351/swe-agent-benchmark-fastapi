# InfoBay AI Benchmark Task — Fix Expired Session Token HTTP Response

A debugging task for evaluating AI agents. A FastAPI session service returns
`500 Internal Server Error` when a client presents an expired token. The agent
must locate and fix the bug so the service returns `401 Unauthorized` instead.

---

## Folder Structure

```
sample-task/
├── instruction.md          # Task description for the AI agent
├── task.toml               # Task metadata (id, difficulty, type …)
├── environment/
│   └── Dockerfile          # Python 3.11 container with all dependencies
├── src/
│   ├── __init__.py
│   ├── main.py             # FastAPI app — GET /session/{token}
│   └── session_repo.py     # Session lookup logic  ← bug is here
├── solution/
│   └── solve.sh            # Reference fix + test verification
└── tests/
    ├── test.sh             # Entry-point: runs pytest
    └── test_outputs.py     # 3 pytest tests
```

---

## The Bug

`src/session_repo.py` raises `ExpiredTokenError` when a token is expired.
`src/main.py` never catches it, so FastAPI falls back to its default handler
and returns **500 Internal Server Error**.

**Expected behaviour:** expired token → **401 Unauthorized**

---

## Quick Start

### 1. Build the Docker image

```bash
cd sample-task
docker build -t infobay-task -f environment/Dockerfile .
```

### 2. Run tests — confirm the bug exists (1 test fails)

```bash
docker run --rm infobay-task pytest tests/test_outputs.py --tb=short -v
```

Expected output:
```
PASSED  tests/test_outputs.py::test_valid_token_returns_200
FAILED  tests/test_outputs.py::test_expired_token_returns_401   ← bug
PASSED  tests/test_outputs.py::test_missing_token_returns_404
```

### 3. Apply the reference fix and verify all tests pass

```bash
docker run --rm infobay-task bash solution/solve.sh
```

Expected output:
```
PASSED  tests/test_outputs.py::test_valid_token_returns_200
PASSED  tests/test_outputs.py::test_expired_token_returns_401   ← fixed
PASSED  tests/test_outputs.py::test_missing_token_returns_404
3 passed in 0.44s
```

---

## Task Metadata

| Field       | Value                                      |
|-------------|--------------------------------------------|
| ID          | `session-expired-token-401`                |
| Difficulty  | Medium                                     |
| Type        | Debugging                                  |
| Language    | Python 3.11                                |
| Framework   | FastAPI                                    |
| Entry point | `tests/test.sh`                            |

---

## The Fix (spoiler)

In `src/session_repo.py`, replace:

```python
raise ExpiredTokenError(f"Token '{token}' has expired")
```

with:

```python
from fastapi import HTTPException
raise HTTPException(status_code=401, detail="Session token has expired")
```

FastAPI natively handles `HTTPException` and returns the correct HTTP status
code — no changes to `main.py` required.
