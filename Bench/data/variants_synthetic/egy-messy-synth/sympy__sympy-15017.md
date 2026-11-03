`sympy.tensor.array.NDimArray.__len__` دايما بيرجع `0` لو الarray rank-0 يعنى scalar
[[A1]]
اهو `len` بتاع `Array` scalar بيدى 0 بس لو لفيت عليه iteration بيطلع element واحد ف المفروض `len` يبقى 1 اللى هو عدد العناصر اللى بيطلعها الiterator زى numpy بالظبط
[[A2]]
جربت ع sympy 1.2-rc1 و Python 3.6.6
