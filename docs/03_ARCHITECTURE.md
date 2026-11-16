# Architecture

## Overview

```
                    ┌──────────────────────────── oracle (R, admiral) ─────────────────────────┐
SDTM (pharmaversesdtm)│ standard run  │ sponsor-variant runs │ perturbed-input runs            │
                    └──────────┬───────────────────────────────────────────────────────────────┘
                               │ reference outputs (hidden: never mounted into sandboxes)
                               ▼
                         ┌───────────┐
                         │ task      │  spec text + input datasets + output contract
                         │ builder   │
                         └─────┬─────┘
                               ▼
        ┌──────────────────────┴──────────────────────┐
        ▼                                             ▼
 ┌──────────────┐                              ┌──────────────┐
 │ programmer A │  model family 1, language R  │ programmer B │  model family 2, language Python
 │ (sandbox A)  │                              │ (sandbox B)  │
 └──────┬───────┘                              └──────┬───────┘
        │ output A                                    │ output B
        └──────────────────┬──────────────────────────┘
                           ▼
                    ┌─────────────┐  agree ─────────────────────► accept output
                    │ comparator  │
                    └──────┬──────┘
                           │ disagree
                           ▼
                    ┌─────────────┐  verdict A / verdict B / escalate with one question
                    │ adjudicator │
                    └──────┬──────┘
                           ▼
                    ┌─────────────┐  compares the final output with the hidden oracle:
                    │ scorer      │  correct / silent error / loud error / escalated
                    └─────────────┘
```

Everything is orchestrated in Python. The oracle runs in R. Model-written code runs in Docker.

## Components

### 1. Oracle (R)
- Runs admiral templates, or modified versions of them, on standard, variant or perturbed SDTM data, and writes reference ADaM outputs to `data/oracle/<oracle_id>/<dataset>.parquet`, together with a manifest of package versions and inputs.
- **Oracle ids** encode what was run, for example `std`, `var-agegr-65`, `pert-dateshift4`.
- **This path is never mounted into any sandbox,** and its contents never appear in prompts.

### 2. Task builder (Python, calling R where needed)
- Turns benchmark task definitions (`benchmark/tasks/*.yaml`, see `04_BENCHMARK_SPEC.md`) into runnable task bundles:
  - `inputs/`: the parquet files the programmer may read (SDTM domains plus any upstream ADaM columns taken from the oracle, so each task stands alone)
  - `spec.md`: the derivation spec in our own words
  - `contract.json`: the expected output columns, types and keys
  - `data_description.md`: a compact description of each input (columns, types, labels, share missing, a few example values, the levels of categorical variables). This is the main context the programmer sees. Track its token count.

### 3. Model providers (`tare/providers/`)
- One interface, `ModelClient.complete(messages, **params) -> Completion(text, usage, latency, raw)`.
- **OpenAI-compatible client:** covers Ollama (`http://localhost:11434/v1`) and OpenAI.
- **Anthropic client:** Messages API, with support for prompt caching and the Message Batches API for final runs.
- Every call is logged: provider, model id (and Ollama model digest), all parameters, the full prompt and response, token usage (input, output, cached), latency, estimated cost. Log to `results/<run_id>/calls.jsonl`.
- Retries with backoff. A **fake provider** that returns canned responses, for tests and dry runs at zero cost.

### 4. Programmer agent (`tare/programmer/`)
- Input: the task bundle (spec, data description, contract, language).
- Output: code, plus an output parquet produced by running that code in the sandbox.
- Loop: generate code, run it in the sandbox. If execution fails or the output breaks the contract, send back the error (truncated) and retry, up to `max_repairs` (default 2).
- **Repairs only fix loud errors.** Programmers never see the oracle, so silent errors can't be "repaired" by peeking.
- Languages: R (dplyr, lubridate and admiral allowed) or Python (pandas, numpy). Language is a config option, so the two programmers can differ.
- Start with single-shot generation plus repairs. Letting the programmer run exploratory queries on the inputs first is a later experiment axis.

### 5. Sandbox (`docker/`, `tare/sandbox/`)
- One image with R (dplyr, lubridate, stringr, admiral, arrow) and Python (pandas, pyarrow, numpy). Must be built for arm64.
- Run with: `--network none`, inputs mounted read-only, one writable `out/` directory, memory and CPU limits (start at 2 GB and 2 CPUs), a process limit, and a wall-clock timeout (start at 120 s).
- Collect stdout, stderr (truncated), the exit code and output files.
- The sandbox contains **only** that task's `inputs/`, the code file and `out/`.

### 6. Isolation guard (`tare/isolation.py`), a core claim, so test it
- Builds each sandbox's mount list from an allowlist. Refuses to start if any mount path is inside `data/oracle/`, another programmer's workdir, or `results/`.
- Before each run, checks that the workdir contains only the expected files.
- Checks every prompt for leaks: a prompt must not contain values taken from oracle outputs, which you can test by fingerprinting hashed oracle rows.
- Unit tests that try to break isolation and must fail.
- Motivation: Merck's QC program read the production ADSL output to infer a pooling rule. Tare makes that impossible by construction.

