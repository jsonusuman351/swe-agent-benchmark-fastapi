FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir fastapi==0.111.0 uvicorn[standard]==0.29.0 pytest==8.2.0 httpx==0.27.0

COPY src/ ./src/
COPY tests/ ./tests/
COPY solution/ ./solution/

# Ensure /app is on sys.path so `from src.main import app` resolves correctly
ENV PYTHONPATH=/app

CMD ["bash"]
