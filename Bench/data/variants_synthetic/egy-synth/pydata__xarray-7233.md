`Dataset.coarsen(...).construct(...)` بيحوّل الـ non-dimensional coordinates لـ data variables.
الـ repro والـ output أهم، عندي coord اسمه `day` على الـ dim `time` وبعدين بعمل `coarsen(time=12).construct(time=("year", "month"))`:
[[A1]]
المفروض أي حاجة كانت coordinate قبل كده تفضل coordinate بعدها. ده على `main`.
