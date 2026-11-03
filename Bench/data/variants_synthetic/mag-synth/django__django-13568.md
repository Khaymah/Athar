le system check ديال auth `auth.E003` كيطلع واخا `USERNAME_FIELD` unique عن طريق `Meta.constraints` ماشي ب `unique=True`.
هاد الuser model [[A1]] كيعطيني:
`auth.User: (auth.E003) 'User.username' must be unique because it is named as the 'USERNAME_FIELD'.`
علاش مابغيتش `unique=True`؟ حيت ف PostgreSQL كيصاوب index زايد implicit ديال `*_like` ل `CharField`/`TextField`.
بغيت الcheck يقبل حتى `USERNAME_FIELD` اللي مغطي ب `UniqueConstraint` total ف `Model._meta.constraints`.
ماعرفتش واش هادا يتحسب bug ولا لا.
