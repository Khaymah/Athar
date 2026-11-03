# django__django-16527

**Repo:** `django/django`

## What the request must convey (all units, nothing extra)

1. Django admin: `show_save_as_new` context in `django/contrib/admin/templatetags/admin_modify.py` (~line 102)
2. Condition does not check add permission, so users without it can still "save as new"
3. "Save as new" is effectively an add operation, so author says `has_add_permission` must be required too
4. Author's local rewrite of the condition, adding `has_add_permission`, in [[A1]]

## Attachments (paste the placeholder where you would paste the block)

### `[[A1]]` (code)

````
			"show_save_as_new": not is_popup
			and has_add_permission # This line that I put!!!
			and has_change_permission
			and change
			and save_as,
````
