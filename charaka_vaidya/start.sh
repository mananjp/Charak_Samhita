#!/bin/bash
set -e

echo "🚀 Starting Charaka Vaidya..."

# Run ingestion if vector store is missing
if [ ! -d "data/chroma_db" ]; then
  echo "  → Vector store not found. Running ingestion pipeline (this may take a minute)..."
  python scripts/ingest.py
fi

# Use Render's $PORT env var, fallback to 8000 for local dev
PORT=${PORT:-8000}

# Start FastAPI backend
echo "  → Starting FastAPI on port $PORT..."
uvicorn api.main:app --host 0.0.0.0 --port $PORT
