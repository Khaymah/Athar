# sphinx-doc__sphinx-8593

**Repo:** `sphinx-doc/sphinx`

## What the request must convey (all units, nothing extra)

1. autodoc: `:meta public:` in a doc-comment has no effect on module-level variables
2. repro: private variable `_foo` with `#: :meta public:` [[A1]], documented via `automodule` with `:members:` [[A2]]
3. actual: `_foo` missing from built docs
4. expected: `_foo` shown in built docs
5. env: Sphinx HEAD of 3.x, `sphinx.ext.autodoc`

## Attachments (paste the placeholder where you would paste the block)

### `[[A1]]` (code)

```
# example.py
_foo = None  #: :meta public:
```

### `[[A2]]` (code)

```
# index.rst
.. automodule:: example
   :members:
```
