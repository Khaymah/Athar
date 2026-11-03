makemigrations on Django 3.2.4 is writing a migration that's missing an import statement. here's my models.py: a custom field, an abstract base model, a plain mixin class, and a model inheriting the mixin + the base
[[A1]]
and this is the 0001_initial.py it generated. `bases` uses `models.Model` but `models` is never imported:
[[A2]]
so loading it fails with `NameError: name 'models' is not defined`:
[[A3]]
the generated migration file should be valid Python. I suspect `django.db.migrations.writer` but not sure
