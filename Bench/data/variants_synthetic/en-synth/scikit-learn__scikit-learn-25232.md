`IterativeImputer` has no `fill_value` parameter. `initial_strategy` is documented as the same as `SimpleImputer`'s strategy, but with `initial_strategy="constant"` there's no way to choose the constant.
for reference, `SimpleImputer.fill_value` is used for `strategy="constant"`, default 0 for numeric and `"missing_value"` for str/object.
can you add `fill_value` to `IterativeImputer`, used when `initial_strategy="constant"`? and also allow `np.nan` as `fill_value` (for decision tree-based estimators).
