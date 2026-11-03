getting an unexpected `PolynomialError: Piecewise generators do not make sense` from expr.subs({1: 1.0}) on exp(sinh(Piecewise((x, y > x), (y, True)) / z)). MWE:
[[A1]]
it only fails when x and y are real=True and the cache was cleared; running the same subs a second time (cache warm) works. cosh or tanh instead of sinh fails too. if I drop the division by z or the outer exp the error goes away, but other outer unary funcs like sin or log still fail. z doesn't need to be real.
context: I'm casting int atoms to float before a tensorflow lambdify. sympy 1.8.dev
