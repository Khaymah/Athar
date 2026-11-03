`makemigrations` بيكتب import path غلط لو عندك subclass من `models.Field` متعرف inner class جوا class تانيه
الموديلز [[A1]] والمايجريشن الى طلع [[A2]] فيه `test1.models.Inner` والمفروض `test1.models.Outer.Inner` يعنى بيعمل serialize للnested class كانها top-level فى الموديول بتاعها
وفى حاله حقيقيه kaman مع django-enumfields `EnumField` و `Enum` جوا الموديل `Thing` [[A3]] المايجريشن بتاعتها [[A4]] بيشاور على `test1.models.State` بدل `test1.models.Thing.State`
