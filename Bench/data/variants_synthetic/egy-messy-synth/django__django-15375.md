`aggregate()` بيضرب لما تستخدم ال `default` argument بتاع ال aggregates (الجديد في 4.0) بعد `annotate()` علي Django 4.0.1 شفتها علي PostgreSQL وعملتلها repro علي SQLite فتحت الsession ب [[A1]]
لو حطيت `default=0` في `Sum` بيطلع `OperationalError: near "FROM": syntax error` [[A3]] مع ان العادي شغال `annotate(idx=F("id"))` وبعدين `aggregate(Sum("id"))` بيرجع الsum عادي [[A2]]
الSQL اللى بيطلع فيه `SELECT` بره فاضي قبل `FROM (...) subquery` [[A4]]
وعلي فكره الطريقه الطويله `Coalesce(Sum("id"), 0)` شغاله وبترجع نفس النتيجه [[A5]] 3adi
