I'm following the documented pickling-querysets approach (Django 2.2 docs) and a queryset using values()/values_list() + annotate() (GROUP BY) breaks when I re-run it from a pickled queryset.query.
model:
[[A1]]
code, I assign the unpickled query to Toy.objects.all().query:
[[A2]]
type(prices[0]) is dict, fine, but type(prices2[0]) is the Toy model, which is wrong. printing prices2 crashes:
[[A3]]
the instances are broken, even .id raises that AttributeError. I'd expect a list of dicts like the original. I think the data from the DB is right but it's building model instances out of it
