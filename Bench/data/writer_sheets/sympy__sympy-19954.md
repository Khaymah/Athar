# sympy__sympy-19954

**Repo:** `sympy/sympy`

## What the request must convey (all units, nothing extra)

1. `sylow_subgroup()` in `sympy.combinatorics` raises `IndexError` for some dihedral groups
2. repro and traceback [[A1]]: `DihedralGroup(18)` with `p=2`; fails inside `minimal_blocks()`
3. same error with the group in [[A2]] (`DihedralGroup(2*25)`, `p=2`)
4. expected: Sylow subgroup returned without error
5. env: sympy 1.6.1, numpy 1.18.5, scipy 1.4.1, Python 3.8.5 on Windows 64-bit

## Attachments (paste the placeholder where you would paste the block)

### `[[A1]]` (traceback)

````
from sympy.combinatorics import DihedralGroup, PermutationGroup, Permutation

G = DihedralGroup(18)

S2 = G.sylow_subgroup(p=2)
 
Traceback (most recent call last):
  File "<input>", line 7, in <module>
  File "D:\anaconda38\envs\default\lib\site-packages\sympy\combinatorics\perm_groups.py", line 4370, in sylow_subgroup
    blocks = self.minimal_blocks()
  File "D:\anaconda38\envs\default\lib\site-packages\sympy\combinatorics\perm_groups.py", line 2207, in minimal_blocks
    del num_blocks[i], blocks[i]
IndexError: list assignment index out of range
````

### `[[A2]]` (code)

````
G = DihedralGroup(2*25)

S2 = G.sylow_subgroup(p=2)
````
