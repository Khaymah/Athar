`Product(n + 1 / 2**k, [k, 0, n-1]).doit()` بيرجع closed form غلط خالص
[[A1]]
دا الrepro والنتايج الغلط بعد simplify وكمان القيمه عند `n=2` مع ان الصح عند `n=2` هو `(2 + 2^0) * (2 + 2^(-1)) = 15/2` يعنى
الراجل اللى كاتب الissue بيقول ان الexpression الصح فيها q-Pochhammer symbol و حاطط لينك WolframAlpha https://www.wolframalpha.com/input/?i=product+of+n+%2B+1%2F2%5Ek+from+k%3D0+to+n-1
