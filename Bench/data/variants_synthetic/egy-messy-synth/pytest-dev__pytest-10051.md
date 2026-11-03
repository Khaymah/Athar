بعد `caplog.clear()` ال `caplog.get_records()` بتبقا مختلفه عن `caplog.records` و `get_records()` بتجمد خالص لا بتفضى ولا بيدخلها records جديده
السبب ان الsetup بيربط الاتنين بنفس الlist bas `clear()` بيبدل list ال `records` بواحده جديده بدل ما يفضيها ف `src/_pytest/logging.py`
الcheck بتاع `get_records("call") == records` بيفشل علطول بعد `clear()`
[[A1]]
المفروض الاتنين يفضلو consistent بعد `clear()`
Arch Linux و Python 3.9.10 و `pytest` 7.1.1 و دى الpackages [[A2]]
