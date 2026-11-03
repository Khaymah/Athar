في Django admin ال context `show_save_as_new` في `django/contrib/admin/templatetags/admin_modify.py` حوالي سطر 102 الcondition مش بتشيك علي add permission فاليوزر اللي معندوش الpermission دي يقدر يعمل "save as new" عادي
ودا اصلا add operation فلازم `has_add_permission` يبقي مطلوب برضو انا عدلت الcondition عندي local وزودت `has_add_permission` اهو [[A1]]
