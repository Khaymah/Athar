fi moshkla fi `mlab._spectral_helper`, el window correction byet7seb ghalat (el code 7awalein `lib/matplotlib/mlab.py` L423-430).
fih `np.abs` metabba2 3al window hnak w malosh lazma, w biybawaz el windows elly fiha 2iyam salba zay `flattop`. law 3ayez te2aren, el implementation bta3 scipy fi `scipy/signal/_spectral_py.py` mafihoosh abs 5ales.
da repro bi2aren el squared sum bel `np.abs` w men gheiro le `signal.windows.flattop(512)`:
[[A1]]
biytla3li `4372.942556173262` w el mafrood yetla3 `0`. w da 3ala a5er noskha men Matplotlib.
