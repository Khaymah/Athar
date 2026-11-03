> **SYNTHETIC-variant results.** Contamination control for the Haiku 5.5 probe, 2026-11-03. Unpublishable; early signal only.

# Blind contamination control (Haiku 5.5)

Variant `blind-synth`: every task gets only *"There is a bug in this repository. Find it and fix it so that the project's existing behaviour is correct."* with no task information and no attachments. If Haiku had memorised SWE-bench Verified, it would solve some tasks blind.

Stopped early by decision once the result was clear: 23/50 tasks graded (the rest were not run, to save budget).

| | Resolved | of |
|---|---|---|
| blind-synth r1 | 0 | 23 |
| en-synth r1, same tasks | 18 | 23 |

Tasks solved blind: none.

Exit statuses: Submitted 15, RepeatedFormatError 5, TimeExceeded 2, LimitsExceeded 1

Grading statuses: empty_patch 12, unresolved 11

Steps per blind run: mean 54.0 (min 16, max 100). Cost per blind run: mean $0.0627, total $1.44 for graded cells. For comparison, en-synth averages 8.8 steps and $0.004 per run.

| Task | blind | en-synth r1 | exit | steps | cost $ |
|---|---|---|---|---|---|
| astropy__astropy-14539 | unresolved | resolved | Submitted | 16 | 0.0100 |
| astropy__astropy-14995 | unresolved | resolved | Submitted | 62 | 0.0543 |
| django__django-10973 | empty_patch | resolved | Submitted | 50 | 0.0387 |
| django__django-11163 | unresolved | resolved | Submitted | 67 | 0.1503 |
| django__django-11532 | unresolved | unresolved | Submitted | 47 | 0.0480 |
| django__django-12125 | empty_patch | resolved | Submitted | 39 | 0.0248 |
| django__django-13406 | empty_patch | resolved | TimeExceeded | 21 | 0.0054 |
| django__django-13513 | empty_patch | empty_patch | RepeatedFormatError | 59 | 0.0434 |
| django__django-13568 | empty_patch | resolved | RepeatedFormatError | 68 | 0.0495 |
| django__django-13809 | empty_patch | resolved | RepeatedFormatError | 44 | 0.0360 |
| django__django-13820 | unresolved | resolved | Submitted | 31 | 0.0212 |
| django__django-14580 | unresolved | resolved | Submitted | 64 | 0.0453 |
| django__django-14608 | unresolved | resolved | Submitted | 46 | 0.0313 |
| django__django-15375 | empty_patch | resolved | RepeatedFormatError | 71 | 0.0526 |
| django__django-16082 | unresolved | resolved | Submitted | 47 | 0.0310 |
| django__django-16116 | empty_patch | resolved | Submitted | 99 | 0.2681 |
| django__django-16527 | unresolved | resolved | Submitted | 25 | 0.0148 |
| matplotlib__matplotlib-21568 | empty_patch | unresolved | TimeExceeded | 89 | 0.1319 |
| matplotlib__matplotlib-25122 | unresolved | resolved | Submitted | 46 | 0.0274 |
| matplotlib__matplotlib-25287 | empty_patch | resolved | RepeatedFormatError | 83 | 0.1704 |
| mwaskom__seaborn-3069 | unresolved | unresolved | Submitted | 25 | 0.0156 |
| pytest-dev__pytest-10051 | empty_patch | resolved | LimitsExceeded | 100 | 0.1407 |
| sphinx-doc__sphinx-7748 | empty_patch | unresolved | Submitted | 44 | 0.0323 |

**No evidence of memorization: the tax estimates above reflect comprehension, not recall.**
