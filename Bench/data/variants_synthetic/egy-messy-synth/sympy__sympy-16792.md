`autowrap` ب `backend='cython'` بايظ لو فى array argument مش ظاهر فى ال`expr` اللى بنعمله wrap
[[A1]]
دا ال repro `MatrixSymbol('x', 2, 1)` ك arg و `expr = 1.0` والمفروض الcall يرجع `1.0` بس بيضرب
[[A2]]
يعنى `TypeError: only size-1 arrays can be converted to Python scalars` والسبب ان ال C function اللى بتتعمل generate الsignature بتاعتها غلط `x` المفروض يبقى `double *` مش `double`
[[A3]]
لو `expr` معتمد ع كل الarguments زى `expr = x[0,0]` بيشتغل تمام
[[A4]]
وانا محتاج دا عشن libs برا زى numerical integration لازم signature ثابته حتى لو فى args مش مستخدمه وشاكك ان المشكله فى `codegen` اصلا
