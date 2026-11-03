سلام، الـ `dpi` ديال la figure كيتضاعف كل مرة كندير ليها unpickle، ف backend MacOSX على Mac M1.
le repro: كندير pickle/unpickle لنفس la figure 32 مرة ف boucle وكنطبع `fig.dpi` [[A1]]
شنو كيطرا [[A2]]: الـ dpi كيمشي 200 -> 400 -> 800 ... ومن بعد كيطيح بـ `OverflowError: signed integer is greater than maximum` من `FigureCanvas.__init__` ف `backend_macosx` عن طريق `Figure.__setstate__`.
المفروض [[A3]]: الـ dpi يبقى `200.0` من بعد كل aller-retour.
Env: matplotlib 3.5.2، macOS 12.4 arm64؛ غير ف MacBooks M1، والـ version ديال Python ماعندها حتى علاقة.