### 7. Comparator (`tare/compare.py`)
- Deterministic. Joins outputs on the contract keys and, for each target variable, counts mismatches (exact for strings and dates, a small tolerance for numbers, NA equal to NA, NA versus a value counts as a mismatch). Also counts extra or missing rows and type differences.
- Returns `agree` or a structured diff: per-variable counts plus a sample of differing records.
- The scorer uses the same code, so "agreement" and "correctness" are measured the same way.

### 8. Adjudicator (`tare/adjudicate.py`)
- Called only when the programmers disagree. Input: spec, both programs, the structured diff, and the input rows for a sample of differing records. It never sees oracle outputs.
- Output (JSON): `{"verdict": "A" | "B" | "escalate", "reason": str, "question": str | null}`. On `escalate`, `question` must be one precise question a human could answer, for example: "Does baseline include unscheduled visits on the day of first dose?"
- Policies to compare: a third model as adjudicator, versus one of the programmers' families, versus a rule (always escalate on disagreement).

**Built 2026-10-29** (`tare/programmer/agent.py`, `tare/adjudicate.py`, `tare/harness.py`, tests in `tests/test_harness.py`): `run_pair` runs two programmers, compares, and either accepts, escalates or reports a loud failure; `score_harness` classifies the result against the oracle afterwards, with `escalated` as its own class. The programmer and adjudicator modules do not import the scorer or the oracle (tested). Policies: adjudicator model or the always-escalate rule; an optional **assumption check** (a reviewer that reads both programmers' `ASSUMPTIONS:` lists when the outputs agree). The assumption check is a hypothesis: E8b found a single-prompt local reviewer does not separate ambiguous from clear specs, so nothing in the harness assumes it works. Not yet run with real models; R programmers and a run command (`tare run` for pairs) are still to do.

### 9. Scorer (`tare/score.py`)
- Compares the final output (or each programmer's raw output) with the hidden oracle and classifies each task as **correct**, **silent error** (valid output with at least one wrong value), **loud error** (no valid output) or **escalated**.
- Also produces record-level mismatch rates and the error categories from `04_BENCHMARK_SPEC.md`.

### 10. Runs, configs and reports
- `configs/*.yaml` define experiments: models, languages, temperatures, samples, adjudication policy, task split. See `05_EXPERIMENTS.md`.
- `tare run --config configs/e3_cross_family.yaml` creates `results/<timestamp>_<name>/` with a copy of the config, the git commit, package versions (Python and R), `calls.jsonl`, outputs per task, and `scores.parquet`.
- `tare report <run_dirs...>` produces tables and charts (Markdown plus PNG or SVG).

## Repo layout

```
tare/
  CLAUDE.md
  README.md
  docs/                      planning docs (this folder)
  pyproject.toml
  tare/                      Python package
    providers/  programmer/  sandbox/
    isolation.py  compare.py  adjudicate.py  score.py
    tasks.py  runs.py  report.py  cli.py
  r/                         oracle and data scripts (renv-managed)
    oracle_build.R  perturb.R  variants/  export_parquet.R
  benchmark/
    tasks/                   one YAML file per task (version-controlled)
    specs/                   spec text in our own words
    BENCHMARK_VERSION
  configs/                   experiment configs
  docker/Dockerfile          sandbox image
  training/                  Phase 3
  tests/
  data/                      generated; git-ignored (oracle outputs, task bundles)
  results/                   run outputs; git-ignored, except for chosen summary files
```

## Technology choices

| Choice | Why |
|---|---|
| Python orchestrator | Fastest to build, best model SDKs, easy to test |
| R oracle with admiral | admiral is the open-source standard for ADaM in R, and its templates give a trustworthy reference |
| Parquet between R and Python | Keeps types (dates, datetimes); `arrow` and `pyarrow` |
| Docker sandbox | Isolation and safety for running model-written code |
| OpenAI-compatible interface | One code path for Ollama and OpenAI; Anthropic gets a thin separate client |
| YAML configs plus immutable run directories | Reproducibility, which engineers reviewing the project will check |

## Testing

- Unit tests: comparator edge cases (NA, tolerance, extra rows), scorer classifications, isolation guard (attempted leaks must fail), parsing of the adjudicator's JSON.
- Golden test: one task end to end with the fake provider, which must produce known scores.
- Smoke test: one task end to end with a small local model through Ollama.
- `make test` runs without network or API keys.

## Performance notes

- Ollama swaps models in and out of memory, so group runs by model. Run local configurations one after another, not in parallel.
- For API runs, use limited concurrency and handle rate limits. For final frozen runs use the Message Batches API (50% cheaper) and prompt caching for shared prefixes (spec templates, data descriptions).
- Docker start-up adds overhead to every task. Keep the image small and reuse a warm container if needed, without weakening isolation.
