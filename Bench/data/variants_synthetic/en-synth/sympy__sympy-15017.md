len() on a rank-0 (scalar) array is always 0. sympy.tensor.array.NDimArray.__len__ returns 0 there, but iterating it gives one element:
[[A1]]
it should be 1, i.e. the number of elements in the iterator, same as numpy does:
[[A2]]
this is on sympy 1.2-rc1, Python 3.6.6
