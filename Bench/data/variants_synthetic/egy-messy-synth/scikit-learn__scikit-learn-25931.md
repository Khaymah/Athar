بص يا عم لما بعمل `IsolationForest.fit()` على `pd.DataFrame` بيطلعلى الwarning ده [[A1]] و ده بيحصل bs لما `contamination` تبقا مش الdefault ya3ni مش `"auto"` الwarning ده غلط اصلن لان X فيها feature names سليمه و هو طالع من `fit()` مش من predict على ndarray
الrepro اهو [[A2]] المفروض مايطلعش الwarning ده خالص وقت `fit`
انا شاكك ان لما `contamination != "auto"` الfit بتنادى predict على الtraining data عشن تحسب `offset_` فى `sklearn/ensemble/_iforest.py` حوالى L337 msh mot2aked bs
الenv sklearn 1.2.1 و pandas 1.5.3 والversions كلها فى [[A3]]
