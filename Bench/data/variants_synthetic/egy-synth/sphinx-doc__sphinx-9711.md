الـ needs_extensions بتقارن الـ versions بتاعة الـ extensions كـ strings مش كـ versions، فـ '0.6' > '0.10' كـ string، وبالتالي الـ versions الأحدث (زي لما الـ minor يعدّي 9) بتترفض غلط.
تقدر تجربها على mplcursors:
[[A1]]
كده الـ build بيعدّي عادي طالما sphinx-gallery متعمله pin على 0.9. بس لما أعمل upgrade لـ 0.10:
[[A2]]
الـ build بيقع بـ version error إنه "not new enough":
[[A3]]
المفروض sphinx_gallery.gen_gallery 0.10.0 يتقبل طالما الـ minimum هو 0.6.0. أنا على Sphinx 4.1.2.
