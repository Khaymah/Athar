el system check bta3 auth.E003 byedrab ma3 en el USERNAME_FIELD 3andi unique 3an taree2 Meta.constraints, bas msh unique=True. el user model da betala3o
[[A1]]
auth.User: (auth.E003) 'User.username' must be unique because it is named as the 'USERNAME_FIELD'.
ana msh 3ayez unique=True 3shan 3ala PostgreSQL bey3mel index zyada implicit men no3 *_like lel CharField/TextField. yenfa3 el check ye2bal kaman el USERNAME_FIELD law 3aleh total UniqueConstraint fi Model._meta.constraints? besara7a msh mot2aked en di tet7seb bug
