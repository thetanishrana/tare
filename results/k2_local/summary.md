# K2, local arm: qwen3-coder:30b on the 20 K2 tasks (plus K3 against K4's 7B model)

Run 2026-10-17, local, $0. Run directory (git-ignored): `results/20261017-024527_k2_qwen3coder30b/`; score records, manifest and config are copied here.
Model: `qwen3-coder:30b` via Ollama 0.40.3, digest `06c1097efce0...` (see `manifest.json`), Q4_K_M, context 16384. 20 tasks x 3 samples, Python, temperature 0.2, up to 2 repairs for loud errors. Benchmark 0.1.0, prompt `k2-v1`.

**This is not the K2 pass line.** K2's pass line (at least 3 of 20 tasks with a silent error for at least one *frontier* model) needs the Claude API runs, which have not happened yet.

| | samples | correct | silent error | loud error |
|---|---|---|---|---|
| all tasks | 60 | 51 (85%) | 4 (6.7%) | 5 (8.3%) |
| standard tasks | 30 | 27 | 0 | 3 |
| sponsor-variant tasks | 30 | 24 | 4 | 2 |

Classes are final outcomes after repairs; 17 of 60 samples needed at least one repair (first-attempt classes were not recorded). Tokens in/out: 200,805 / 37,391; model latency 1,021 s.

Silent errors: 2 of 20 tasks.
- `adsl-eosstt-safety`, 3 of 3 samples, 52 of 306 records wrong each time. The code correctly maps `SCREEN FAILURE` to null, then a later `fillna('ONGOING')` turns those nulls into `ONGOING` (null from "screen failure" is confused with "no disposition record"). The spec is unambiguous here. The standard sibling task `adsl-eosstt-std` was correct 3 of 3.
- `adsl-lstalvdt-addvs`, 1 of 3 samples (5 records wrong).

Loud errors (5): all "no output file" (adlb-ablfl-std 3 of 3, adlb-ablfl-strict 2 of 3). The three lab-baseline samples never produced output even after repairs.

## K3 (informational; 20 tasks, anecdotal)
7B (K4) versus 30B, by sample index (wrong = not correct):

| sample | P(30B wrong given 7B wrong) | P(7B wrong given 30B wrong) |
|---|---|---|
| 0 | 2/11 | 2/2 |
| 1 | 4/12 | 4/4 |
| 2 | 3/12 | 3/3 |

Every task the 30B model got wrong was also wrong for the 7B model, in all three samples; the reverse is far from true. The "same-wrong output" rate was not measurable when this was first written: no run had output digests yet (an earlier note here saying the 30B run had them was wrong). Digests were backfilled on 2026-10-26 by re-running each saved final script (`scripts/rescore_digests.py`; all stored classes reproduced exactly), so `scripts/k3_correlation.py` can now compute it for these runs. Both models were silent-wrong on `adsl-eosstt-safety` with the same count (52 records) in one sample, which suggests the same mistake, but that is unverified.

## Limits
One model per arm, 20 tasks, samples within a task are not independent, final-after-repair classes only, and the K3 pair is two models from the same family.


## Addendum 2026-10-27: gpt-oss:20b (OpenAI family) on the same 20 tasks

Run `results/20261026-212246_k2_gptoss20b/` (local, $0; prompt `k2-v1`, temperature 0.2, 8192 max tokens, up to 2 repairs, 3 samples per task). Score records (original-round part only), manifest and config are in `gptoss20b/` here. Model digest `f38aa0c53da5...` (see manifest).

The run was meant to cover the 20 original tasks, but its config had no round filter, so it also ran the 11 harder-round tasks (93 samples in all). The configs are now pinned to a round. The 33 extra samples are reported separately in `results/k2b/summary.md` as a prompt comparison.

| | samples | correct | silent error | loud error |
|---|---|---|---|---|
| gpt-oss:20b, original 20 tasks | 60 | 52 (86.7%) | 6 (10.0%) | 2 (3.3%) |

Silent errors occurred in 3 of 20 tasks (not a frontier model, so this is not the K2 pass line):
- `adsl-lstalvdt-addvs`: 3 of 3 samples, 1 subject wrong each time. `adsl-lstalvdt-std`: 2 of 3 silent (1 subject wrong each), 1 loud. In the one subject checked (01-709-1424) the oracle returns 2013-03-17, the subject's latest lab date, and the model returned 2013-03-08, a date that appears in none of the sources: a model error, not a spec or oracle problem.
- `adsl-eosstt-safety`: 1 of 3 samples, 52 of 306 wrong. This is **the same mistake** as qwen3-coder:30b (screen failures turned into `ONGOING` after a `fillna`), and the output is byte-identical (same output digest) to the 30B's output in all of its 3 samples. Two models from different families made the identical silent error on an explicit, unambiguous spec.

Comparison on the same 20 tasks: Claude Haiku 5.5 20 of 20 and Sonnet 5.5 20 of 20 correct (1 sample each), qwen3-coder:30b 51 of 60, gpt-oss:20b 52 of 60, qwen2.5-coder:7b 25 of 60. Tokens in/out for the gpt-oss run on these 60 samples: 166,403 / 142,082.
