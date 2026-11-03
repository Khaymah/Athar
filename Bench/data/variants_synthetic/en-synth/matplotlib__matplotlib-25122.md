hey, the window correction in `mlab._spectral_helper` is computed wrong, code is around `lib/matplotlib/mlab.py` L423-430.
there's an `np.abs` applied to the window there that's unnecessary, and it breaks windows that have negative values, e.g. `flattop`. for reference, scipy's implementation in `scipy/signal/_spectral_py.py` has no abs.
quick repro, compares the squared sum with and without `np.abs` for `signal.windows.flattop(512)`:
[[A1]]
I get `4372.942556173262`, expected `0`. this is on latest Matplotlib.
