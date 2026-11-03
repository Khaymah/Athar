في الـ Django admin، الـ `show_save_as_new` context اللي في `django/contrib/admin/templatetags/admin_modify.py` (حوالي line 102) الـ condition بتاعه مش بيشيك على الـ add permission، فاليوزرز اللي معندهمش الـ permission دي لسه يقدروا يعملوا "save as new".
والـ "save as new" دي في الآخر add operation، فأنا شايف إن `has_add_permission` لازم تبقى مطلوبة هي كمان.
ده الـ condition بعد ما عدّلته عندي local وزوّدت `has_add_permission`:
[[A1]]
