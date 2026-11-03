عندي اقتراح: الـ scales ديال `so.Nominal` (حتى اللي كيتستنتجو automatiquement) خاصهم يتصرفو بحال l'axe catégoriel ديال les plots catégoriels فـ seaborn:
1. الـ limits ديال l'axe يكونو +/- 0.5 على أول وآخر tick، ماشي la logique ديال الـ margins العادية.
2. بلا grid، حتى إلا كان الـ style اللي خدام كيرسمها.
3. إلا كان على l'axe y، نقلبو l'axe.
على l'implémentation: 1 صعيبة شوية، الفكرة اللي عندي هي artist مخفي فيه sticky edges مع margin 0، ولكن hacky، ويمكن نحطو الـ sticky edges على الـ spine.
2 غالبا فـ `Plotter._finalize_figure`، ولكن باقي السؤال: كيفاش الـ user يفرض الـ grid من الـ theme؟ يمكن نحطو الـ grid على الـ scale.
3 ساهلة، ولكن ماعرفتش فين خاصها تكون.
