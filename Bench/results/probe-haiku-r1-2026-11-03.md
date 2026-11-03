> **SYNTHETIC-variant results.** Non-orig variants are model-written dialect (data/variants_synthetic), not human text. Unpublishable; early signal only. Step: Haiku 5.5 full probe, 50 tasks x 4 variants x 1 repeat, 2026-11-03.

# Dialect Tax report

Reference variant: `en-synth`. Tax = reference resolve rate minus variant resolve rate, in percentage points (pp), paired by task.

## haiku-5.5

| Variant | Tasks | Resolve % | Tax (pp) | 95% CI | p | MDE (pp) | Cost/run $ | Steps/run |
|---|---|---|---|---|---|---|---|---|
| orig | 50 | 78.0 | 0.0 | [-6.0, 6.0] | 1.000 | 8.0 | 0.003 | 7.8 |
| **en-synth** | 50 | 78.0 | — | — | — | — | 0.004 | 8.7 |
| egy-synth | 50 | 78.0 | 0.0 | [-8.0, 8.0] | 1.000 | 11.3 | 0.004 | 8.6 |
| egy-franco-synth | 50 | 76.0 | 2.0 | [-4.0, 10.0] | 1.000 | 9.8 | 0.004 | 8.7 |

## Cost

Total agent cost so far: $0.74 over 200 cells ($0.004/cell).

## How to read this

- **Tax > 0** means the agent solves fewer tasks in that variant than in the reference.
- The **95% CI** comes from a paired bootstrap over tasks. If it includes 0, the pilot cannot distinguish the tax from noise.
- **MDE** is the smallest tax this many tasks can reliably detect (80% power). Use it to size the next round.
