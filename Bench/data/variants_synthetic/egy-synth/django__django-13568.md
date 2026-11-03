الـ system check بتاع auth.E003 بيضرب مع إن الـ USERNAME_FIELD عندي unique عن طريق Meta.constraints، بس مش unique=True. الـ user model ده بيطلّعه
[[A1]]
auth.User: (auth.E003) 'User.username' must be unique because it is named as the 'USERNAME_FIELD'.
أنا مش عايز unique=True عشان على PostgreSQL بيعمل index زيادة implicit من نوع *_like للـ CharField/TextField. ينفع الـ check يقبل كمان الـ USERNAME_FIELD لو عليه total UniqueConstraint في Model._meta.constraints؟ بصراحة مش متأكد إن دي تتحسب bug
