# sympy__sympy-12481

**Repo:** `sympy/sympy`

## What the request must convey (all units, nothing extra)

1. `Permutation` constructor rejects non-disjoint cycles
2. `Permutation([[0,1],[0,1]])` raises `ValueError`
3. expected: identity permutation for that input
4. general rule wanted: non-disjoint cycles applied in left-to-right order, resulting permutation returned
5. author sees no reason to forbid non-disjoint cycles

## Attachments (paste the placeholder where you would paste the block)

_None: the request is prose only._
