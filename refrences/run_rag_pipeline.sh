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

# Step 1: Documentation Semantic Component Chunking
echo "[1/2] Processing technical documentation into atomic semantic chunks..."
if [ -n "$TARGET_DIR" ]; then
    "$PYTHON" "$DIR/scripts/01_extract_chunks.py" --dir "$TARGET_DIR" -m "$MODEL"
else
    "$PYTHON" "$DIR/scripts/01_extract_chunks.py" -m "$MODEL"
fi

# Step 2: SCM Code Examples Extraction
echo ""
echo "[2/2] Extracting SCM code examples with formal AST features and scenario summaries..."
"$PYTHON" "$DIR/scripts/02_extract_code_examples.py" -m "$MODEL"

echo ""
echo "============================================================"
echo "CPSA Full RAG Corpus Pipeline Complete!"
echo "Documentation Chunks: $DIR/chunks/manual_chunks.jsonl"
echo "Code Examples:        $DIR/chunks/code_examples.jsonl"
echo "To query: $PYTHON $DIR/scripts/03_query_rag.py '<query>'"
echo "============================================================"
