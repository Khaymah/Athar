الـ len() على array من rank-0 (scalar يعني) دايمًا بيرجّع 0. الـ sympy.tensor.array.NDimArray.__len__ بيدّيني 0، مع إن لما بعمل iterate عليه بيطلع element واحد:
[[A1]]
المفروض يرجّع 1، يعني عدد الـ elements اللي بيطلعها الـ iterator، زي numpy بالظبط:
[[A2]]
جربت ده على sympy 1.2-rc1 و Python 3.6.6
