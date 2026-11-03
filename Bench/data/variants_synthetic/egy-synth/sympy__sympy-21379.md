بيطلعلي `PolynomialError: Piecewise generators do not make sense` من expr.subs({1: 1.0}) ومش فاهم ليه، والـ expression هو exp(sinh(Piecewise((x, y > x), (y, True)) / z)). ده MWE:
[[A1]]
بيفشل بس لما x و y يكونوا real=True والـ cache متمسّح، ولو عملت نفس الـ subs تاني والـ cache warm بيشتغل. ولو حطيت cosh أو tanh بدل sinh برضه بيفشل. لو شيلت القسمة على z أو الـ exp اللي بره الـ error بيختفي، بس unary funcs تانية بره زي sin أو log برضه بتفشل. والـ z مش لازم تكون real.
أنا بعمل كده عشان بحوّل الـ int atoms لـ float قبل الـ lambdify بتاع tensorflow. الـ version: sympy 1.8.dev
