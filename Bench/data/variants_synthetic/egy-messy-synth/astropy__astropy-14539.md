ya gama3a `io.fits.FITSDiff` بيقول ان فى differences بين فايلات زى بعض بالظبط حتي لما بقارن الفايل بنفسه
ده على astropy `5.2.1` بالمناسبه
عملت `BinTableHDU` فيه column VLA ب `format='QD'` وقارنت الفايل بنفسه ب `FITSDiff` و `fits.printdiff` اهو [[A1]]
والى طلع `.identical` طلعت `False` وبيقول ان الداتا بتاعت column `a` مختلفه فى row 0 [[A2]]
انا شاكك ان المشكله فى الهاندلنج بتاع VLA يعنى variable-length array عشن من غير column VLA msh bey7sal
el mafrod ميطلعش فرق غير لو فى فرق فعلا والفايل مع نفسه عمره ما يبقى مختلف
