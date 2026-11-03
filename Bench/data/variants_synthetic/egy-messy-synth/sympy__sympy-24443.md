`_check_homomorphism` بايظه مع ال `PermutationGroup`s
[[A1]]
يعنى `homomorphism(D3, D3, D3.generators, D3.generators)` و `D3 = DihedralGroup(3)` بيرمى `ValueError` والمشكله من `_image()` اللى جوا فى `sympy/combinatorics/homomorphisms.py` (L336-337) فى حته ال `PermutationGroup` لما `r[i]` يبقى generator معكوس (inverted) الcheck بتاع `in gens` بيفشل
وبصراحه حاسس ان اللوجيك دا ممكن يتبسط جامد
