_check_homomorphism is broken for PermutationGroups. with D3 = DihedralGroup(3), homomorphism(D3, D3, D3.generators, D3.generators) raises ValueError:
[[A1]]
the culprit is the internal _image() in sympy/combinatorics/homomorphisms.py (L336-337), the PermutationGroup branch: when r[i] is an inverted generator the `in gens` check fails. I think that logic can be simplified a lot.
