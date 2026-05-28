#!/usr/bin/env bash
set -euo pipefail

cd /app
pytest tests/test_outputs.py --tb=short -v
