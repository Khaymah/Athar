`xr.where(..., keep_attrs=True)` بيكتب علي attrs الcoordinates بattrs الdata variable
دى regression من PR #6461 كان تغيير بسيط ف `lambda` و غالبا بايظه من `2022.06.0`
الكود ع الdataset `air_temperature` من الtutorial بص على `.time.attrs` بتاعت نتيجه `where`
[[A1]]
attrs `time` اللى طالعه و اللى المفروض تطلع ف [[A2]] المفروض attributes الcoordinates تفضل زى ماهى متغيرش
حاولت اتتبع السبب جوه طبقت الmerge ma3reftsh لو حد عنده فكره للfix ممكن ابعت PR
env [[A3]] xarray `2022.10.0`
