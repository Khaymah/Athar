ياجماعه `makemigrations` في Django 3.2.4 بيطلع migration ناقصها import statement ولما بحمل الملف بيضرب `NameError: name 'models' is not defined` الtraceback اهو [[A3]]
ده `0001_initial.py` اللى اتعمل [[A2]] ال `bases` فيه بيستخدم `models.Model` bs `models` مش متعملها import خالص
ودا `models.py` [[A1]] فيه custom field و abstract base model و mixin class عادي و model وارث من الmixin والbase
المفروض الmigration اللي بيطلع يبقي python سليم msh keda.. انا شاكك في `django.db.migrations.writer` بس مش متاكد
