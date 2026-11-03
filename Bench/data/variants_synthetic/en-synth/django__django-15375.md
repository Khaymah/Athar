aggregate() with the aggregate `default` argument (new in 4.0) crashes after annotate(), Django 4.0.1. saw it on PostgreSQL first, reproduced on SQLite. opened a shell with
[[A1]]
baseline works, `annotate(idx=F("id"))` then `aggregate(Sum("id"))` returns the sum:
[[A2]]
but adding `default=0` to the `Sum` raises `OperationalError: near "FROM": syntax error`
[[A3]]
the generated SQL has an empty outer `SELECT` before `FROM (...) subquery`:
[[A4]]
and the long form `Coalesce(Sum("id"), 0)` works and gives the same result:
[[A5]]
