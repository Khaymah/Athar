الـ makemigrations بيكتب import path غلط لو عندي subclass من models.Field متعرّف كـ inner class جوه class تانية. بيعمل serialize للـ nested class كإنها top-level في الـ module بتاعها.
دي الـ models اللي بتطلّع المشكلة
[[A1]]
والـ migration اللي اتعملت بتستخدم test1.models.Inner، والمفروض تبقى test1.models.Outer.Inner
[[A2]]
والحالة الحقيقية اللي قابلتني: EnumField بتاع django-enumfields مع Enum متعرّف جوه الـ model اللي اسمه Thing
[[A3]]
والـ migration بتاعته بتشاور على test1.models.State بدل test1.models.Thing.State
[[A4]]
