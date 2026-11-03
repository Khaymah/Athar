`evalf` بيضرب `UnboundLocalError` (`reprec` referenced before assignment) فى `sympy/core/evalf.py` و ده حسب ترتيب الargs بتاعت `Mul` ya3ni `Mul(x, Max(0, y), evaluate=False).evalf()` شغاله تمام bs `Mul(Max(0, y), x, ...)` بتقع الsession و الtraceback فى [[A1]]
`Max` ملوش entry فى `evalf_table` (`KeyError: Max`) و بعدين الerror بيحصل فى الfallback path
لقيتها لما غيرت ترتيب الargs بتاعت `Mul` فى sympy PR #13059
اقتراحى ان الclauses بتاعت `elif` اللى بتحط `reprec`/`imprec` محتاجه `else: raise NotImplementedError` و شكلها حلت المشكله bs مدورتش ليه الترتيب فارق
