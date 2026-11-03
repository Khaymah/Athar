سلام، عندي مشكل فـ `coth.eval` لي كاين فـ `sympy/functions/elementary/hyperbolic.py`: كيطيح (crash) ملي كندير substitution فـ `coth(log(tan(x)))`.
هاهو الكود والـ traceback:
[[A1]]
`.subs(x, 2)` كيطلع ليا `NameError` حيت `cotm` ماشي défini.
وماشي غير 2، حتى x = 2, 3, 5, 6, 8, 9, 11, 12, 13, 15, 18, ... etc كيطيح فيهم نفس le bug.
لي بغيت هو الـ substitution تدوز وتحسب القيمة بلا حتى error.
