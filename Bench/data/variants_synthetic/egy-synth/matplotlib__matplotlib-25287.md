الـ offset text بتاع الـ axis (الـ exponent label يعني) مش بيحترم `xtick.labelcolor` / `ytick.labelcolor` لما بحطهم في الـ rcParams أو في style، وبياخد لونه من `xtick.color` / `ytick.color` بدالهم. أنا على Matplotlib 3.6.3.
ده الـ repro، حاطط `ytick.labelcolor` بـ red والقيم حوالين 1e9:
[[A1]]
اللي بيطلعلي دلوقتي، الـ exponent label مش أحمر: [[A2]]
واللي المفروض يطلع، أحمر: [[A3]]
عملت patch كده في `axis.py` وشغال معايا في الحالات البسيطة بتاعتي: [[A4]]
ممكن تبصلي عليها؟
