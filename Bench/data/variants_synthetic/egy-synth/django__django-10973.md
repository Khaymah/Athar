عايزك تخلّي الـ client بتاع الـ postgres backend (django.db.backends.postgres.client، اللي هو بتاع dbshell) يشغّل psql بـ subprocess.run، والـ password تتبعت عن طريق PGPASSWORD في env مخصوص للـ subprocess.
الـ subprocess.run موجودة من Python 3.5، ودي أصلاً الـ minimum من ساعة Django 2.1. الهدف إن الكود يبقى أبسط و reliable أكتر
