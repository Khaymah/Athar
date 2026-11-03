أنا ماشي على طريقة الـ pickling querysets اللي في الـ docs (Django 2.2)، وفيه queryset فيه values()/values_list() + annotate() (يعني GROUP BY) بيبوظ لما أشغّله تاني من queryset.query متعمله pickle.
ده الـ model
[[A1]]
وده الكود، بحط الـ query بعد الـ unpickle في Toy.objects.all().query
[[A2]]
الـ type(prices[0]) طالع dict وده تمام، بس type(prices2[0]) طالع الـ model بتاع Toy وده غلط. ولما أعمل print لـ prices2 بيضرب
[[A3]]
الـ instances دي بايظة، حتى .id بيرمي الـ AttributeError ده. المفروض أرجع list of dicts زي الأصلي. أنا حاسس إن الـ data اللي جاية من الـ DB سليمة بس هو بيبني منها model instances
