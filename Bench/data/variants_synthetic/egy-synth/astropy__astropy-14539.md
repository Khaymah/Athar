الـ io.fits.FITSDiff بيطلعلي differences بين files متطابقة، حتى لو بقارن الملف بنفسه. ده الـ repro: عملت BinTableHDU فيه column VLA بـ format='QD' وقارنت الملف بنفسه بـ FITSDiff و fits.printdiff
[[A1]]
وده الـ output، الـ .identical طالعة False وبيقول إن الـ data بتاعة column a مختلفة في row 0
[[A2]]
المفروض يقول فيه differences بس لو فيه فعلاً، والملف مع نفسه عمره ما يختلف. أنا شاكك إن المشكلة في الـ handling بتاع الـ VLA (variable-length array)، لأني مقدرتش أطلّع الـ bug من غير column VLA. أنا على astropy 5.2.1
