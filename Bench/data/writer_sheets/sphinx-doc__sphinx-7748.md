# sphinx-doc__sphinx-7748

**Repo:** `sphinx-doc/sphinx`

## What the request must convey (all units, nothing extra)

1. context: SWIG-wrapped C++ classes with overloaded methods
2. convention: one signature per overload, all placed at the start of the docstring
3. `autodoc_docstring_signature` currently picks up only the first signature
4. request: make it pick up all of the signatures

## Attachments (paste the placeholder where you would paste the block)

_None: the request is prose only._
