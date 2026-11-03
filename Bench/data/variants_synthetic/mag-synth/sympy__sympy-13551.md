`Product(n + 1 / 2**k, [k, 0, n-1]).doit()` كيرجع ليا closed form غالطة.
شوف الـ repro والنتائج الغالطين (الـ simplify والقيمة ديال `n=2`):
[[A1]]
القيمة الصحيحة ملي `n=2` خاصها تكون `(2 + 2^0) * (2 + 2^(-1)) = 15/2`.
صاحب l'issue كيقول بلي l'expression الصحيحة فيها الـ q-Pochhammer symbol، وها الرابط ديال WolframAlpha: https://www.wolframalpha.com/input/?i=product+of+n+%2B+1%2F2%5Ek+from+k%3D0+to+n-1
