# sympy__sympy-24443

**Repo:** `sympy/sympy`

## What the request must convey (all units, nothing extra)

1. `_check_homomorphism` broken for `PermutationGroup`s
2. repro in [[A1]]: `homomorphism(D3, D3, D3.generators, D3.generators)` with `D3 = DihedralGroup(3)` raises `ValueError`
3. culprit: internal `_image()` in `sympy/combinatorics/homomorphisms.py` (L336-337), the `PermutationGroup` branch
4. when `r[i]` is an inverted generator, the `in gens` check fails
5. author thinks that logic can be greatly simplified

## Attachments (paste the placeholder where you would paste the block)

### `[[A1]]` (code)

```python
In [1]: from sympy.combinatorics import *
   ...: from sympy.combinatorics.homomorphisms import homomorphism
   ...: D3 = DihedralGroup(3)
   ...: T = homomorphism(D3, D3, D3.generators, D3.generators)

ValueError: The given images do not define a homomorphism
```
