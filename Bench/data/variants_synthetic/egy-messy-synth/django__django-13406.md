الqueryset الى فيها `values()`/`values_list()` و `annotate()` يعنى GROUP BY بتبوظ لما اشغلها تانى من `queryset.query` متعملها pickle
`type(prices[0])` بيطلع `dict` تمام bas `type(prices2[0])` بيطلع الموديل `Toy` وده غلط
وانا ماشى على طريقة pickling querysets الى فى الdocs بتاعت Django 2.2
الموديل [[A1]] والكود [[A2]] بحط الquery بعد الunpickle فى `Toy.objects.all().query`
ولما اعمل print ل `prices2` بيكراش [[A3]] الinstances بايظه خالص حتى `.id` بيرمى نفس الـ `AttributeError`
المفروض list of dicts زى الاصل انا 7ases ان الداتا من الDB صح بس بيتعمل منها instances للموديل
