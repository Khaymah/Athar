autowrap with backend='cython' breaks when an array argument doesn't show up in the wrapped expr. repro below, x is MatrixSymbol('x', 2, 1) and expr = 1.0, so the call should just return 1.0:
[[A1]]
instead I get:
[[A2]]
the generated C function has the wrong signature, x should be `double *` not `double`:
[[A3]]
if expr depends on every argument (e.g. expr = x[0,0]) it works fine:
[[A4]]
I need this because external libs (numerical integration etc.) want a fixed signature even when some args are unused. I suspect the bug is in codegen.
