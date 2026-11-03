looks like `annotate` with arrows keeps the array I pass as `xy` by reference instead of copying it, so if I mutate that array after the call the arrow position changes.
[[A1]]
in this repro the first arrow moves after I edit the array, the second one (given `.copy()`) is unaffected. result: [[A2]]
both arrows should stay horizontal.
env: matplotlib 3.0.3, Qt5Agg, Python 3.5.3, Debian 9
