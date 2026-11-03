في مشكلة في `mlab._spectral_helper`، الـ window correction بيتحسب غلط (الكود حوالين `lib/matplotlib/mlab.py` L423-430).
فيه `np.abs` متطبق على الـ window هناك وملوش لازمة، وبيبوّظ الـ windows اللي فيها قيم سالبة زي `flattop`. لو عايز تقارن، الـ implementation بتاع scipy في `scipy/signal/_spectral_py.py` مفيهوش abs خالص.
ده repro بيقارن الـ squared sum بالـ `np.abs` ومن غيره لـ `signal.windows.flattop(512)`:
[[A1]]
بيطلعلي `4372.942556173262` والمفروض يطلع `0`. وده على آخر نسخة من Matplotlib.
