عندي مشكل مع `IsolationForest.fit()`: ملي كندير fit على `pd.DataFrame` كيطلع ليا هاد le warning: [[A1]]
وهادشي كيوقع غير ملي كنعطي `contamination` شي valeur ماشي ديال default، يعني ماشي `"auto"`.
le warning غالط: X فيها feature names صحاح، وهو كيخرج من `fit()` ماشي من predict على شي ndarray.
كنظن (ماشي متأكد) بلي ملي `contamination != "auto"` la fonction fit كتعيط على predict على الـ training data باش تحسب `offset_`، شوف `sklearn/ensemble/_iforest.py` تقريبا L337.
الـ repro هنا [[A2]]، واللي كنتسنا هو ما يطلع حتى warning بحال هادا وقت `fit`.
l'env: sklearn 1.2.1 و pandas 1.5.3، les versions كاملين ف [[A3]].
