# django__django-13568

**Repo:** `django/django`

## What the request must convey (all units, nothing extra)

1. auth system check `auth.E003` fires though `USERNAME_FIELD` is unique via `Meta.constraints`, not `unique=True`
2. user model in [[A1]] triggers: `auth.User: (auth.E003) 'User.username' must be unique because it is named as the 'USERNAME_FIELD'.`
3. why avoid `unique=True`: creates extra implicit `*_like` index for `CharField`/`TextField` on PostgreSQL
4. request: check should also accept `USERNAME_FIELD` covered by a total `UniqueConstraint` in `Model._meta.constraints`
5. author unsure it counts as a bug

## Attachments (paste the placeholder where you would paste the block)

### `[[A1]]` (code)

````
class User(AbstractBaseUser):
	username = models.CharField(max_length=30)
	USERNAME_FIELD = "username"
	class Meta:
		constraints = [UniqueConstraint(fields=["username"], name="user_username_unq")]
````
