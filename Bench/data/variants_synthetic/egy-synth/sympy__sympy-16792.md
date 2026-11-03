الـ autowrap بالـ backend='cython' بيبوظ لما يكون فيه array argument مش موجود في الـ expr اللي بعمله wrap. ده الـ repro، الـ x عبارة عن MatrixSymbol('x', 2, 1) والـ expr = 1.0، يعني المفروض الـ call يرجّع 1.0:
[[A1]]
بس بدل كده بيطلعلي:
[[A2]]
المشكلة إن الـ C function اللي بتتولّد الـ signature بتاعها غلط، الـ x المفروض تبقى `double *` مش `double`:
[[A3]]
لو الـ expr معتمد على كل الـ arguments (زي expr = x[0,0]) بيشتغل عادي:
[[A4]]
أنا محتاج ده عشان فيه external libs (numerical integration مثلًا) عايزة signature ثابت حتى لو فيه args مش مستخدمة. وشاكك إن الـ bug في الـ codegen.
