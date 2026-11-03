hey, when I call IsolationForest.fit() on a pd.DataFrame I get this warning:
[[A1]]
it only happens when contamination is set to something non-default (not "auto"). the warning is just wrong, X does have valid feature names, and it's coming from fit() itself, not from predicting on an ndarray.
my guess: with contamination != "auto", fit calls predict on the training data to set offset_ (sklearn/ensemble/_iforest.py ~L337).
repro:
[[A2]]
I'd expect no such warning during fit. sklearn 1.2.1, pandas 1.5.3, full versions:
[[A3]]
