`caplog.get_records()` و `caplog.records` كيتفرقو من بعد `caplog.clear()`.
من بعد الـ clear، `get_records()` كيبقى freezé: ماكيتخواش وماكتزادش فيه حتى record جديدة.
السبب حسب ما فهمت: فالـ setup بجوج مربوطين لنفس الـ liste، ولكن `clear()` كيبدل الـ list ديال `records` بوحدة جديدة بلاصة ما يخويها (`src/_pytest/logging.py`).
الـ repro، الـ check ديال `get_records("call") == records` كيطيح مباشرة من بعد `clear()`:
[[A1]]
اللي كنتسنى: بجوج يبقاو متطابقين من بعد `clear()`.
l'env: Arch Linux، Python 3.9.10، `pytest` 7.1.1، les packages: [[A2]]
