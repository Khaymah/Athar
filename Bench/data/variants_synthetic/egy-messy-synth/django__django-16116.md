`makemigrations --check` لسه بيكتب migration files ولازم تحط `--check` مع `--dry-run` عشن يعمل check بس ودا مش متسق مع `migrate --check` و `optimizemigration --check` اللي بيعملو exit وخلاص يمكن بعد شوية logging
الكتابه دي محدش اتكلم عنها في ticket #25604 ولا الthread بتاعه علي django-developers والdocs دلوقت ساكته عنها خالص
اقتراحي ان `makemigrations --check` يعمل exit من غير ما يعمل migrations
