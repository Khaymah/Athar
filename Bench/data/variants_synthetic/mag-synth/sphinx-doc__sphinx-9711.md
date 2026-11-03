`needs_extensions` كيقارن les versions ديال الـ extensions بحال strings، ماشي بحال versions.
النتيجة: كـ strings `'0.6' > '0.10'`، يعني les versions الجداد (مثلا minor فوق 9) كيترفضو بلا سبب.
الـ repro ف الـ projet mplcursors [[A1]]: كيتبنى مزيان مع sphinx-gallery 0.9 pinned.
ملي كنطلع لـ sphinx-gallery 0.10 [[A2]]، الـ build كيطيح بـ erreur ديال version "not new enough" [[A3]].
اللي خاصو يوقع: `sphinx_gallery.gen_gallery` 0.10.0 يتقبل ملي الـ minimum هو 0.6.0.
l'env: Sphinx 4.1.2.
