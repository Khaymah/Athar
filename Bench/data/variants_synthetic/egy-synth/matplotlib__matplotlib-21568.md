الـ datetime axis مع `usetex=True` الـ spacing بتاع الـ tick labels بقى مش واضح في matplotlib 3.4 مقارنةً بـ 3.3.
ده الـ repro script، بيشغّل `text.usetex` وبيرسم pandas date range قصير وبيعمل save لـ PNG باسم الـ version:
[[A1]]
ودي الصور، 3.3.4: [[A2]]
و 3.4.3: [[A3]]
أنا عايز الـ spacing يبقى زي 3.3 بس برضه يفضل متعمله render بالـ TeX format. الـ env: matplotlib 3.4.3 على Windows من conda-forge
