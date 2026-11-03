la vue ديال debug error (`django/views/debug.py`) ماكتحترمش `exc.__suppress_context__` (PEP 415).
هاهي view باش تعاودها: [[A1]]، كترمي `ValueError` `from None` وهي كتhandli `RuntimeError`.
الصفحة ديال debug باقا كتبين `RuntimeError`، ماشي بحال le traceback ديال Python براسو.
السبب فراسي: `explicit_or_implicit_cause()` اللي وسط `get_traceback_frames()` [[A2]] عمرها ما كتشيكي `__suppress_context__`.
هادي الversion اللي كنقترح، مبسطة ل Python 3: [[A3]]
