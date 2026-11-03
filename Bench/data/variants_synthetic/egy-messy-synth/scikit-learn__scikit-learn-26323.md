`ColumnTransformer.set_output` بيعدى الsetting للsub-transformers كلهم bs بيطنش الestimator اللى متباصى فى `remainder` ف النتيجه ان شرط `if` وقت تجميع النتايج فى `sklearn/compose/_column_transformer.py` حوالى L853 بيفشل والoutput النهائى بيتجمع غلط
الrepro فى [[A1]] بقارن `remainder=VarianceThreshold()` بنفس الtransformer مكتوب صريح و الاتنين ب `set_output(transform="pandas")`
اللى حاصل فى حالة الremainder العمود `a` بيطلع ints `1/0` [[A3]] .. المفروض الاتنين يطلعو زى بعض بالظبط و العمود `a` اللى هو bool يفضل `True/False` [[A2]]
الenv sklearn 1.2.2 و pandas 2.0.1 التفاصيل [[A4]]
