datetime axis with `usetex=True`: the tick label spacing is unclear in matplotlib 3.4 compared to 3.3. repro script turns `text.usetex` on, plots a short pandas date range and saves a PNG named by version:
[[A1]]
3.3.4: [[A2]]
3.4.3: [[A3]]
expected the 3.3 spacing, but still rendered in TeX format. env is matplotlib 3.4.3, Windows, conda-forge
