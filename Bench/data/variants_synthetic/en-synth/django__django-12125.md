makemigrations writes the wrong import path for a models.Field subclass that's defined as an inner class of another class. it serializes the nested class as if it were top-level in its module.
repro models:
[[A1]]
generated migration uses test1.models.Inner, expected test1.models.Outer.Inner:
[[A2]]
real case where I hit it: django-enumfields EnumField with an Enum nested inside the Thing model
[[A3]]
and its migration references test1.models.State instead of test1.models.Thing.State
[[A4]]
