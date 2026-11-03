عايزين `client` بتاع postgres backend الى هو `django.db.backends.postgres.client` يعنى dbshell يشغل psql ب `subprocess.run`
والباسورد يتبعت فى `PGPASSWORD` جوا env مخصوص للsubprocess
`subprocess.run` موجوده من Python 3.5 وده اصلا الminimum من ساعة Django 2.1
el fekra ان الكود يبقى ابسط و reliable اكتر
