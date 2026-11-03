`xr.where(..., keep_attrs=True)` بيكتب attrs الـ data variable فوق الـ attrs بتاعة الـ coordinates.
ده regression من PR #6461 (كان تغيير بسيط في `lambda`)، وغالباً بايظ من أيام `2022.06.0`.
الـ repro بالـ tutorial dataset `air_temperature`، بص على `.time.attrs` بتاعة نتيجة الـ `where`:
[[A1]]
الـ `time` attrs اللي بتطلع واللي المفروض تطلع: [[A2]]
المفروض الـ attributes بتاعة الـ coordinates تفضل زي ما هي من غير تغيير. حاولت أتتبع السبب جوه طبقات الـ merge ومعرفتش، ولو عندك فكرة للـ fix أنا ممكن أبعت الـ PR.
الـ env: [[A3]] (xarray `2022.10.0`)
