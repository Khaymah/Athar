# Dialect Tax — evaluation harness

Measures how much coding-agent performance drops when a SWE-bench task is written
in an Arabic dialect (or Franco/Arabizi) instead of English. Design rationale:
[`../Docs/DialectTax.md`](../Docs/DialectTax.md). Writer instructions (Arabic):
[`WritersGuide.md`](WritersGuide.md).

## How it works

1. **Tasks**: 50 SWE-bench Verified instances, stratified by repo (`data/pilot_tasks.json`).
2. **Cards**: each issue is split into prose and verbatim *attachments* (code, tracebacks).
   Cards hold short *information units* that a native-speaker writer turns into a request,
   without seeing the original English prose (`data/cards/`, rendered to `data/writer_sheets/`).
3. **Variants**: writers produce `data/variants/<variant>/<instance_id>.md` with `[[A1]]`
   placeholders. Attachments are substituted byte-for-byte, so only the language differs.
   `orig` is the untouched SWE-bench text (sanity anchor); `en` is the fair reference.
4. **Runs**: [mini-swe-agent](https://github.com/SWE-agent/mini-swe-agent) with the same
   English scaffold for every variant; only the task text changes. Every
   (task × model × variant × repeat) cell is graded with the official SWE-bench harness.
5. **Analysis**: paired by task. Tax = reference resolve rate − variant resolve rate (pp),
   with a paired-bootstrap 95% CI, a sign-flip permutation p-value, and the minimum
   detectable effect at the current task count.

## Setup

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -e "Bench[dev]"
```

Docker must be running. Images come from Epoch AI's GHCR mirror
(`ghcr.io/epoch-research/swe-bench.eval.x86_64.<id>`), 1–4 GB each; runs are task-major
and delete each image after its cells finish, so ~30 GB free disk is enough.

Only one secret is needed for the pilot:

```bash
export OPENROUTER_API_KEY=...
```

## Commands (run from `Bench/`)

```bash
dialect-tax select-tasks                 # pick the 50 pilot tasks
dialect-tax make-cards                   # split issues into prose + attachments
dialect-tax sheets                       # render writer sheets
dialect-tax validate                     # check writers' variant files
dialect-tax run --models gold,empty --variants orig --limit 2 --repeats 1 --output runs/dryrun   # keyless end-to-end check
dialect-tax run --variants orig --limit 5 --repeats 1   # cost calibration (needs key)
dialect-tax estimate-cost                # extrapolate full pilot cost
dialect-tax run                          # full pilot (resumable)
dialect-tax report                       # rebuild runs/pilot/report.md
```

`gold` applies the reference patch and must come out `resolved`; `empty` submits nothing
and must come out `empty_patch`. If `gold` fails on a task, that task's environment is broken
and should be dropped before spending money on it.

## Writers' web page

`web/WriterApp.template.html` is built into `web/WriterApp.html` by
`dialect-tax build-writer-page` and published as a private artifact. It embeds the cards
**without** the English prose or title. Writers (shared as Contributors) claim a task,
write `en` / `egy` / `egy-franco` with live script and placeholder checks, and submit.

Store layout (artifact `db`):

```
claims/<instance_id>               {uid, status: claimed|submitted, at}
subs/<uid>/tasks/<instance_id>     {en, egy, franco, status, updatedAt}   # each writer writes only their own
```

To pull submissions into the repo, export `claims` and each claimer's `subs/<uid>/tasks`
to a directory (the store's `out_dir` export), then:

```bash
dialect-tax import-submissions path/to/export   # writes data/variants/* and data/variants/provenance.json
dialect-tax validate
```

## Output layout

```
runs/<experiment>/cells/<model>/<variant>/r<k>/<instance_id>/
    task.md          # exact text the agent saw
    trajectory.json  # full agent transcript
    agent.json       # exit status, patch, cost, api calls
    eval.json        # resolved / unresolved / empty_patch / patch_apply_failed / eval_error
runs/<experiment>/eval_logs/   # SWE-bench harness logs
runs/<experiment>/report.md
```

`eval_error` and `agent_error` are infrastructure failures: they are excluded from the
analysis and retried on the next `run`.

## Tests

```bash
cd Bench && python -m pytest -q
```
