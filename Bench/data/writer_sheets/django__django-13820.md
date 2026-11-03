# django__django-13820

**Repo:** `django/django`

## What the request must convey (all units, nothing extra)

1. `MigrationLoader.load_disk` (`django.db.migrations.loader`) skips migrations module `m` when `getattr(m, '__file__', None)` is falsy
2. Intent of that check: reject PEP-420 namespace packages; but regular packages may also lack `__file__`
3. Python import docs: `__file__` optional; import system may leave it unset (e.g. module loaded from database)
4. Affects frozen Python environments (not setting `__file__` on regular packages): existing migrations not found; related tickets #30950, #32177
5. Namespace packages' `__path__` is a custom iterable, not `list` (CPython `_NamespacePath` = implementation detail, don't rely on it)
6. Author proposes: augment the `__file__` check with `and isinstance(m.__path__, list)`
7. Constraints: namespace packages still rejected for migrations; no behavior change in normal envs; no other frozen-env features

## Attachments (paste the placeholder where you would paste the block)

_None: the request is prose only._
