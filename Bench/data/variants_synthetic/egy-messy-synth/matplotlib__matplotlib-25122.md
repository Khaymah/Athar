طالع `4372.942556173262` و المفروض `0` el bug ف `mlab._spectral_helper` الwindow correction بتتحسب غلط الكود ف `lib/matplotlib/mlab.py` حولين L423-430
الموضوع ان `np.abs` اللى بيتعمل على الwindow هناك ملوش لزمه و بيبوظ اى window فيها قيم سالبه زى `flattop` بص على scipy ف `scipy/signal/_spectral_py.py` msh bystakhdemo abs
الrepro بيقارن مربع المجموع ب `np.abs` و من غيرها ل `signal.windows.flattop(512)`
[[A1]]
و ده حاصل ف اخر نسخه من Matplotlib كمان
