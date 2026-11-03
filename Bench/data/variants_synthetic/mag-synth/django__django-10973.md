بغيت `client` ديال postgres backend (`django.db.backends.postgres.client`، يعني dbshell) يلانسي psql ب `subprocess.run`.
والmot de passe خاصو يدوز ف `PGPASSWORD` ف env خاص بالsubprocess.
`subprocess.run` كاينة من Python 3.5، وهادي أصلا هي la version minimum من Django 2.1.
الهدف هو يولي le code أبسط و fiable كثر.
