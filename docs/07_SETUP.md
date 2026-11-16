# Environment setup (macOS, Apple Silicon)

Target machine: MacBook Pro, Apple M5, 32 GB unified memory.
**Rule:** do the read-only audit first (`00_START_HERE.md`, step 2), then propose installs to the project owner and get approval. Ask before downloads over 5 GB.

## 1. Base tools

- Xcode command-line tools: `xcode-select --install` (if `xcode-select -p` fails).
- Homebrew: from https://brew.sh (if missing).
- Git identity set (`git config --global user.name`, `user.email`).

## 2. R (the oracle)

- Install the current CRAN release of R (CRAN ships macOS binaries only for current and recent R versions; an older R means compiling packages from source). Installed: **R 4.6.1** (2026-06-24), via `brew install --cask r-app` (the cask is named `r-app`, not `r`; it needs sudo, so run it yourself with `! brew install --cask r-app`). Check: `R --version`.
- In the project, use **renv**: `install.packages("renv"); renv::init(bare=TRUE)`. R is pinned to the 4.6 series (`renv::settings$r.version("4.6")`) and the snapshot type is `all`, so the lockfile stays valid before any R scripts exist.
- Packages: `admiral`, `pharmaversesdtm`, `pharmaverseadam`, `diffdf`, `dplyr`, `tidyr`, `lubridate`, `stringr`, `arrow`, `jsonlite`.
- Write the versions into `renv.lock` and commit it.
- Check: `Rscript -e 'library(admiral); admiral::list_all_templates()'`.

## 3. Python (the harness)

- Python **3.12** (works with MLX tooling and, optionally, `cdisc-rules-engine`, which requires ≥3.12 and <3.13). Use `uv` (recommended) or pyenv plus venv.
- Starting dependencies: `pandas`, `pyarrow`, `pyyaml`, `pydantic`, `openai` (also used for Ollama), `anthropic`, `python-dotenv`, `typer` (CLI), `rich`, `pytest`, `ruff`. Add `matplotlib` for reports.
- `pyproject.toml` with pinned versions; commit the lockfile.

## 4. Docker (the sandbox)

- Docker Desktop for Mac, Apple Silicon build. Check: `docker info`.
- Build `docker/Dockerfile` for **arm64**, with R (dplyr, lubridate, stringr, admiral, arrow) and Python (pandas, pyarrow, numpy). A rocker base image for R with Python added is one option. Verified 2026-10-12: `rocker/r-ver:4.6.1` and `rocker/tidyverse:4.6.1` publish arm64 manifests.
- **Cap the Docker Desktop VM at 4 GB** (Settings → Resources → Memory), so it doesn't compete with the local model for the 32 GB. The per-run `--memory 2g` limit fits inside it.
- Built and verified 2026-10-12: `docker build -t tare-sandbox:dev docker` (base `rocker/r-ver:4.6.1`, arm64; 1.38 GB; about 35 s). R packages are installed as binaries (dplyr 1.2.1, lubridate 1.9.5, stringr 1.6.0, admiral 1.5.0, arrow 25.0.1); Python 3 venv with pandas 3.0.6, pyarrow 26.0.0, numpy 2.5.4. Runs as non-root user `sandbox`. `scripts/sandbox_smoke_test.sh` checks the full run flags. Python package versions are not pinned yet.
- Image size was estimated at 1–3 GB. Ask before pulling base images over 5 GB.
- Run flags: `--network none --read-only` plus a writable `--tmpfs /tmp`, read-only input mount, writable `out/` mount, `--memory 2g --cpus 2 --pids-limit 256`, wall-clock timeout from the harness.
- Smoke test: run a trivial R and a trivial Python script that read a parquet input and write a parquet output, and confirm that network access fails.

## 5. Ollama (local models)

