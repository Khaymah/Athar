coth(log(tan(x))) blows up when I do subs on it. `coth.eval` in sympy/functions/elementary/hyperbolic.py throws a NameError because `cotm` isn't defined:
[[A1]]
same thing happens for x = 2, 3, 5, 6, 8, 9, 11, 12, 13, 15, 18, ... etc. the substitution should just evaluate without an error, can you fix it?
