الـ aggregate() لما بستخدم فيها الـ `default` argument بتاع الـ aggregate (الجديد في 4.0) بتضرب crash بعد annotate()، على Django 4.0.1. شفتها الأول على PostgreSQL وعملتلها reproduce على SQLite. فتحت shell كده:
[[A1]]
العادي شغال، `annotate(idx=F("id"))` وبعدين `aggregate(Sum("id"))` بترجّعلي الـ sum:
[[A2]]
بس أول ما بزوّد `default=0` على الـ `Sum` بيطلعلي `OperationalError: near "FROM": syntax error`
[[A3]]
والـ SQL اللي بيتولّد فيه `SELECT` بره فاضي قبل `FROM (...) subquery`:
[[A4]]
والـ long form `Coalesce(Sum("id"), 0)` شغالة وبترجّع نفس النتيجة:
[[A5]]
