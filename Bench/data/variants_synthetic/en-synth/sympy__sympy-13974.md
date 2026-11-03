powers of TensorProduct expressions can't be evaluated, e.g. tp(1,1)*tp(1,1). neither expand(tensorproduct=True) nor tensor_product_simp simplifies them, the output just stays 1x1**2 / 1xsigma3**2. example session (TensorProduct, tensor_product_simp, Pauli(3) and a noncommutative a):
[[A1]]
what I'd expect is what you see in cell [5] for t1 (1x1) and cell [9] for t2 (1x1).
