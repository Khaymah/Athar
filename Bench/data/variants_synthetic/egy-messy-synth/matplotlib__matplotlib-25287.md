الoffset text بتاع الaxis (اللى هو label الexponent) مش بيسمع كلام `xtick.labelcolor` / `ytick.labelcolor` لما تحطهم ف rcParams او ف style بياخد لونه من `xtick.color` / `ytick.color` بدالهم ده علي Matplotlib 3.6.3
الكود اهو `ytick.labelcolor` معموله red و برسم قيم حولين 1e9
[[A1]]
ده اللى طالع الexponent msh a7mar [[A2]] و ده المفروض يبقا احمر [[A3]]
انا عملت patch ف `axis.py` شغاله معايا ف الحالات البسيطه [[A4]]
