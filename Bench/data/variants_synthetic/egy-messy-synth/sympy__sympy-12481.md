الconstructor بتاع `Permutation` بيرفض الcycles اللى مش disjoint ya3ni `Permutation([[0,1],[0,1]])` بيضرب `ValueError` مع ان المفروض يرجع الidentity permutation
المفروض لو الcycles مش disjoint تتطبق بالترتيب من الشمال لليمين و يرجع الpermutation اللى طلعت
وانا مش شايف اى سبب نمنع الnon-disjoint cycles اصلن
