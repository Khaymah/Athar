# django__django-10973

**Repo:** `django/django`

## What the request must convey (all units, nothing extra)

1. postgres backend `client` (`django.db.backends.postgres.client`, i.e. dbshell) should launch psql with `subprocess.run`
2. pass password via `PGPASSWORD` in a custom env for the subprocess
3. `subprocess.run` exists since Python 3.5, already the minimum since Django 2.1
4. goal: simpler and more reliable code

## Attachments (paste the placeholder where you would paste the block)

_None: the request is prose only._
