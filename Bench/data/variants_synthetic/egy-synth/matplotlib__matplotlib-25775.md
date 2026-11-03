عايز أعمل حاجة في `Text`: دلوقتي الـ antialiasing بتاعه بيتقري دايماً من الـ global `rcParams["text.antialiased"]`، مع إن باقي الـ artists ينفع تتحكم فيهم كل واحد لوحده بـ `set_antialiased` / `get_antialiased`.
ضيف `get_antialiased` / `set_antialiased` لـ `Text`، ولو محتاج تعدّل `Annotation` كمان عدّله. والمهم إن القيمة اللي على الـ artist تتستخدم فعلاً وقت الـ draw.
على فكرة غالباً الـ backends هتحتاج تتعدل، يعني بدل ما بيقروا `rcParams["text.antialiased"]` على طول يقروها من الـ state بتاعة الـ `GraphicsContext`.
