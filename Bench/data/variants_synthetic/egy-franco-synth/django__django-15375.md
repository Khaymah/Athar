el aggregate() lamma basta5dem fiha el `default` argument bta3 el aggregate (el gedeed fe 4.0) betdrab crash ba3d annotate(), 3ala Django 4.0.1. shoftaha el awel 3ala PostgreSQL w 3amaltelha reproduce 3ala SQLite. fata7t shell keda:
[[A1]]
el 3ady shaghal, `annotate(idx=F("id"))` w ba3dein `aggregate(Sum("id"))` betrag3li el sum:
[[A2]]
bas awel ma bazawwed `default=0` 3al `Sum` byetla3li `OperationalError: near "FROM": syntax error`
[[A3]]
wel SQL elly byetwalled fih `SELECT` barra fady 2abl `FROM (...) subquery`:
[[A4]]
wel long form `Coalesce(Sum("id"), 0)` shaghala w betrag3 nafs el natiga:
[[A5]]
