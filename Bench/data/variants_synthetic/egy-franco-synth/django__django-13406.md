ana mashy 3ala taree2et el pickling querysets elli fel docs (Django 2.2), w fih queryset fih values()/values_list() + annotate() (ya3ni GROUP BY) beyboz lama ashaghalo tani men queryset.query met3amalo pickle.
da el model
[[A1]]
w da el code, ba7ot el query ba3d el unpickle fi Toy.objects.all().query
[[A2]]
el type(prices[0]) tale3 dict w da tamam, bas type(prices2[0]) tale3 el model bta3 Toy w da ghalat. w lama a3mel print l prices2 byedrab
[[A3]]
el instances di bayza, 7atta .id byermy el AttributeError da. el mafrood arga3 list of dicts zay el asli. ana 7ases en el data elli gaya men el DB salima bas howa bybni menha model instances
