el evalf byo2a3 b UnboundLocalError (reprec referenced before assignment) fe sympy/core/evalf.py, w el ghareeb eno bye3temed 3ala tarteeb el args beta3et Mul: Mul(x, Max(0, y), evaluate=False).evalf() shaghala 3ady, enama Mul(Max(0, y), x, ...) btedrab. el session w el traceback:
[[A1]]
el Max malhash entry fe evalf_table (KeyError: Max), w ba3daha el error byes7al fe el fallback path. le2eet da ba3d ma ghayart tarteeb el args beta3et Mul fe sympy PR #13059.
e2tera7y en el elif clauses elly bt7ot reprec/imprec me7taga else: raise NotImplementedError, w da shaklo 7allaha 3andy. bas madawartesh leh tarteeb el args fare2.
