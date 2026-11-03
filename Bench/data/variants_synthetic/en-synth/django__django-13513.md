the debug error view in django/views/debug.py ignores exc.__suppress_context__ (PEP 415). repro view, raises ValueError from None while handling a RuntimeError:
[[A1]]
debug page still shows the RuntimeError, unlike Python's own traceback. I think the cause is explicit_or_implicit_cause() inside get_traceback_frames(), it never checks __suppress_context__:
[[A2]]
here's what I'd propose, simplified for Python 3:
[[A3]]
