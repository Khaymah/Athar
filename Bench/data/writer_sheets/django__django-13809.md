# django__django-13809

**Repo:** `django/django`

## What the request must convey (all units, nothing extra)

1. feature: add `--skip-checks` option to `runserver` management command
2. rationale: consistent with other management commands that run system checks
3. rationale: author wants checks only in CI/CD, not a 15-20 s wait on every dev reload
4. related StackOverflow: https://stackoverflow.com/questions/41438593/skip-system-checks-on-django-server-in-debug-mode-in-pycharm/41725866

## Attachments (paste the placeholder where you would paste the block)

_None: the request is prose only._
