`IterativeImputer` مفيهوش parameter اسمه `fill_value`.
الـ docs بتقول إن `initial_strategy` زي الـ strategy بتاعة `SimpleImputer`، بس لو اخترت `initial_strategy="constant"` مفيش أي طريقة أحدد بيها الـ constant.
للعلم `SimpleImputer.fill_value` بيتستخدم مع `strategy="constant"`، والـ default بتاعه 0 للـ numeric و`"missing_value"` للـ str/object.
ممكن تضيف `fill_value` لـ `IterativeImputer` ويتستخدم لما `initial_strategy="constant"`؟ وخلي `np.nan` مسموح كـ `fill_value` كمان، عشان الـ decision tree-based estimators.
