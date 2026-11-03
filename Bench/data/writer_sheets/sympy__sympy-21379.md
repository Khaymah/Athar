# sympy__sympy-21379

**Repo:** `sympy/sympy`

## What the request must convey (all units, nothing extra)

1. `expr.subs({1: 1.0})` raises unexpected `PolynomialError: Piecewise generators do not make sense`
2. expression: `exp(sinh(Piecewise((x, y > x), (y, True)) / z))`; MWE in [[A1]]
3. fails only when `x`, `y` are `real=True` and cache cleared; second identical `subs` call (cache warm) succeeds
4. also fails with `cosh` or `tanh` instead of `sinh`
5. error disappears if division by `z` or the outer `exp` removed; other outer unary funcs (`sin`, `log`) still fail
6. `z` need not be real; context: casting int atoms to float before tensorflow `lambdify`
7. sympy 1.8.dev

## Attachments (paste the placeholder where you would paste the block)

### `[[A1]]` (code)

```python
from sympy import *
from sympy.core.cache import clear_cache

x, y, z = symbols('x y z')

clear_cache()
expr = exp(sinh(Piecewise((x, y > x), (y, True)) / z))
# This works fine
expr.subs({1: 1.0})

clear_cache()
x, y, z = symbols('x y z', real=True)
expr = exp(sinh(Piecewise((x, y > x), (y, True)) / z))
# This fails with "PolynomialError: Piecewise generators do not make sense"
expr.subs({1: 1.0})  # error
# Now run it again (isympy...) w/o clearing cache and everything works as expected without error
expr.subs({1: 1.0})
```
