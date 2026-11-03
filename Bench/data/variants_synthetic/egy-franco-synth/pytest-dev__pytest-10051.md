`caplog.get_records()` biyb2a mo5talef 3an `caplog.records` ba3d `caplog.clear()`.
ba3d el clear el `get_records()` betetgammed: mabtetfadash w mabyed5olhash records gdida.
elly fehmto en el setup biyorbot el etnein 3ala nafs el list, w `clear()` biybaddel el `records` be list gdida badal ma yfaddiha (`src/_pytest/logging.py`).
[[A1]]
el check bta3 `get_records("call") == records` biyefshal 3ala tool ba3d `clear()`. el mafrood el etnein yefdalo consistent ba3d el `clear()`.
el env: Arch Linux, Python 3.9.10, `pytest` 7.1.1, wel packages: [[A2]]
