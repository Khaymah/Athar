> **SYNTHETIC-variant results.** Non-orig variants are model-written dialect (data/variants_synthetic), not human text. Unpublishable; early signal only. 2026-11-03.

# Subgroup analysis: prose-only vs with attachments

Hypothesis: when a request is all prose (no code or traceback to anchor on), the dialect matters more.

Subgroups come from `data/cards/*.json`: **prose-only** = card has no attachments (13 tasks, `data/subgroups/prose-only.txt`); **with attachments** = at least one (37 tasks, `data/subgroups/with-attachments.txt`). Same cells as the main probe: Haiku 5.5 with 3 repeats, Sonnet 5.5 with 1 repeat. No new runs. Rebuild with `dialect-tax report -c configs/probe.yaml --only-tasks data/subgroups/<group>.txt`.

## Summary (tax vs en-synth, pp, paired bootstrap 95% CI, sign-flip p)

| Model | Subgroup | n | egy-synth tax | egy-franco-synth tax | Steps en / egy / franco |
|---|---|---|---|---|---|
| Haiku | prose-only | 13 | -2.6 [-7.7, 0.0] p=1.000 | 0.0 [-7.7, 7.7] p=1.000 | 10.9 / 9.6 / 9.5 |
| Haiku | with attachments | 37 | +4.5 [-0.9, 10.8] p=0.275 | +2.7 [-1.8, 8.1] p=0.529 | 8.0 / 8.4 / 7.7 |
| Sonnet | prose-only | 13 | +7.7 [0.0, 23.1] p=1.000 | 0.0 [0.0, 0.0] p=1.000 | 6.4 / 7.2 / 7.5 |
| Sonnet | with attachments | 37 | -2.7 [-8.1, 0.0] p=1.000 | 0.0 [-8.1, 8.1] p=1.000 | 5.9 / 6.4 / 6.4 |

**Reading:** the hypothesis is not supported. No subgroup tax is distinguishable from zero, and the two models point in opposite directions. Haiku's largest point estimate is in the *with-attachments* group (+4.5 pp). Sonnet's prose-only +7.7 pp is one task out of 13 (p=1.0). The only consistent pattern is effort: on prose-only tasks, Sonnet takes about 13-17% more steps in dialect (6.4 vs 7.2 / 7.5). That is a weak signal from 13 tasks with 1 repeat, and Haiku does not show it. With n=13 the prose-only MDE is 7-22 pp, so this subgroup can only detect large effects.


---

# Full table: prose-only

## haiku-5.5

| Variant | Tasks | Resolve % | Tax (pp) | 95% CI | p | MDE (pp) | Cost/run $ | Steps/run |
|---|---|---|---|---|---|---|---|---|
| orig | 13 | 69.2 | 7.7 | [-2.6, 17.9] | 0.378 | 15.5 | 0.004 | 9.4 |
| **en-synth** | 13 | 76.9 | — | — | — | — | 0.005 | 10.9 |
| egy-synth | 13 | 79.5 | -2.6 | [-7.7, 0.0] | 1.000 | 7.2 | 0.005 | 9.6 |
| egy-franco-synth | 13 | 76.9 | 0.0 | [-7.7, 7.7] | 1.000 | 10.6 | 0.005 | 9.5 |

## sonnet-5.5-direct

| Variant | Tasks | Resolve % | Tax (pp) | 95% CI | p | MDE (pp) | Cost/run $ | Steps/run |
|---|---|---|---|---|---|---|---|---|
| orig | 13 | 84.6 | 0.0 | [0.0, 0.0] | 1.000 | 0.0 | 0.041 | 5.9 |
| **en-synth** | 13 | 84.6 | — | — | — | — | 0.049 | 6.4 |
| egy-synth | 13 | 76.9 | 7.7 | [0.0, 23.1] | 1.000 | 21.5 | 0.054 | 7.2 |
| egy-franco-synth | 13 | 84.6 | 0.0 | [0.0, 0.0] | 1.000 | 0.0 | 0.054 | 7.5 |


---

# Full table: with-attachments

## haiku-5.5

| Variant | Tasks | Resolve % | Tax (pp) | 95% CI | p | MDE (pp) | Cost/run $ | Steps/run |
|---|---|---|---|---|---|---|---|---|
| orig | 37 | 77.5 | 0.0 | [-4.5, 5.4] | 1.000 | 7.2 | 0.003 | 7.7 |
| **en-synth** | 37 | 77.5 | — | — | — | — | 0.003 | 8.0 |
| egy-synth | 37 | 73.0 | 4.5 | [-0.9, 10.8] | 0.275 | 9.0 | 0.004 | 8.4 |
| egy-franco-synth | 37 | 74.8 | 2.7 | [-1.8, 8.1] | 0.529 | 7.6 | 0.003 | 7.7 |

## sonnet-5.5-direct

| Variant | Tasks | Resolve % | Tax (pp) | 95% CI | p | MDE (pp) | Cost/run $ | Steps/run |
|---|---|---|---|---|---|---|---|---|
| orig | 37 | 78.4 | 0.0 | [-8.1, 8.1] | 1.000 | 10.8 | 0.037 | 6.2 |
| **en-synth** | 37 | 78.4 | — | — | — | — | 0.035 | 5.9 |
| egy-synth | 37 | 81.1 | -2.7 | [-8.1, 0.0] | 1.000 | 7.6 | 0.038 | 6.4 |
| egy-franco-synth | 37 | 78.4 | 0.0 | [-8.1, 8.1] | 1.000 | 10.8 | 0.036 | 6.4 |

