# sphinx-doc__sphinx-9258

**Repo:** `sphinx-doc/sphinx`

## What the request must convey (all units, nothing extra)

1. feature request: support union types written with `|` (pipe) in type specs
2. applies to parameter / attribute / variable types in docstrings
3. use case: function accepting both `bytes` and `str` -> `:type text: bytes | str` [[A1]]
4. note: this syntax already supported by e.g. PyCharm

## Attachments (paste the placeholder where you would paste the block)

### `[[A1]]` (code)

``` restructuredtext
def foo(text):
    """Bar

    :param text: a text
    :type text: bytes | str

    """
```
