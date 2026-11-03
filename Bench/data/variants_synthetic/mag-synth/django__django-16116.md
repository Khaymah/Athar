سلام، `makemigrations --check` باقي كيكتب les fichiers ديال migrations؛ باش غير تشيكي خاصك `--check` و `--dry-run` بجوج.
هادشي ماشي متناسق مع `migrate --check` و `optimizemigration --check`، لي كيخرجو وصافي (يمكن من بعد شي logging).
اقتراحي: `makemigrations --check` خاصو يخرج بلا مايصاوب migrations.
هاد السلوك ديال أنه يكتب على أي حال عمرو ماتناقش ف ticket #25604 ولا ف le thread ديالو ف django-developers، والـ docs دابا ساكتين عليه.
