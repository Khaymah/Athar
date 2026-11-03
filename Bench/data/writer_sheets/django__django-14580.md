# django__django-14580

**Repo:** `django/django`

## What the request must convey (all units, nothing extra)

1. `makemigrations` in Django 3.2.4 writes a migration missing an import statement
2. `models.py` in [[A1]]: custom field, abstract base model, plain mixin class, model inheriting mixin + base
3. Generated `0001_initial.py` in [[A2]]: `bases` uses `models.Model` but `models` is never imported
4. Loading it fails with `NameError: name 'models' is not defined`, traceback [[A3]]
5. Expected: generated migration file is valid Python
6. Author suspects `django.db.migrations.writer`, not sure

## Attachments (paste the placeholder where you would paste the block)

### `[[A1]]` (code)

````
from django.db import models
class MyField(models.TextField):
	pass
class MyBaseModel(models.Model):
	class Meta:
		abstract = True
class MyMixin:
	pass
class MyModel(MyMixin, MyBaseModel):
	name = MyField(primary_key=True)
````

### `[[A2]]` (code)

````
import app.models
from django.db import migrations
class Migration(migrations.Migration):
	initial = True
	dependencies = [
	]
	operations = [
		migrations.CreateModel(
			name='MyModel',
			fields=[
				('name', app.models.MyField(primary_key=True, serialize=False)),
			],
			options={
				'abstract': False,
			},
			bases=(app.models.MyMixin, models.Model),
		),
	]
````

### `[[A3]]` (code)

````
 File "/home/jj/django_example/app/migrations/0001_initial.py", line 7, in <module>
	class Migration(migrations.Migration):
 File "/home/jj/django_example/app/migrations/0001_initial.py", line 23, in Migration
	bases=(app.models.MyMixin, models.Model),
NameError: name 'models' is not defined
````
