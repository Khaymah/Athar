لما بعمل IsolationForest.fit() على pd.DataFrame بيطلعلي الـ warning ده:
[[A1]]
وده بيحصل بس لما الـ contamination تبقى قيمة غير الـ default، يعني مش "auto". الـ warning غلط أصلاً، الـ X فيها feature names سليمة، وهو طالع من fit() نفسها مش من predict على ndarray.
أنا شاكك إن لما contamination != "auto" الـ fit بتنادي predict على الـ training data عشان تحسب offset_ (في sklearn/ensemble/_iforest.py حوالين L337).
الـ repro:
[[A2]]
المفروض مايطلعش الـ warning ده خالص وقت الـ fit. أنا على sklearn 1.2.1 و pandas 1.5.3، والـ versions كلها هنا:
[[A3]]
