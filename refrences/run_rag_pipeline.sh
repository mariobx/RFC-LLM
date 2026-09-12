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

# Model selection: CLI argument 1, or environment variable, or fallback
MODEL="${1:-${MODEL_NAME:-gemini/gemini-3.5-flash-lite}}"
OLLAMA_BASE="${OLLAMA_API_BASE:-http://localhost:11434}"

echo "============================================================"
echo "          CPSA Manual RAG Automated Pipeline                "
echo "============================================================"
echo "Target Model: $MODEL"

if [[ "$MODEL" == gemini* ]]; then
    if [ -z "$GEMINI_API_KEY" ]; then
        echo "Error: GEMINI_API_KEY is not set. Add it to .env or export it."
        exit 1
    fi
    echo "[1/3] Cloud Provider: Google Gemini (via LiteLLM)"
else
    echo "[1/3] Local Provider: Ollama at $OLLAMA_BASE"
    CLEAN_MODEL="${MODEL#ollama_chat/}"
    CLEAN_MODEL="${CLEAN_MODEL#ollama/}"
    echo "      Ensuring model '$CLEAN_MODEL' is pinned in VRAM..."
    curl -s -X POST "$OLLAMA_BASE/api/generate" \
        -d "{\"model\": \"$CLEAN_MODEL\", \"keep_alive\": -1}" > /dev/null || true
fi

# Step 2: Extract chunks (skips if already generated)
CHUNKS_FILE="$DIR/chunks/manual_chunks.json"
if [ -s "$CHUNKS_FILE" ]; then
    echo "[2/3] Existing chunk catalog detected ($CHUNKS_FILE). Skipping extraction."
else
    echo "[2/3] Extracting chunks with semantic boundary detection..."
    "$PYTHON" "$DIR/scripts/01_extract_chunks.py" --semantic-split -m "$MODEL"
fi

# Step 3: Sequential DSPy Q&A generation
echo "[3/3] Running sequential Q&A extraction across chunks using $MODEL..."
"$PYTHON" "$DIR/scripts/02_generate_qa.py" -m "$MODEL"
