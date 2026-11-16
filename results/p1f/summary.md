# P1f: perturbed AE dates (explicit tasks), Claude Haiku 5.5 and Sonnet 5.5

Run 2026-10-29. Oracle `pert-aedates` (`r/perturb.R`, `perturb_ae_dates`, seed 20261029): in AE, 15% of start dates cut to year-month, 7% to year, 5% blank; 15% of end dates cut to year-month, 10% blank; ADSL and ADAE regenerated with the admiral templates. Partial start dates rise from 26 to 261 of 1191 and blank start dates from 0 to 58. Tasks (round `p1f`): `adae-astdt-pdates` (imputation with the first-dose adjustment, exact spec), `adae-adurn-pdates` (duration with missing end dates), `adae-aoccifl-pdates` (most severe event per subject, spec states that a missing `ASTDT` ranks last), and `adae-astdt-pdates-amb` (the underspecified first-dose-adjustment spec; stored readings `adjust-any-earlier`, 20 records differ, and `no-adjustment`, 105 differ). Reference solutions for the three explicit tasks score correct on the perturbed oracle, so the specs hold on the edge data. Prompt `k2-v2`, 3 samples, no sampling parameters. Cost: Haiku $0.0179, Sonnet $0.1641.

| Model | explicit tasks (9 samples) | ambiguous twin (3 samples) | escalations |
|---|---|---|---|
| Claude Haiku 5.5 | 9 correct | 3 matched the oracle's reading | 0 of 12 |
| Claude Sonnet 5.5 | 9 correct | 3 matched the oracle's reading | 0 of 12 |

Both models were correct on all 24 samples. Heavy partial and blank dates did not produce errors on explicit specs, and on the ambiguous twin both took the oracle's reading with no flag (right with no question asked). Together with P1e this shows that perturbing inputs for these explicit specs, and changing sponsor rules, did not make Claude fail; the one error in P1e was a missing-value bug (`0001-01-01` for missing). Limits: 4 tasks, 12 samples per model, one author for specs and perturbation.
