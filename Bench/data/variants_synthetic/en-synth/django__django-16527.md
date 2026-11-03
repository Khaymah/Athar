in the Django admin, the `show_save_as_new` context in `django/contrib/admin/templatetags/admin_modify.py` (~line 102) doesn't check add permission, so users without it can still "save as new". "save as new" is effectively an add operation, so I'd say `has_add_permission` must be required too.
this is how I rewrote the condition locally, adding `has_add_permission`:
[[A1]]
