evalf crashes with UnboundLocalError (reprec referenced before assignment) in sympy/core/evalf.py, and it depends on the Mul arg order: Mul(x, Max(0, y), evaluate=False).evalf() is ok but Mul(Max(0, y), x, ...) fails. session + traceback:
[[A1]]
Max has no evalf_table entry (KeyError: Max), and then it errors in the fallback path. found this after reordering Mul args in sympy PR #13059.
my suggestion: the elif clauses that set reprec/imprec need an else: raise NotImplementedError, that seemed to fix it. didn't investigate why the arg order matters though.
