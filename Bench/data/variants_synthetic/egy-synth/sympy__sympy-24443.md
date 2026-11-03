الـ _check_homomorphism بايظ مع الـ PermutationGroups. لو D3 = DihedralGroup(3)، الـ homomorphism(D3, D3, D3.generators, D3.generators) بيرمي ValueError:
[[A1]]
المشكلة في الـ _image() الداخلية في sympy/combinatorics/homomorphisms.py (L336-337)، في الـ branch بتاع الـ PermutationGroup: لما r[i] يبقى generator معكوس (inverted) الـ check بتاع `in gens` بيفشل. وأنا شايف إن اللوجيك ده ممكن يتبسّط جامد.
