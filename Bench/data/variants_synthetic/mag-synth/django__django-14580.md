سلام، `makemigrations` ف Django 3.2.4 كيكتب ليا migration ناقصها import statement.
هادا `models.py` ديالي، فيه custom field، و base model abstract، و mixin class عادية، و model كيورث من الـ mixin و الـ base: [[A1]]
وهادا `0001_initial.py` لي كيطلع ليا، فـ `bases` كيستعمل `models.Model` ولكن `models` عمرها ماتدار ليها import: [[A2]]
ملي كنشارجي هاد le fichier كيطيح بـ `NameError: name 'models' is not defined`، هاهو le traceback: [[A3]]
المفروض الـ migration لي كيتولد يكون Python صالح. كنشك فـ `django.db.migrations.writer` ولكن ماشي متأكد.
