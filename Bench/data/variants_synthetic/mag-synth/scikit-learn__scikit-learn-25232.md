`IterativeImputer` ماعندوش paramètre `fill_value`.
فالدوك `initial_strategy="constant"` مكتوب بلي هي بحال الـ strategy ديال `SimpleImputer`، ولكن ماكاينش كيفاش تختار القيمة constante.
فـ `SimpleImputer.fill_value` كتستعمل مع `strategy="constant"`، والـ default ديالها 0 للأرقام و `"missing_value"` لـ str/object.
بغيت نزيدو `fill_value` لـ `IterativeImputer` وتستعمل ملي يكون `initial_strategy="constant"`.
وزيدو خليو `np.nan` يتقبل كـ `fill_value` (مفيد للـ estimators اللي مبنيين على decision trees).
