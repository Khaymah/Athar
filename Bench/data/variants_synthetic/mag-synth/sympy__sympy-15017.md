`sympy.tensor.array.NDimArray.__len__` ديما كيرجع `0` للـ arrays ديال rank-0 (scalar).
شوف هاد الـ repro: `len` ديال `Array` scalar كيعطي 0، ولكن ملي كندير iteration عليه كيعطيني element واحد:
[[A1]]
المنطقي هو `len` يكون 1، يعني عدد les éléments لي كيعطي الـ iterator، بحال numpy:
[[A2]]
جربت هادشي على sympy 1.2-rc1 و Python 3.6.6.
