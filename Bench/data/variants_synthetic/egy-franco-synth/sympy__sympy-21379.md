bytal3li `PolynomialError: Piecewise generators do not make sense` mn expr.subs({1: 1.0}) w msh fahem leh, wel expression howa exp(sinh(Piecewise((x, y > x), (y, True)) / z)). da MWE:
[[A1]]
byfshal bas lama x w y ykono real=True wel cache metmasa7, w law 3amalt nafs el subs tany wel cache warm byshtghal. w law 7atteet cosh aw tanh badal sinh bardo byfshal. law sheelt el 2esma 3ala z aw el exp elly barra el error bye5tefi, bas unary funcs tanya barra zay sin aw log bardo btefshal. wel z msh lazem tkoon real.
ana ba3mel keda 3shan ba7awel el int atoms le float 2abl el lambdify bta3 tensorflow. el version: sympy 1.8.dev
