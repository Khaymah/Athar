الـ offset text ديال l'axe (الـ label ديال l'exposant) ماكيحترمش `xtick.labelcolor` / `ytick.labelcolor` ملي كنحطهم فـ rcParams ولا فـ style.
بلاصة هادشي كياخد اللون ديالو من `xtick.color` / `ytick.color`، هادشي فـ Matplotlib 3.6.3.
الـ repro: كنحط `ytick.labelcolor` أحمر وكنرسم values قراب لـ 1e9:
[[A1]]
هادا اللي كيطلع ليا، l'exposant ماشي أحمر: [[A2]]
وهادا اللي بغيت، أحمر: [[A3]]
درت واحد patch فـ `axis.py` خدام ليا فالحالات البسيطة ديالي: [[A4]]
