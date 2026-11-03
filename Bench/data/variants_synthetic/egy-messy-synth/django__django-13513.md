صفحه الdebug error فى `django/views/debug.py` مش بتحترم `exc.__suppress_context__` بتاع PEP 415
لو عندك view زى [[A1]] بترمى `ValueError` `from None` وهى بتهاندل `RuntimeError` صفحة الdebug lessa بتظهر الـ `RuntimeError` عكس traceback بتاع python نفسه
اعتقد السبب `explicit_or_implicit_cause()` جوا `get_traceback_frames()` [[A2]] عمرها ما بتشيك على `__suppress_context__`
ودى نسختى مبسطه لpython 3 [[A3]]
