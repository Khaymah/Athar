# django__django-16116

**Repo:** `django/django`

## What the request must convey (all units, nothing extra)

1. `makemigrations --check` still writes migration files; only checking requires `--check` plus `--dry-run`
2. Inconsistent with `migrate --check` and `optimizemigration --check`, which just exit (maybe after some logging)
3. Proposal: `makemigrations --check` should exit without making migrations
4. Writing-anyway behavior never discussed in ticket #25604 or its django-developers thread; docs currently silent on it

## Attachments (paste the placeholder where you would paste the block)

_None: the request is prose only._
