> **SYNTHETIC-variant results.** Non-orig variants are model-written dialect (data/variants_synthetic), not human text. Unpublishable; early signal only. Step: Sonnet 5.5 (Anthropic API) calibration, 5 tasks x 4 variants x 1 repeat, 2026-11-03. The haiku-5.5 section is the 3-repeat run, repeated for reference.

# Dialect Tax report

Reference variant: `en-synth`. Tax = reference resolve rate minus variant resolve rate, in percentage points (pp), paired by task.

## haiku-5.5

| Variant | Tasks | Resolve % | Tax (pp) | 95% CI | p | MDE (pp) | Cost/run $ | Steps/run |
|---|---|---|---|---|---|---|---|---|
| orig | 50 | 75.3 | 2.0 | [-2.7, 6.7] | 0.586 | 6.8 | 0.003 | 8.1 |
| **en-synth** | 50 | 77.3 | — | — | — | — | 0.004 | 8.8 |
| egy-synth | 50 | 74.7 | 2.7 | [-2.0, 8.0] | 0.439 | 7.0 | 0.004 | 8.7 |
| egy-franco-synth | 50 | 75.3 | 2.0 | [-2.0, 6.7] | 0.566 | 6.2 | 0.004 | 8.2 |

## sonnet-5.5-direct

| Variant | Tasks | Resolve % | Tax (pp) | 95% CI | p | MDE (pp) | Cost/run $ | Steps/run |
|---|---|---|---|---|---|---|---|---|
| orig | 5 | 80.0 | 0.0 | [0.0, 0.0] | 1.000 | 0.0 | 0.022 | 4.4 |
| **en-synth** | 5 | 80.0 | — | — | — | — | 0.023 | 4.0 |
| egy-synth | 5 | 80.0 | 0.0 | [0.0, 0.0] | 1.000 | 0.0 | 0.024 | 4.8 |
| egy-franco-synth | 5 | 80.0 | 0.0 | [0.0, 0.0] | 1.000 | 0.0 | 0.024 | 4.8 |

## Cost

Total agent cost so far: $4.14 over 643 cells ($0.006/cell).

## How to read this

- **Tax > 0** means the agent solves fewer tasks in that variant than in the reference.
- The **95% CI** comes from a paired bootstrap over tasks. If it includes 0, the pilot cannot distinguish the tax from noise.
- **MDE** is the smallest tax this many tasks can reliably detect (80% power). Use it to size the next round.
