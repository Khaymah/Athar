دابا `Text` ديما كياخد l'antialiasing من الـ global `rcParams["text.antialiased"]`، والـ artists لخرين كيخليوك تتحكم فيه لكل artist بوحدو بـ `set_antialiased` / `get_antialiased`.
بغيت نزيدو `get_antialiased` و `set_antialiased` لـ `Text`، وإلا كان خاص حتى `Annotation` نبدلوه.
والمهم القيمة ديال كل artist خاصها تتستعمل بصح فـ le dessin، ماشي غير تتخزن.
ملاحظة: كنظن خاص نقيسو الـ backends، يعني بلاصة ما يقراو `rcParams["text.antialiased"]` نيشان يقراو من الـ state ديال `GraphicsContext`.
