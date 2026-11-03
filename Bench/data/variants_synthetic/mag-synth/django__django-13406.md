عندي queryset فيها `values()`/`values_list()` مع `annotate()` (GROUP BY) كتخسر ملي كنعاود نرونيها من `queryset.query` اللي درت ليه pickle.
راني تابع الطريقة اللي ف la doc ديال pickling querysets (Django 2.2).
الmodel: [[A1]] والcode: [[A2]]، كنحط الquery اللي درت ليها unpickle ف `Toy.objects.all().query`.
`type(prices[0])` كيعطي `dict` وهادشي مزيان، ولكن `type(prices2[0])` كيعطي الmodel `Toy` وهادا غالط.
وملي كنprinti `prices2` كيكراشي: [[A3]]، les instances مهرسين، حتى `.id` كيطلع نفس `AttributeError`.
كنتسنى liste ديال dicts بحال الأصلية؛ كنظن الdata ف الDB صحيحة ولكن كيتبناو منها instances ديال الmodel.
