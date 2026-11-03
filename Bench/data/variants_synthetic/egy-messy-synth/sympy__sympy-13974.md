الpowers بتاعه `TensorProduct` مش بتتحسب خالص زى `tp(1,1)*tp(1,1)` جربت `expand(tensorproduct=True)` وجربت `tensor_product_simp` ولا واحده فيهم بتبسط حاجه الناتج بيفضل `1x1**2` او `1xsigma3**2` زى ماهو
[[A1]]
دى session فيها `TensorProduct` و `tensor_product_simp` و `Pauli(3)` و `a` noncommutative والمتوقع موجود فى نفس الsession فى الخليه `[5]` لـ `t1` المفروض تطلع `1x1` و `[9]` لـ `t2` بردو `1x1`
