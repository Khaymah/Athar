`ColumnTransformer.set_output` كيدوز الإعداد للـ sub-transformers ولكن كينسى الـ estimator اللي معطي ف `remainder`.
والنتيجة: واحد الـ check ديال `if` ملي كيجمع les résultats ف `sklearn/compose/_column_transformer.py` (تقريبا L853) كيطيح، والـ output النهائي كيتركب غالط.
الـ repro ف [[A1]]: كنقارن `remainder=VarianceThreshold()` مع نفس الـ transformer محطوط صراحة، وجوج بـ `set_output(transform="pandas")`.
كنتسنا جوج outputs يكونو بحال بحال، والعمود `a` اللي هو bool يبقى `True/False` [[A2]].
ولكن اللي كيطلع ليا: ف حالة remainder العمود `a` كيولي ints `1/0` [[A3]].
l'env: sklearn 1.2.2 و pandas 2.0.1، التفاصيل ف [[A4]].
