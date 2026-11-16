#!/usr/bin/env bash
# Start the local Ollama server with Tare's settings.
# `brew services` ignores shell-profile env vars, so we start it explicitly.
set -euo pipefail
export OLLAMA_CONTEXT_LENGTH="${OLLAMA_CONTEXT_LENGTH:-16384}"
# TARE_OLLAMA_URL (default http://localhost:11434) tells the Python clients where to connect; to run
# beside another Ollama server, set OLLAMA_HOST=127.0.0.1:11435 here and TARE_OLLAMA_URL=http://localhost:11435 there.
exec ollama serve
