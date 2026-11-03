# sympy__sympy-16792

**Repo:** `sympy/sympy`

## What the request must convey (all units, nothing extra)

1. `autowrap` with `backend='cython'` broken when an array argument does not appear in the wrapped `expr`
2. repro in [[A1]]: `MatrixSymbol('x', 2, 1)` as arg, `expr = 1.0`; call should return `1.0`
3. instead raises [[A2]] (`TypeError: only size-1 arrays can be converted to Python scalars`)
4. cause: generated C function has wrong signature, see [[A3]]; `x` should be `double *`, not `double`
5. works fine if `expr` depends on every argument, e.g. `expr = x[0,0]` in [[A4]]
6. use case: external libs (e.g. numerical integration) need a fixed signature even if some args are unused
7. author suspects the bug is in `codegen`

## Attachments (paste the placeholder where you would paste the block)

### `[[A1]]` (code)

```python
from sympy.utilities.autowrap import autowrap
from sympy import MatrixSymbol
import numpy as np

x = MatrixSymbol('x', 2, 1)
expr = 1.0
f = autowrap(expr, args=(x,), backend='cython')

f(np.array([[1.0, 2.0]]))
```

### `[[A2]]` (code)

```python
TypeError: only size-1 arrays can be converted to Python scalars
```

### `[[A3]]` (code)

```C
double autofunc(double x) {

   double autofunc_result;
   autofunc_result = 1.0;
   return autofunc_result;

}
```

### `[[A4]]` (code)

```python
from sympy.utilities.autowrap import autowrap
from sympy import MatrixSymbol
import numpy as np

x = MatrixSymbol('x', 2, 1)
# now output depends on x
expr = x[0,0]
f = autowrap(expr, args=(x,), backend='cython')

# returns 1.0 as expected, without failure
f(np.array([[1.0, 2.0]]))
```
