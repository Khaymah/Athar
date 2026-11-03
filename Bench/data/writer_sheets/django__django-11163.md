# django__django-11163

**Repo:** `django/django`

## What the request must convey (all units, nothing extra)

1. `model_to_dict(instance, fields=[])` returns all fields
2. expected: empty dict, since no fields were requested
3. author points at the condition [[A1]] as the problem; says it should be [[A2]]
4. author's PR: https://github.com/django/django/pull/11150/files

## Attachments (paste the placeholder where you would paste the block)

### `[[A1]]` (code)

````
if fields and f.name not in fields:
````

### `[[A2]]` (code)

````
if fields is not None and f.name not in fields:
````
