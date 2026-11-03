`sylow_subgroup()` فى `sympy.combinatorics` بيرمى `IndexError` مع شوية dihedral groups
[[A1]]
دا مع `DihedralGroup(18)` و `p=2` وبيقع جوا `minimal_blocks()` ونفس الايرور بالظبط بيحصل مع `DihedralGroup(2*25)` و `p=2`
[[A2]]
المفروض يرجعلى الSylow subgroup عادى من غير error
عندى sympy 1.6.1 و numpy 1.18.5 و scipy 1.4.1 و Python 3.8.5 ع Windows 64-bit
