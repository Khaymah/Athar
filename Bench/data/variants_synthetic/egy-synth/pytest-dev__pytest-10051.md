`caplog.get_records()` بيبقى مختلف عن `caplog.records` بعد `caplog.clear()`.
بعد الـ clear الـ `get_records()` بتتجمد: مبتفضاش ومبيدخلهاش records جديدة.
اللي فهمته إن الـ setup بيربط الاتنين على نفس الـ list، و`clear()` بيبدّل الـ `records` بـ list جديدة بدل ما يفضّيها (`src/_pytest/logging.py`).
[[A1]]
الـ check بتاع `get_records("call") == records` بيفشل على طول بعد `clear()`. المفروض الاتنين يفضلوا consistent بعد الـ `clear()`.
الـ env: Arch Linux, Python 3.9.10, `pytest` 7.1.1، والـ packages: [[A2]]
