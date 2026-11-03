`sylow_subgroup()` فـ `sympy.combinatorics` كيطلع `IndexError` مع شي dihedral groups.
هاهو الـ repro والـ traceback مع `DihedralGroup(18)` و `p=2`، كيطيح وسط `minimal_blocks()`:
[[A1]]
ونفس l'erreur مع هاد الـ group (`DihedralGroup(2*25)` و `p=2`):
[[A2]]
المفروض يرجع الـ Sylow subgroup بلا حتى error.
l'environnement ديالي: sympy 1.6.1، numpy 1.18.5، scipy 1.4.1، Python 3.8.5 على Windows 64-bit.
