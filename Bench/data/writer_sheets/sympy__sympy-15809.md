# sympy__sympy-15809

**Repo:** `sympy/sympy`

## What the request must convey (all units, nothing extra)

1. `Min()` and `Max()` with no arguments currently raise `ValueError: The Max/Min functions must have arguments.`
2. proposal: zero-arg `Min()` should return `oo`, zero-arg `Max()` should return `-oo`
3. justification: empty set in extended reals, see https://en.wikipedia.org/wiki/Empty_set#Extended_real_numbers

## Attachments (paste the placeholder where you would paste the block)

_None: the request is prose only._
