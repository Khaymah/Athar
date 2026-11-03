system check auth.E003 fires even though my USERNAME_FIELD is unique via Meta.constraints, just not unique=True. this user model triggers it:
[[A1]]
auth.User: (auth.E003) 'User.username' must be unique because it is named as the 'USERNAME_FIELD'.
reason I'm avoiding unique=True: on PostgreSQL it creates an extra implicit *_like index for CharField/TextField. could the check also accept a USERNAME_FIELD that's covered by a total UniqueConstraint in Model._meta.constraints? not sure this even counts as a bug tbh
