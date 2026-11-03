بص `expr.subs({1: 1.0})` بيضرب `PolynomialError: Piecewise generators do not make sense` ودا مش متوقع خالص
[[A1]]
الexpression هو `exp(sinh(Piecewise((x, y > x), (y, True)) / z))` والغريب انه بيقع بس لو `x` و `y` `real=True` والcache متمسح لو عملت نفس ال`subs` تانى والcache سخن بيعدى عادى ya3ni
و بيقع بردو لو حطيت `cosh` او `tanh` بدل `sinh` ولو شلت القسمه على `z` او شلت ال`exp` اللى برا الايرور بيختفى بس لو حطيت unary function تانيه برا زى `sin` او `log` لسه بيقع
`z` مش لازم تبقى real اصلا انا كنت بحول ال int atoms ل float قبل `lambdify` بتاع tensorflow و دا على sympy 1.8.dev
