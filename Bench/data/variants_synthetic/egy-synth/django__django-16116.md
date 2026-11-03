الـ `makemigrations --check` لسه بيكتب الـ migration files عادي، ولو عايز check بس لازم تديله `--check` و `--dry-run` مع بعض.
وده مش متسق مع `migrate --check` و `optimizemigration --check` اللي بيعملوا exit وخلاص (يمكن بعد شوية logging).
أنا شايف إن `makemigrations --check` المفروض يعمل exit من غير ما يعمل migrations. وعلى فكرة حكاية إنه بيكتب برضه دي محدش اتكلم فيها أصلاً في ticket #25604 ولا في الـ django-developers thread بتاعها، والـ docs دلوقتي مش بتقول أي حاجة عنها.
