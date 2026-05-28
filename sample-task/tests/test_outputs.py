import pytest
from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app, raise_server_exceptions=False)


def test_valid_token_returns_200():
    """A live, non-expired token must return 200 with session data."""
    response = client.get("/session/valid_token_abc")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == 1
    assert data["username"] == "alice"


def test_expired_token_returns_401():
    """An expired token must return 401 Unauthorized.

    Before the bug is fixed this test FAILS — the unhandled ExpiredTokenError
    causes FastAPI to return 500 Internal Server Error instead.
    """
    response = client.get("/session/expired_token_xyz")
    assert response.status_code == 401


def test_missing_token_returns_404():
    """A token that was never issued must return 404 Not Found."""
    response = client.get("/session/nonexistent_token_000")
    assert response.status_code == 404
