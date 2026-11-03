شكل `annotate` لما بيكون فيه arrows بيحتفظ بالـ array اللي باديهوله في `xy` بالـ reference مش بياخد copy منه، فلو غيرت في الـ array بعد الـ call مكان الـ arrow بيتغير.
[[A1]]
في الـ repro ده أول arrow بيتحرك بعد ما بعدّل الـ array، والتاني اللي اديتله `.copy()` مبيتأثرش. النتيجة: [[A2]]
المفروض الاتنين يفضلوا horizontal.
الـ env: matplotlib 3.0.3, Qt5Agg, Python 3.5.3, Debian 9
