# scikit-learn__scikit-learn-25232

**Repo:** `scikit-learn/scikit-learn`

## What the request must convey (all units, nothing extra)

1. `IterativeImputer` has no `fill_value` parameter
2. `initial_strategy="constant"` documented as same as `SimpleImputer` strategy, but constant can't be chosen
3. `SimpleImputer.fill_value`: used for `strategy="constant"`, default 0 for numeric, `"missing_value"` for str/object
4. request: add `fill_value` to `IterativeImputer`, used when `initial_strategy="constant"`
5. also allow `np.nan` as `fill_value` (for decision tree-based estimators)

## Attachments (paste the placeholder where you would paste the block)

_None: the request is prose only._
