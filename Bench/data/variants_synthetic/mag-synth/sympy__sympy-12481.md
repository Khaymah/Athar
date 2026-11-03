الـ constructor ديال `Permutation` كيرفض les cycles اللي ماشي disjoint.
مثلا `Permutation([[0,1],[0,1]])` كيطلع `ValueError`، والمفروض يرجع identity permutation.
بغيت القاعدة العامة تكون: ملي يكونو الـ cycles ماشي disjoint، يتطبقو من اليسار لليمين ويرجع الـ permutation اللي خرجات.
وماشايفش علاش خاصنا نمنعو cycles ماشي disjoint أصلا.
