`caplog.get_records()` and `caplog.records` get out of sync after `caplog.clear()`. after the clear, `get_records()` is frozen: it isn't emptied and doesn't get new records.
from what I can tell, setup binds both to the same list, and `clear()` replaces the `records` list instead of emptying it (`src/_pytest/logging.py`).
[[A1]]
the `get_records("call") == records` check fails right after `clear()`. both should stay consistent after `clear()`.
env: Arch Linux, Python 3.9.10, `pytest` 7.1.1, packages: [[A2]]
