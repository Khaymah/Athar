the Permutation constructor rejects non-disjoint cycles, e.g. Permutation([[0,1],[0,1]]) raises a ValueError. I'd expect that to give the identity permutation.
in general, non-disjoint cycles should just be applied in left-to-right order and the resulting permutation returned. I don't see any reason to forbid them.
