الـ Product(n + 1 / 2**k, [k, 0, n-1]).doit() بيرجّع closed form غلط. بص ده اللي بيطلعلي، الناتج بعد الـ simplify والقيمة عند n=2:
[[A1]]
عند n=2 المفروض تطلع (2 + 2^0) * (2 + 2^(-1)) = 15/2. وعلى فكرة أنا شايف إن الـ expression الصح فيه الـ q-Pochhammer symbol، بص هنا: https://www.wolframalpha.com/input/?i=product+of+n+%2B+1%2F2%5Ek+from+k%3D0+to+n-1
