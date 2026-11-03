الـ makemigrations في Django 3.2.4 بيكتب migration ناقصها import statement. ده الـ models.py بتاعي: custom field و abstract base model و mixin class عادية و model بيورث من الـ mixin والـ base
[[A1]]
ودي الـ 0001_initial.py اللي اتعملت. بص على `bases`، مستخدمة `models.Model` بس `models` مش متعملها import خالص:
[[A2]]
فلما بتتحمّل بيطلعلي `NameError: name 'models' is not defined`:
[[A3]]
المفروض الـ migration file اللي بتتولّد تبقى Python سليم. أنا شاكك في `django.db.migrations.writer` بس مش متأكد
