the axis offset text (the exponent label) ignores `xtick.labelcolor` / `ytick.labelcolor` when I set them in rcParams or a style, it gets colored from `xtick.color` / `ytick.color` instead. matplotlib 3.6.3.
repro, `ytick.labelcolor` set to red and values around 1e9:
[[A1]]
what I get, exponent label isn't red: [[A2]]
what I expect, it's red: [[A3]]
I patched `axis.py` like this and it works for my simple cases: [[A4]]
can you look into it?
