`expr.subs({1: 1.0})` كيطلع ليا `PolynomialError: Piecewise generators do not make sense` وهادشي ماكانش متوقع.
l'expression هي `exp(sinh(Piecewise((x, y > x), (y, True)) / z))`، وهاهو MWE:
[[A1]]
كيطيح غير إلا كانو `x` و `y` `real=True` والـ cache مخوي (cleared)؛ إلا عاودت نفس `subs` مرة ثانية (والـ cache عامر) كتدوز عادي.
حتى مع `cosh` ولا `tanh` بلاصت `sinh` كيطيح.
إلا حيدت القسمة على `z` ولا الـ `exp` لي برا كيمشي l'erreur، ولكن إلا بدلت `exp` بشي unary function أخرى بحال `sin` ولا `log` باقي كيطيح.
`z` ماشي ضروري يكون real. الـ context: كنحول les atomes int لـ float قبل `lambdify` ديال tensorflow. الـ version: sympy 1.8.dev.
