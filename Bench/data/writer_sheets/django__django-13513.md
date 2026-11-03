# django__django-13513

**Repo:** `django/django`

## What the request must convey (all units, nothing extra)

1. debug error view (`django/views/debug.py`) ignores `exc.__suppress_context__` (PEP 415)
2. repro view [[A1]]: raises `ValueError` `from None` while handling a `RuntimeError`
3. debug page still shows the `RuntimeError`, unlike Python's own traceback
4. author's cause: `explicit_or_implicit_cause()` inside `get_traceback_frames()` [[A2]] never checks `__suppress_context__`
5. author's proposed version, simplified for Python 3: [[A3]]

## Attachments (paste the placeholder where you would paste the block)

### `[[A1]]` (code)

````
class TestView(View):
	def get(self, request, *args, **kwargs):
		try:
			raise RuntimeError('my error')
		except Exception as exc:
			raise ValueError('my new error') from None
````

### `[[A2]]` (code)

````
def get_traceback_frames(self):
	def explicit_or_implicit_cause(exc_value):
		explicit = getattr(exc_value, '__cause__', None)
		implicit = getattr(exc_value, '__context__', None)
		return explicit or implicit
````

### `[[A3]]` (code)

````
def explicit_or_implicit_cause(exc_value):
	return (
		exc_value.__cause__ or
		(None if exc_value.__suppress_context__ else
			exc_value.__context__)
	)
````
