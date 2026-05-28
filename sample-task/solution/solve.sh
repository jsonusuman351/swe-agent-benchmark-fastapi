#!/usr/bin/env bash
# Reference solution: fix the unhandled ExpiredTokenError in session_repo.py.
#
# Root cause: get_session() raises ExpiredTokenError for expired tokens, but
# no caller catches it. FastAPI's default exception handler turns any unhandled
# exception into a 500 Internal Server Error.
#
# Fix: replace the bare `raise ExpiredTokenError(...)` with FastAPI's
# HTTPException(status_code=401) so the framework emits a proper 401 response.
set -euo pipefail

cat > /app/src/session_repo.py << 'PYTHON'
import time
from fastapi import HTTPException


class ExpiredTokenError(Exception):
    """Kept for import compatibility; no longer raised by this module."""
    pass


SESSIONS = {
    "valid_token_abc": {
        "user_id": 1,
        "username": "alice",
        "expires_at": 9_999_999_999,
    },
    "expired_token_xyz": {
        "user_id": 2,
        "username": "bob",
        "expires_at": 1_000_000_000,
    },
}


def get_session(token: str):
    """Return session data for *token*.

    Returns None when the token is not found.
    Raises HTTPException(401) when the token exists but has expired.
    """
    if token not in SESSIONS:
        return None

    session = SESSIONS[token]
    if session["expires_at"] < time.time():
        raise HTTPException(status_code=401, detail="Session token has expired")

    return session
PYTHON

echo "Patch applied to /app/src/session_repo.py"
echo ""
echo "Running test suite to confirm fix..."
echo "------------------------------------"
cd /app
pytest tests/test_outputs.py --tb=short -v
