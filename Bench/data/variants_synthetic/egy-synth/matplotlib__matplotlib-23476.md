الـ `dpi` بتاع الـ figure بيتضاعف كل مرة الـ figure يتعمله unpickle، على M1 Mac بالـ MacOSX backend.
الـ repro بيعمل pickle/unpickle لنفس الـ figure 32 مرة في loop وبيطبع `fig.dpi`:
[[A1]]
اللي بيحصل عندي إن الـ dpi بيروح 200 -> 400 -> 800 ... لحد ما يطلعلي `OverflowError: signed integer is greater than maximum` من `FigureCanvas.__init__` في `backend_macosx` عن طريق `Figure.__setstate__`:
[[A2]]
والمفروض الـ dpi يفضل `200.0` بعد كل round trip:
[[A3]]
الـ env: matplotlib 3.5.2 على macOS 12.4 arm64. بتحصل على الـ M1 MacBooks بس، والـ Python version ملهاش علاقة
