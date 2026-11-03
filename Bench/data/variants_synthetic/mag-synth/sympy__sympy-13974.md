الـ powers ديال les expressions ديال `TensorProduct` ماكيتحسبوش، بحال `tp(1,1)*tp(1,1)`.
لا `expand(tensorproduct=True)` لا `tensor_product_simp` كيبسطوهم، الـ output كيبقى `1x1**2` ولا `1xsigma3**2` كيف ما هو.
هاهي session فيها `TensorProduct` و`tensor_product_simp` و`Pauli(3)` و`a` لي هو noncommutative:
[[A1]]
النتيجة لي كنتسناها كاينة فنفس الـ session فـ الخلية `[5]` (`t1` خاصو يعطي `1x1`) وفـ `[9]` (`t2` حتى هو خاصو يعطي `1x1`).
