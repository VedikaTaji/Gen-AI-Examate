#!/bin/sh
# Build the vector index on first boot, then serve.
set -e
python - <<'PY'
from app.vectorstore import get_collection, build_index
if get_collection().count() == 0:
    print("Empty vector index - building from data/raw ...")
    build_index()
else:
    print("Vector index already present.")
PY
exec python -m uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8000}"