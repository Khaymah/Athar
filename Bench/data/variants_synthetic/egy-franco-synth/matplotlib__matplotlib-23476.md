el `dpi` bta3 el figure byetda3ef kol marra el figure yet3amalo unpickle, 3ala M1 Mac bel MacOSX backend.
el repro bye3mel pickle/unpickle le nafs el figure 32 marra fe loop w byetba3 `fig.dpi`:
[[A1]]
elly bey7sal 3andy en el dpi byrou7 200 -> 400 -> 800 ... le7ad ma yetla3li `OverflowError: signed integer is greater than maximum` men `FigureCanvas.__init__` fe `backend_macosx` 3an taree2 `Figure.__setstate__`:
[[A2]]
wel mafrood el dpi yefdal `200.0` ba3d kol round trip:
[[A3]]
el env: matplotlib 3.5.2 3ala macOS 12.4 arm64. bet7sal 3al M1 MacBooks bas, wel Python version malhash 3ala2a
