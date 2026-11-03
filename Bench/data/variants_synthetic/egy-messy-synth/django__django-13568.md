msh 3aref ده يتحسب bug ولا لا بس الcheck بتاع auth `auth.E003` بيطلع رغم ان `USERNAME_FIELD` unique بـ `Meta.constraints` مش ب `unique=True`
اليوزر موديل ده [[A1]] بيطلع `auth.User: (auth.E003) 'User.username' must be unique because it is named as the 'USERNAME_FIELD'.`
ومش عايز `unique=True` عشن على PostgreSQL بيعمل index زياده implicit `*_like` لل `CharField`/`TextField`
فالمطلوب الcheck يقبل كمان `USERNAME_FIELD` لو عليه `UniqueConstraint` total فى `Model._meta.constraints`
