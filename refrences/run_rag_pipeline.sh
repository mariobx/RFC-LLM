#!/usr/bin/env bash
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON="$DIR/../.venv/bin/python"

if [ ! -f "$PYTHON" ]; then
    echo "Error: Python environment not found at $DIR/../.venv"
    exit 1
fi

# Load environment variables if .env exists
if [ -f "$DIR/.env" ]; then
    set -a
    source "$DIR/.env"
    set +a
elif [ -f "$DIR/../.env" ]; then
    set -a
    source "$DIR/../.env"
    set +a
fi

# Model selection
MODEL="${1:-${MODEL_NAME:-gemini/gemini-3.1-flash-lite}}"
TARGET_DIR="${2:-}"

echo "============================================================"
echo "    CPSA Atomic Semantic Decomposition & RAG Pipeline       "
echo "============================================================"
echo "Target Model: $MODEL"

if [[ "$MODEL" == gemini* ]]; then
    if [ -z "$GEMINI_API_KEY" ]; then
        echo "Error: GEMINI_API_KEY is not set. Add it to .env or export it."
        exit 1
    fi
    echo "[1/2] Cloud Provider: Google Gemini ($MODEL)"
else
    echo "[1/2] Local Provider: Ollama"
fi

# Step 1: Semantic Component Chunking
echo "[2/2] Extracting atomic semantic components with exact line-break boundaries..."
if [ -n "$TARGET_DIR" ]; then
    "$PYTHON" "$DIR/scripts/01_extract_chunks.py" --dir "$TARGET_DIR" --semantic-split -m "$MODEL"
else
    "$PYTHON" "$DIR/scripts/01_extract_chunks.py" --semantic-split -m "$MODEL"
fi

echo ""
echo "============================================================"
echo "RAG Semantic Decomposition complete!"
echo "Chunks catalog: $DIR/chunks/manual_chunks.jsonl"
echo "Checkpoint:     $DIR/chunks/checkpoint.json"
echo "To query: $PYTHON $DIR/scripts/03_query_rag.py '<query>'"
echo "============================================================"
