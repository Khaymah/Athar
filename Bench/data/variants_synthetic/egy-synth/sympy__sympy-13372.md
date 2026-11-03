الـ evalf بيقع بـ UnboundLocalError (reprec referenced before assignment) في sympy/core/evalf.py، والغريب إنه بيعتمد على ترتيب الـ args بتاعة Mul: Mul(x, Max(0, y), evaluate=False).evalf() شغالة عادي، إنما Mul(Max(0, y), x, ...) بتضرب. الـ session والـ traceback:
[[A1]]
الـ Max ملهاش entry في evalf_table (KeyError: Max)، وبعدها الـ error بيحصل في الـ fallback path. لقيت ده بعد ما غيرت ترتيب الـ args بتاعة Mul في sympy PR #13059.
اقتراحي إن الـ elif clauses اللي بتحط reprec/imprec محتاجة else: raise NotImplementedError، وده شكله حلها عندي. بس مدوّرتش ليه ترتيب الـ args فارق.
