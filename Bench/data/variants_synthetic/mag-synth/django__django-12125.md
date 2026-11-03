`makemigrations` كيكتب import path غالط ملي كيكون عندك subclass ديال `models.Field` معرف كـ inner class وسط class أخرى.
الclass المتداخلة كتتsérialisa بحال إلا كانت top-level ف الmodule ديالها.
هاهو الmodel: [[A1]] والmigration اللي كتخرج: [[A2]]، فيها `test1.models.Inner` والمفروض `test1.models.Outer.Inner`.
حالة حقيقية: django-enumfields، `EnumField` مع `Enum` داخل الmodel `Thing`: [[A3]]
والmigration ديالها [[A4]] كتشير ل `test1.models.State` عوض `test1.models.Thing.State`.
