سلام، `aggregate()` مع l'argument `default` ديال les aggregates (جديد ف 4.0) كيكراشي إلا جا من بعد `annotate()`، ف Django 4.0.1.
شفتها ف PostgreSQL و عاودت درتها ف SQLite، حليت la session بـ [[A1]]
الحالة العادية خدامة: `annotate(idx=F("id"))` ومن بعد `aggregate(Sum("id"))` كترجع la somme [[A2]]
ولكن ملي كنزيد `default=0` لـ `Sum` كيطلع ليا `OperationalError: near "FROM": syntax error` [[A3]]
الـ SQL لي كيتولد فيه `SELECT` خارجي خاوي قبل `FROM (...) subquery` [[A4]]
والصيغة الطويلة `Coalesce(Sum("id"), 0)` خدامة وكترجع نفس النتيجة [[A5]]
