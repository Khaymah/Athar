السلام، عندي مشكل فـ `mlab._spectral_helper`: la correction ديال الـ window كتتحسب غالطة، الكود فـ `lib/matplotlib/mlab.py` تقريبا L423-430.
الـ `np.abs` اللي كيتطبق على الـ window تما ماخاصوش يكون أصلا، وكيخسر الـ windows اللي فيهم قيم سالبة بحال `flattop`.
للمقارنة شوف l'implémentation ديال scipy فـ `scipy/signal/_spectral_py.py`، ماكيديروش فيها abs.
هاد الـ repro كيقارن مربع الـ sum مع `np.abs` وبلا بيه على `signal.windows.flattop(512)`:
[[A1]]
كيطلع ليا `4372.942556173262` والمفروض يطلع `0`. le bug باقي كاين حتى فآخر version ديال Matplotlib.
