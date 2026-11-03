fel Django admin, el `show_save_as_new` context elly fe `django/contrib/admin/templatetags/admin_modify.py` (7awaly line 102) el condition bta3o msh beyshayek 3al add permission, fa el users elly ma3andhomsh el permission di lessa y2daro ye3mlo "save as new".
wel "save as new" di fel a5er add operation, fa ana shayef en `has_add_permission` lazem tb2a matlooba heya kaman.
da el condition ba3d ma 3addelto 3andy local w zawwedt `has_add_permission`:
[[A1]]
