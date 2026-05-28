import time


class ExpiredTokenError(Exception):
    pass


# In-memory session store.  expires_at is a Unix timestamp.
SESSIONS = {
    "valid_token_abc": {
        "user_id": 1,
        "username": "alice",
        "expires_at": 9_999_999_999,   # year 2286 — effectively never expires
    },
    "expired_token_xyz": {
        "user_id": 2,
        "username": "bob",
        "expires_at": 1_000_000_000,   # 2001-09-08 — always expired
    },
}


def get_session(token: str):
    """Return session data for *token*.

    Returns None when the token is not found.
    Raises ExpiredTokenError when the token exists but has expired.
    """
    if token not in SESSIONS:
        return None

    session = SESSIONS[token]
    if session["expires_at"] < time.time():
        # BUG: ExpiredTokenError is never caught by the caller.
        # FastAPI has no handler for it, so the request returns 500
        # instead of the expected 401 Unauthorized.
        raise ExpiredTokenError(f"Token '{token}' has expired")

    return session
