model_to_dict(instance, fields=[]) returns all fields. it should return an empty dict, I didn't ask for any fields. I think the problem is this condition:
[[A1]]
it should be:
[[A2]]
my PR: https://github.com/django/django/pull/11150/files
