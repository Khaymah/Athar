sylow_subgroup() in sympy.combinatorics raises IndexError for some dihedral groups. DihedralGroup(18) with p=2 dies inside minimal_blocks():
[[A1]]
same error with this one too (DihedralGroup(2*25), p=2):
[[A2]]
it should just return the Sylow subgroup without erroring. env: sympy 1.6.1, numpy 1.18.5, scipy 1.4.1, Python 3.8.5 on Windows 64-bit
