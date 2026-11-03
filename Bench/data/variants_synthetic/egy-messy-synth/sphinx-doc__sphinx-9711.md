`needs_extensions` بيقارن versions الextensions ك strings مش ك versions ف `'0.6' > '0.10'` كنصوص و بالتالى اى version جديده (مثلا minor اكبر من 9) بتترفض غلط
جرب mplcursors [[A1]] بيعمل build عادى و sphinx-gallery pinned على 0.9 bs اول ما تعمل upgrade ل sphinx-gallery 0.10 [[A2]] الbuild بيقع بerror بتاع version "not new enough" [[A3]]
المفروض `sphinx_gallery.gen_gallery` 0.10.0 يتقبل طالما الminimum 0.6.0
Sphinx 4.1.2
