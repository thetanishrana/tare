# P1e: three hard explicit sponsor-variant tasks on Claude Haiku 5.5 and Sonnet 5.5

Run 2026-10-29. Tasks `adsl-lstalvdt-complete` (partial dates dropped), `adlb-ontrtfl-w7` (on treatment until 7 days after the last dose) and `adae-aoccifl-bysoc` (most severe event per subject and body system). Exact specs, oracle from a patched admiral template, none ambiguous. Prompt `k2-v2`, 3 samples, up to 2 repairs, no sampling parameters. Cost: Haiku $0.0102, Sonnet $0.1043. A direction-finding run (9 samples per model), not a reported measurement.

| Model | correct | silent errors | loud errors | escalations |
|---|---|---|---|---|
| Claude Haiku 5.5 | 9 of 9 | 0 | 0 | 0 |
| Claude Sonnet 5.5 | 8 of 9 | 1 | 0 | 0 |

- Haiku solved every sample, including both variants whose rule differs from the standard admiral one.
- Sonnet's silent error: `adsl-lstalvdt-complete` sample 1 followed the spec's rule (only complete dates) but wrote the date `0001-01-01` for the 52 subjects with no usable date instead of a missing value (a null-to-date conversion bug), so the output was valid but wrong for those subjects. Category: missing-value, not a misreading of the variant rule.
- The variant rules did not trip the models: they applied the changed window, the changed grouping and the complete-dates rule correctly in 17 of 18 samples.

## Reading

On explicit specs with a changed rule, Claude again produced no spec-misreading errors, as on the original 20 tasks; the one error was a data-handling bug on a missing value. Direction: more variants of this kind are unlikely to separate the models. A harder explicit set would need rules that conflict with what models remember from admiral, multi-dataset rules or longer rule chains, and perturbed inputs that exercise missing and partial values (as `pert-edge` does).

Limits: 3 tasks, 9 samples per model, one author for the variants and specs.
