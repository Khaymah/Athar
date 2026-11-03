`xr.where(..., keep_attrs=True)` كيكتب فوق الـ attrs ديال les coordonnées بالـ attrs ديال الـ data variable.
هادي regression جات من PR #6461 (تبديل صغير فـ `lambda`)، وكنظن خاسرة من `2022.06.0`.
الـ repro: الـ dataset `air_temperature` ديال tutorial، وشوف `.time.attrs` ديال الـ résultat ديال `where`:
[[A1]]
الـ attrs ديال `time` اللي كيطلعو ليا مقارنة مع اللي خاصهم يكونو: [[A2]]
اللي بغيت هو الـ attributes ديال les coordonnées يبقاو كيف ماهوما بلا تبديل.
حاولت نتبع منين جا le problème فـ les couches ديال merge وماقدرتش؛ إلا عندكم شي فكرة ديال fix نقدر نصيفط PR.
l'env: [[A3]] (xarray `2022.10.0`)
