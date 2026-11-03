> **SYNTHETIC-variant results.** Non-orig variants are model-written dialect (data/variants_synthetic), not human text. Unpublishable; early signal only. Step: Haiku 5.5 full probe, 50 tasks x 4 variants x 3 repeats, 2026-11-03.

# Dialect Tax report

Reference variant: `en-synth`. Tax = reference resolve rate minus variant resolve rate, in percentage points (pp), paired by task.

## haiku-5.5

| Variant | Tasks | Resolve % | Tax (pp) | 95% CI | p | MDE (pp) | Cost/run $ | Steps/run |
|---|---|---|---|---|---|---|---|---|
| orig | 50 | 75.3 | 2.0 | [-2.7, 6.7] | 0.586 | 6.8 | 0.003 | 8.1 |
| **en-synth** | 50 | 77.3 | — | — | — | — | 0.004 | 8.8 |
| egy-synth | 50 | 74.7 | 2.7 | [-2.0, 8.0] | 0.439 | 7.0 | 0.004 | 8.7 |
| egy-franco-synth | 50 | 75.3 | 2.0 | [-2.0, 6.7] | 0.566 | 6.2 | 0.004 | 8.2 |

## Cost

Total agent cost so far: $2.23 over 600 cells ($0.004/cell).

## How to read this

- **Tax > 0** means the agent solves fewer tasks in that variant than in the reference.
- The **95% CI** comes from a paired bootstrap over tasks. If it includes 0, the pilot cannot distinguish the tax from noise.
- **MDE** is the smallest tax this many tasks can reliably detect (80% power). Use it to size the next round.

## Discordant tasks (resolved/repeats per variant, where variants disagree)

| Task | orig | en-synth | egy-synth | egy-franco-synth |
|---|---|---|---|---|
| django__django-10973 | 2/3 | 3/3 | 3/3 | 3/3 |
| django__django-12125 | 1/3 | 3/3 | 3/3 | 3/3 |
| django__django-13406 | 3/3 | 2/3 | 0/3 | 0/3 |
| django__django-13809 | 2/3 | 3/3 | 3/3 | 3/3 |
| django__django-14608 | 2/3 | 3/3 | 3/3 | 3/3 |
| django__django-16082 | 3/3 | 3/3 | 3/3 | 2/3 |
| matplotlib__matplotlib-21568 | 1/3 | 1/3 | 0/3 | 1/3 |
| matplotlib__matplotlib-23476 | 3/3 | 3/3 | 2/3 | 3/3 |
| matplotlib__matplotlib-25122 | 3/3 | 3/3 | 3/3 | 2/3 |
| mwaskom__seaborn-3069 | 3/3 | 2/3 | 3/3 | 3/3 |
| pytest-dev__pytest-10051 | 3/3 | 2/3 | 3/3 | 3/3 |
| sphinx-doc__sphinx-8056 | 2/3 | 3/3 | 2/3 | 2/3 |
| sphinx-doc__sphinx-8593 | 3/3 | 3/3 | 3/3 | 2/3 |
| sympy__sympy-15017 | 3/3 | 3/3 | 1/3 | 3/3 |
| sympy__sympy-15809 | 2/3 | 3/3 | 3/3 | 3/3 |
| sympy__sympy-21379 | 3/3 | 2/3 | 3/3 | 3/3 |
