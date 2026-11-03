الـ powers بتاعة الـ TensorProduct expressions مش بتتحسب خالص، زي tp(1,1)*tp(1,1). لا expand(tensorproduct=True) ولا tensor_product_simp بيبسّطوها، والـ output بيفضل زي ما هو 1x1**2 أو 1xsigma3**2. دي session فيها TensorProduct و tensor_product_simp و Pauli(3) و a اللي هو noncommutative:
[[A1]]
النتايج اللي أنا مستنيها هي اللي في الخلية [5] بتاعة t1 (بتطلع 1x1) والخلية [9] بتاعة t2 (بتطلع 1x1).
