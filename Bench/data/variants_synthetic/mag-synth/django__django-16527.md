سلام، فـ Django admin، le context `show_save_as_new` ف `django/contrib/admin/templatetags/admin_modify.py` (تقريبا السطر 102) la condition ديالو ماكتشيكيش l'add permission، يعني users لي ماعندهومش هاد la permission يقدرو يديرو "save as new".
و "save as new" فالحقيقة راه add operation، داكشي علاش كنقول خاص حتى `has_add_permission` يكون مطلوب.
هادي la condition كيفاش عاودت كتبتها عندي ف local، زدت فيها `has_add_permission`: [[A1]]
