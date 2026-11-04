> **SYNTHETIC-variant results.** Non-orig variants are model-written dialect (data/variants_synthetic), not human text. Unpublishable; early signal only. 2026-11-04. Haiku 5.5: 50 tasks x 6 variants x 3 repeats. Sonnet 5.5 (Anthropic API): 50 tasks x 6 variants x 1 repeat.

# Harder variants: Moroccan Darija and messy Egyptian

New variants: `mag-synth` (Moroccan Darija) and `egy-messy-synth` (fast, messy Egyptian typing). All other cells are reused from the main probe.

## Summary (tax vs en-synth, pp, paired bootstrap 95% CI, sign-flip p)

| Variant | Haiku tax | Sonnet tax |
|---|---|---|
| orig | +2.0 [-2.7, 6.7] p=0.586 | 0.0 [-6.0, 6.0] p=1.000 |
| egy-synth | +2.7 [-2.0, 8.0] p=0.439 | 0.0 [-6.0, 6.0] p=1.000 |
| egy-franco-synth | +2.0 [-2.0, 6.7] p=0.566 | 0.0 [-6.0, 6.0] p=1.000 |
| mag-synth | +2.7 [-1.3, 7.3] p=0.362 | -2.0 [-6.0, 0.0] p=1.000 |
| egy-messy-synth | 0.0 [-4.0, 4.0] p=1.000 | +4.0 [0.0, 10.0] p=0.507 |

**Reading:** still no tax distinguishable from zero. The largest point estimate is Sonnet on messy Egyptian (+4.0 pp: 2 tasks lost, sympy-13974 and sympy-15017, none gained; p=0.51). That is the closest thing to a signal so far, and it would need repeats to confirm. Moroccan, the dialect furthest from MSA and Egyptian, does not hurt either model. As before, model-written text is cleaner than real text, so these are lower bounds.

## Subgroups for the new variants (tax vs en-synth)

| Model | Subgroup | n | mag-synth | egy-messy-synth |
|---|---|---|---|---|
| Haiku | prose-only | 13 | -2.6 [-7.7, 0.0] p=1.000 | -2.6 [-10.3, 5.1] p=1.000 |
| Haiku | with attachments | 37 | +4.5 [0.0, 9.9] p=0.187 | +0.9 [-3.6, 5.4] p=1.000 |
| Sonnet | prose-only | 13 | 0.0 [0.0, 0.0] p=1.000 | 0.0 [0.0, 0.0] p=1.000 |
| Sonnet | with attachments | 37 | -2.7 [-8.1, 0.0] p=1.000 | +5.4 [0.0, 13.5] p=0.507 |

As in the first subgroup analysis, prose-only tasks do not show a larger tax. Where there is a positive estimate, it is in the with-attachments group.

# Dialect Tax report

Reference variant: `en-synth`. Tax = reference resolve rate minus variant resolve rate, in percentage points (pp), paired by task.

## haiku-5.5

| Variant | Tasks | Resolve % | Tax (pp) | 95% CI | p | MDE (pp) | Cost/run $ | Steps/run |
|---|---|---|---|---|---|---|---|---|
| orig | 50 | 75.3 | 2.0 | [-2.7, 6.7] | 0.586 | 6.8 | 0.003 | 8.1 |
| **en-synth** | 50 | 77.3 | — | — | — | — | 0.004 | 8.8 |
| egy-synth | 50 | 74.7 | 2.7 | [-2.0, 8.0] | 0.439 | 7.0 | 0.004 | 8.7 |
| egy-franco-synth | 50 | 75.3 | 2.0 | [-2.0, 6.7] | 0.566 | 6.2 | 0.004 | 8.2 |
| mag-synth | 50 | 74.7 | 2.7 | [-1.3, 7.3] | 0.362 | 5.9 | 0.004 | 9.2 |
| egy-messy-synth | 50 | 77.3 | -0.0 | [-4.0, 4.0] | 1.000 | 6.0 | 0.004 | 8.3 |

## sonnet-5.5-direct

| Variant | Tasks | Resolve % | Tax (pp) | 95% CI | p | MDE (pp) | Cost/run $ | Steps/run |
|---|---|---|---|---|---|---|---|---|
| orig | 50 | 80.0 | 0.0 | [-6.0, 6.0] | 1.000 | 8.0 | 0.038 | 6.1 |
| **en-synth** | 50 | 80.0 | — | — | — | — | 0.039 | 6.0 |
| egy-synth | 50 | 80.0 | 0.0 | [-6.0, 6.0] | 1.000 | 8.0 | 0.042 | 6.6 |
| egy-franco-synth | 50 | 80.0 | 0.0 | [-6.0, 6.0] | 1.000 | 8.0 | 0.041 | 6.7 |
| mag-synth | 50 | 82.0 | -2.0 | [-6.0, 0.0] | 1.000 | 5.6 | 0.041 | 6.3 |
| egy-messy-synth | 50 | 76.0 | 4.0 | [0.0, 10.0] | 0.507 | 7.8 | 0.041 | 6.5 |

## Cost

Total agent cost so far: $16.92 over 1223 cells ($0.014/cell).


## Discordant tasks among en / egy / mag / egy-messy, Sonnet 5.5 (resolved/repeats)

| Task | en-synth | egy-synth | mag-synth | egy-messy-synth |
|---|---|---|---|---|
| django__django-13809 | 1/1 | 0/1 | 1/1 | 1/1 |
| matplotlib__matplotlib-21568 | 0/1 | 1/1 | 1/1 | 0/1 |
| sympy__sympy-13974 | 1/1 | 1/1 | 1/1 | 0/1 |
| sympy__sympy-15017 | 1/1 | 1/1 | 1/1 | 0/1 |

## Discordant tasks among en / egy / mag / egy-messy, Haiku 5.5 (resolved/repeats)

| Task | en-synth | egy-synth | mag-synth | egy-messy-synth |
|---|---|---|---|---|
| django__django-10973 | 3/3 | 3/3 | 3/3 | 2/3 |
| django__django-11532 | 1/3 | 1/3 | 0/3 | 2/3 |
| django__django-12125 | 3/3 | 3/3 | 3/3 | 2/3 |
| django__django-13406 | 2/3 | 0/3 | 1/3 | 1/3 |
| matplotlib__matplotlib-21568 | 1/3 | 0/3 | 0/3 | 1/3 |
| matplotlib__matplotlib-23412 | 3/3 | 3/3 | 2/3 | 3/3 |
| matplotlib__matplotlib-23476 | 3/3 | 2/3 | 3/3 | 3/3 |
| matplotlib__matplotlib-25775 | 1/3 | 1/3 | 1/3 | 2/3 |
| mwaskom__seaborn-3069 | 2/3 | 3/3 | 3/3 | 3/3 |
| pytest-dev__pytest-10051 | 2/3 | 3/3 | 3/3 | 3/3 |
| sphinx-doc__sphinx-8056 | 3/3 | 2/3 | 3/3 | 2/3 |
| sympy__sympy-15017 | 3/3 | 1/3 | 1/3 | 2/3 |
| sympy__sympy-21379 | 2/3 | 3/3 | 2/3 | 3/3 |
