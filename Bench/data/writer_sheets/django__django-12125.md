# django__django-12125

**Repo:** `django/django`

## What the request must convey (all units, nothing extra)

1. `makemigrations` writes wrong import path for a `models.Field` subclass defined as inner class of another class
2. nested class is serialized as if it were top-level in its module
3. repro models [[A1]]; generated migration [[A2]] uses `test1.models.Inner`, expected `test1.models.Outer.Inner`
4. real case: django-enumfields `EnumField` with an `Enum` nested inside model `Thing` [[A3]]
5. its migration [[A4]] references `test1.models.State` instead of `test1.models.Thing.State`

## Attachments (paste the placeholder where you would paste the block)

### `[[A1]]` (code)

````
class Outer(object):
	class Inner(models.CharField):
		pass
class A(models.Model):
	field = Outer.Inner(max_length=20)
````

### `[[A2]]` (code)

````
migrations.CreateModel(
	name='A',
	fields=[
		('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
		('field', test1.models.Inner(max_length=20)),
	],
),
````

### `[[A3]]` (code)

````
import enum
from enumfields import Enum, EnumField
class Thing(models.Model):
	@enum.unique
	class State(Enum):
		on = 'on'
		off = 'off'
	state = EnumField(enum=State)
````

### `[[A4]]` (code)

````
migrations.CreateModel(
	name='Thing',
	fields=[
		('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
		('state', enumfields.fields.EnumField(enum=test1.models.State, max_length=10)),
	],
),
````
