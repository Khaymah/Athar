الـ ColumnTransformer.set_output بتعدّي الـ setting للـ sub-transformers بس بتسيب الـ estimator اللي باعته في remainder. وبسبب كده فيه if check وقت تجميع النتايج في sklearn/compose/_column_transformer.py (حوالي L853) بيفشل، والـ output النهائي بيتركّب غلط.
جرب ده، مقارنة بين remainder=VarianceThreshold() ونفس الـ transformer متحط صريح، والاتنين معاهم set_output(transform="pandas"):
[[A1]]
المتوقع إن الاتنين يطلعوا زي بعض بالظبط، والعمود a اللي هو bool يفضل True/False:
[[A2]]
بس اللي بيحصل إن في حالة الـ remainder العمود a بيطلع ints 1/0:
[[A3]]
sklearn 1.2.2 و pandas 2.0.1، والتفاصيل:
[[A4]]
