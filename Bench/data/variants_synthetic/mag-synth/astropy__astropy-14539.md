السلام، عندي واحد le bug غريب ف `io.fits.FITSDiff`: كيقول ليا بلي كاينين différences بين fichiers متطابقين، حتى ملي كنقارن الملف مع راسو.
باش تعاودها: كنصاوب `BinTableHDU` فيه colonne VLA ب `format='QD'`، ومن بعد كنقارن الملف مع راسو ب `FITSDiff` و `fits.printdiff`:
[[A1]]
وهادشي اللي كيطلع ليا، `.identical` كتعطي `False` وكيقول بلي الdata ديال la colonne `a` مختلفة ف row 0:
[[A2]]
المفروض مايبان حتى فرق إلا إلا كان كاين بصح، والملف مع راسو عمرو ما خاصو يطلع مختلف.
كنشك بلي المشكل ف la gestion ديال VLA (variable-length array)، حيت بلا colonne VLA ماقدرتش نعاود le bug.
هادشي على astropy `5.2.1`.
