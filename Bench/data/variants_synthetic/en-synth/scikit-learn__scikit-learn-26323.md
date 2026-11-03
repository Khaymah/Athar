ColumnTransformer.set_output passes the setting down to the sub-transformers but skips the estimator you give as remainder. because of that, an if check when gathering the results in sklearn/compose/_column_transformer.py (~L853) fails and the final output gets assembled wrong.
repro, remainder=VarianceThreshold() vs the same transformer listed explicitly, both with set_output(transform="pandas"):
[[A1]]
expected both outputs to be identical, with the bool column a kept as True/False:
[[A2]]
but in the remainder case column a comes out as 1/0 ints:
[[A3]]
sklearn 1.2.2, pandas 2.0.1, details:
[[A4]]