- Install: `brew install ollama`, or the Mac app from ollama.com. Start the server: `brew services start ollama` or `ollama serve`.
- **Context length:** Ollama's default context is about 4096 tokens, too small for spec + data description + code. Set `OLLAMA_CONTEXT_LENGTH` (start with 16384) in the environment the server runs in. Note that `brew services` doesn't read your shell profile. Verified (Ollama 0.40.3): the server reads `OLLAMA_CONTEXT_LENGTH` and other settings from its environment only. The `brew services` plist hardcodes its own environment (flash attention, q8_0 KV cache) and can be overwritten by upgrades, so start the server with `scripts/ollama_serve.sh`, which sets `OLLAMA_CONTEXT_LENGTH=16384`. `ollama ps` confirms the loaded context.
- Models, in this order (ask before the large ones):
  1. `qwen2.5-coder:7b` (about 5 GB): K4. Verified: tag valid, 4.7 GB, digest `dae161e27b0e`.
  2. `qwen3-coder:30b` (about 19 GB): main local programmer.
  3. `gpt-oss:20b` (about 14 GB): OpenAI-family local programmer.
  4. Optional: `devstral:24b` (about 14 GB).
  - Totals: ~38 GB for the three core models, ~52 GB with optional devstral:24b.
- Record each model's digest (`ollama show <model>`) in run manifests, because tags can be updated.
- OpenAI-compatible endpoint: `http://localhost:11434/v1`. Smoke test a chat completion with the `openai` client.
- Memory: plan on roughly 20–24 GB usable for one model plus its context. Don't run two large models at once. Close heavy apps during long runs.
- Performance context: Apple measured M5 time-to-first-token 3.3–4.1× faster than M4 with MLX, and generation 19–27% faster (Apple ML Research). Prompt processing matters here, because prompts are long.

## 6. API keys

- **Anthropic:** create an API key in the Claude Console (platform.claude.com). The API is billed separately from any Claude subscription and needs prepaid credit. Set a **monthly spend limit** in the Console as a safety net.
- **OpenAI** (optional): only if the budget allows an OpenAI API model. gpt-oss covers the OpenAI family locally.
- Put keys in `.env` (git-ignored). Load with `python-dotenv`. Never print keys.

## 7. Subscriptions: what's allowed

- **Fine:** using Claude Code (this tool) and Codex with subscription logins to *build* the project.
- **Not for the harness:** Anthropic's terms say developers building products or services, including with the Agent SDK, should use API keys; subscription OAuth is for ordinary use of Claude Code and Anthropic's own apps. OpenAI's Codex docs recommend API keys for programmatic workflows. So all harness model calls go through API keys or Ollama. Never script the claude.ai or chatgpt.com websites.
- **Manual K2 option:** The project owner may paste the 20 K2 prompts into the chat apps by hand, with memory and personalization off and a fresh or temporary chat each time, and save the responses into the expected files. That's ordinary use.
- Turn off "improve the model" data sharing in both apps, so held-out benchmark tasks don't end up in future training data.

## 8. Optional extras

- **mlx-lm-lora** (Phase 3): `pip install -U mlx-lm-lora`, in a separate virtual environment if its dependencies conflict.
- **cdisc-rules-engine** (optional conformance checks): Python 3.12; needs the rules cache from its GitHub repo kept in sync with the package version, and a CDISC Library API key. **VERIFY** who can get a key. Not core scope.

## 9. Verification checklist

- [ ] `R --version`, and admiral templates listed
- [ ] `pharmaverseadam::adsl` loads; row and column counts printed
- [ ] Python virtual environment created; `pytest` runs (even with zero tests)
- [ ] Docker sandbox smoke test passes, and network is blocked inside it
- [ ] `ollama list` shows the small model, and an OpenAI-compatible chat completion works
- [ ] `.env` present and git-ignored; key check prints only "set" or "missing"

## Troubleshooting notes

- R package binaries: use the CRAN build of R so packages install as Apple Silicon binaries rather than compiling.
- If `arrow` fails to install in R, try the CRAN binary repo or install `nanoparquet` as a lighter fallback, and update this doc.
- If Ollama returns truncated outputs, check the context length and `num_predict`.
