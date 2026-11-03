# sympy__sympy-15017

**Repo:** `sympy/sympy`

## What the request must convey (all units, nothing extra)

1. `sympy.tensor.array.NDimArray.__len__` always returns `0` for rank-0 (scalar) arrays
2. repro [[A1]]: `len` of scalar `Array` gives 0 while iterating it yields one element
3. expected `len` = 1: number of elements of the iterator, matching numpy behaviour
4. numpy comparison in [[A2]]
5. tested on sympy 1.2-rc1, Python 3.6.6

## Attachments (paste the placeholder where you would paste the block)

### `[[A1]]` (code)

```python
>>> import sympy
>>> a = sympy.Array(3)
>>> len(a)
0
>>> len(list(a))
1
```

### `[[A2]]` (code)

```python
>>> import numpy
>>> numpy.asarray(1).size
1
```
