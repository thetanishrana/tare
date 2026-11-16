# Start here: first-session runbook

This is the runbook for the first Claude Code session on Tare. Follow it in order. Stop and ask the project owner wherever it says **ASK**.

## Kickoff prompt

The project owner can paste this to start:

> Read CLAUDE.md, docs/STATUS.md and docs/00_START_HERE.md, then follow the runbook. Start with the read-only environment audit and report back before installing anything.

## 1. Read, in this order

1. `CLAUDE.md`: the rules.
2. `docs/STATUS.md`: where things stand.
3. `docs/01_PROJECT_BRIEF.md`: what we're building and why, and what's already been published.
4. `docs/02_DOMAIN_PRIMER.md`: clinical trial data (SDTM, ADaM) and how pharma does QC. Read it fully. Every later step depends on it.
5. `docs/08_ROADMAP.md`: phases and the week-1 kill tests.
6. `docs/07_SETUP.md`: the environment.
7. `docs/03_ARCHITECTURE.md`, `04_BENCHMARK_SPEC.md` and `05_EXPERIMENTS.md`: skim now, read properly before Phase 1.
8. `docs/06_TRAINING.md`: skip until Phase 3.

## 2. Read-only environment audit

Don't install or change anything yet. Collect and report:

- macOS version, chip, RAM, free disk (`sw_vers`, `sysctl -n machdep.cpu.brand_string`, `sysctl -n hw.memsize`, `df -h ~`)
- Xcode command-line tools (`xcode-select -p`)
- Homebrew (`brew --version`)
- R and Rscript (`R --version`), plus whether `admiral`, `pharmaversesdtm`, `pharmaverseadam`, `diffdf` and `renv` are installed
- Python versions (`python3 --version`, `pyenv versions`, `uv --version`)
- Docker (`docker --version`, `docker info`)
- Ollama (`ollama --version`, `ollama list`, and whether `curl -s localhost:11434/api/version` responds)
- Git configuration (`git config user.name`, `git config user.email`)
- Whether `ANTHROPIC_API_KEY` or `OPENAI_API_KEY` are set. Report only yes or no, never the value.

Report this as a table: what's present, what's missing, and what you propose to install.

## 3. Setup (ASK first)

Follow `07_SETUP.md`. Show the project owner the plan and get approval before:
- installing anything system-wide (Homebrew packages, R, Docker Desktop, Ollama)
- any download over 5 GB. Local models are ~38 GB for the three core models, ~52 GB with optional devstral:24b, so pull the small model first (K4 only needs that one).

## 4. Create the repo skeleton

- `git init`, `.gitignore`, the folder layout from `03_ARCHITECTURE.md`, `pyproject.toml`, `renv` for R.
- Keep `CLAUDE.md` and `docs/` at the root as they are.
- First commit: "Initial skeleton and planning docs".

## 5. Run K1, the oracle check

The full procedure is in `08_ROADMAP.md` under K1. In short:
- Generate the admiral templates for ADSL, ADAE and ADLB.
- First, inspect how each template reads its input data. Don't assume.
- Run the templates and compare the output against `pharmaverseadam`.
- Run the metamorphic test: shift every SDTM date forward 4 years, rerun, and expect the baseline output with dates shifted.
- Write the results to `results/k1/summary.md` and record the outcome in `STATUS.md`.

## 6. Build the K2 kit

Twenty derivation tasks (10 standard, 10 sponsor variants), each with a spec in our own words, input data, an answer key and a scoring script. See `08_ROADMAP.md` (K2) and `04_BENCHMARK_SPEC.md` for the task format. This kit becomes the seed of the full benchmark, so build it in the benchmark format from day one.

## 7. Run K2, K3 and K4 (ASK about API spend)

- **K2:** frontier models on the 20 tasks. Either the API (about $1; needs the project owner's Anthropic key and approval) or the project owner pasting prompts into the chat apps and saving responses into the expected files. Offer both.
- **K3:** compute from K2's results.
- **K4:** the small local model on the same 20 tasks.

## 8. Go/no-go

Write the go/no-go recommendation into `STATUS.md` using the template in `08_ROADMAP.md`, then tell the project owner.

## What to ask the project owner early

- Hours per week through December.
- Claude plan tier (Pro or Max).
- Whether he wants to fund about $1 of API usage for K2 or do it by hand.
- Whether the GitHub repo (`tare`, already decided) starts public or private. Suggested: private until Phase 1 results exist.
