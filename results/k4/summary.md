# K4: does a small local model have any signal?

**Result: PASS.** 25 of 60 samples correct (41.7%), against the roadmap's target of "some correct answers, ideally 10-50%". Run 2026-10-12, 20 K2 tasks x 3 samples, Python, temperature 0.2, up to 2 repairs for loud errors. Full run directory (local, git-ignored): `results/20261012-135922_k4_qwen25coder7b/`; the score records, manifest and config are copied here.

Model: `qwen2.5-coder:7b` via Ollama 0.40.3, digest `dae161e27b0e...` (see `manifest.json`), 7.6B parameters, Q4_K_M, context 16384. Benchmark 0.1.0, prompt template `k2-v1`.

| | samples | correct | silent error | loud error |
|---|---|---|---|---|
| all tasks | 60 | 25 (41.7%) | 13 (21.7%) | 22 (36.7%) |
| standard tasks | 30 | 11 | 8 | 11 |
| sponsor-variant tasks | 30 | 14 | 5 | 11 |

Classes are the final outcome after repairs; 34 of 60 samples needed at least one repair. The first-attempt class was not recorded, so first-attempt rates are not available for this run.

Per task (C correct, S silent error, L loud error; samples 0, 1, 2):

| task | result | task | result |
|---|---|---|---|
| adae-astdt-dayonly | S L S | adsl-eosstt-safety | S S S |
| adae-astdt-std | S L S | adsl-eosstt-std | S S S |
| adae-trtemfl-std | C C C | adsl-lstalvdt-addvs | L L L |
| adae-trtemfl-w0 | C C C | adsl-lstalvdt-std | L L L |
| adlb-ablfl-std | L L S | adsl-saffl-2rec | L C C |
| adlb-ablfl-strict | L L L | adsl-saffl-std | C C C |
| adlb-chg-ontrt | C L C | adsl-trtdurd-noplus1 | C C L |
| adlb-chg-std | C L L | adsl-trtdurd-std | L L L |
| adsl-agegr1-65-75 | C C C | adsl-trtsdt-active | C L C |
| adsl-agegr1-std | C C C | adsl-trtsdt-std | S C S |

- 6 of 20 tasks had at least one silent error; 9 of 20 tasks were never solved.
- Loud errors: 17 of 22 are "no output file" (the script crashed or wrote nothing), 3 are missing keys, 1 duplicate keys, 1 nulls in a non-nullable column.
- Cost: local, $0. Tokens in/out: 311,890 / 46,486. Total model latency: 2,157 s.

## What I checked about the harness
Spot checks of failing samples (`adsl-trtdurd-std`, `adsl-lstalvdt-std`, `adae-astdt-std`) showed genuine model bugs, not harness faults: applying `.dt` to Python date objects, calling string methods on already-converted dates, and flagging every complete date as imputed. One input-format gotcha is worth knowing: parquet `date32` columns arrive in pandas as Python `date` objects, not datetimes, which tripped several samples. That is a property of the task inputs, not a bug, but it inflates loud errors for this model.

## Limits
One model, 20 tasks, 3 samples per task (samples within a task are not independent), final-after-repair classes only. The pass line only says there is signal for later SFT/GRPO work; it is not a measure of the model's real accuracy.
