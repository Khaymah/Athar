`_check_homomorphism` ماخدامش مع les `PermutationGroup`s.
الـ repro: `homomorphism(D3, D3, D3.generators, D3.generators)` مع `D3 = DihedralGroup(3)` كيطلع `ValueError`:
[[A1]]
المشكل جاي من `_image()` الداخلية فـ `sympy/combinatorics/homomorphisms.py` (L336-337)، فـ la branche ديال `PermutationGroup`: ملي كيكون `r[i]` generator مقلوب (inverted)، الـ check ديال `in gens` كيفشل.
وكنظن بلي هاد la logique يمكن تتبسط بزاف.
