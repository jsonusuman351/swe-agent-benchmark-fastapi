from fastapi import FastAPI
from fastapi.responses import JSONResponse

from src.session_repo import get_session

app = FastAPI()


@app.get("/session/{token}")
def read_session(token: str):
    # get_session() can raise ExpiredTokenError for expired tokens.
    # That exception is not handled here, so FastAPI returns 500.
    session = get_session(token)
    if session is None:
        return JSONResponse(status_code=404, content={"detail": "Session not found"})
    return {"user_id": session["user_id"], "username": session["username"]}
