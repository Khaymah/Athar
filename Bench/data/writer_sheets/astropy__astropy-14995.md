# astropy__astropy-14995

**Repo:** `astropy/astropy`

## What the request must convey (all units, nothing extra)

1. `NDDataRef` arithmetic mask propagation fails in astropy `5.3` when one operand lacks a mask; fine in `5.2`
2. happens with `handle_mask=np.bitwise_or`; raises `TypeError` on `|` between `int` and `NoneType`
3. repro session [[A1]]: mask × constant and mask × no-mask fail; no-mask cases and mask × mask work
4. author's guess: missing mask treated as `None`s, so `bitwise_or` gets int and `None`
5. expected: if only one operand has a mask, copy that mask to the output (as in v5.2)
6. version info [[A2]]

## Attachments (paste the placeholder where you would paste the block)

### `[[A1]]` (code)

```
>>> import numpy as np
>>> from astropy.nddata import NDDataRef

>>> array = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
>>> mask = np.array([[0, 1, 64], [8, 0, 1], [2, 1, 0]])

>>> nref_nomask = NDDataRef(array)
>>> nref_mask = NDDataRef(array, mask=mask)

# multiply no mask by constant (no mask * no mask)
>>> nref_nomask.multiply(1., handle_mask=np.bitwise_or).mask   # returns nothing, no mask,  OK

# multiply no mask by itself (no mask * no mask)
>>> nref_nomask.multiply(nref_nomask, handle_mask=np.bitwise_or).mask # return nothing, no mask, OK

# multiply mask by constant (mask * no mask)
>>> nref_mask.multiply(1., handle_mask=np.bitwise_or).mask
...
TypeError: unsupported operand type(s) for |: 'int' and 'NoneType'

# multiply mask by itself (mask * mask)
>>> nref_mask.multiply(nref_mask, handle_mask=np.bitwise_or).mask
array([[ 0,  1, 64],
       [ 8,  0,  1],
       [ 2,  1,  0]])

# multiply mask by no mask (mask * no mask)
>>> nref_mask.multiply(nref_nomask, handle_mask=np.bitwise_or).mask
...
TypeError: unsupported operand type(s) for |: 'int' and 'NoneType'
```

### `[[A2]]` (code)

````
>>> import sys; print("Python", sys.version)
Python 3.10.11 | packaged by conda-forge | (main, May 10 2023, 19:07:22) [Clang 14.0.6 ]
>>> import astropy; print("astropy", astropy.__version__)
astropy 5.3
>>> import numpy; print("Numpy", numpy.__version__)
Numpy 1.24.3
>>> import erfa; print("pyerfa", erfa.__version__)
pyerfa 2.0.0.3
>>> import scipy; print("Scipy", scipy.__version__)
Scipy 1.10.1
>>> import matplotlib; print("Matplotlib", matplotlib.__version__)
Matplotlib 3.7.1
````
