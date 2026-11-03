ملي كنستعمل `annotate` مع الـ arrows، كيبان ليا بلي l'array اللي كندوزها فـ `xy` كتتخزن par référence، ماكتتنسخش.
إلا بدلت داك l'array من بعد l'appel، الـ position ديال الفليشة كتبدل معاه.
فهاد الـ repro الفليشة الأولى كتتحرك ملي كنبدل l'array، والثانية اللي عطيتها `.copy()` ماكيوقع ليها والو:
[[A1]]
النتيجة: [[A2]]
اللي كنتسنى هو بجوج الفليشات يبقاو horizontal.
l'env: matplotlib 3.0.3، Qt5Agg، Python 3.5.3، Debian 9.
