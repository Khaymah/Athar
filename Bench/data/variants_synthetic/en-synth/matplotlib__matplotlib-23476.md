figure `dpi` doubles every time the figure is unpickled, MacOSX backend on an M1 Mac. repro pickles/unpickles the same figure 32 times in a loop and prints `fig.dpi`:
[[A1]]
what I get: dpi goes 200 -> 400 -> 800 ... and then `OverflowError: signed integer is greater than maximum` from `backend_macosx` `FigureCanvas.__init__` via `Figure.__setstate__`
[[A2]]
what I'd expect, dpi stays `200.0` after every round trip:
[[A3]]
env: matplotlib 3.5.2, macOS 12.4 arm64. only happens on M1 MacBooks, python version doesn't matter
