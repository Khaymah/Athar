الـ constructor بتاع Permutation مش راضي ياخد cycles مش disjoint، يعني Permutation([[0,1],[0,1]]) بيضرب ValueError.
المفروض ده يرجّع الـ identity permutation. وبشكل عام لو الـ cycles مش disjoint يتطبقوا بالترتيب من الشمال لليمين ويرجع الـ permutation اللي هتطلع.
مش شايف أي سبب إننا نمنع الـ non-disjoint cycles أصلاً.
