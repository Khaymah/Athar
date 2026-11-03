`Dataset.coarsen(...).construct(...)` كيقلب الـ coordinates اللي ماشي dimensionnelles لـ data variables.
الـ repro والـ output: عندي coord `day` على الـ dim `time`، ومن بعد `coarsen(time=12).construct(time=("year", "month"))`:
[[A1]]
اللي بغيت: أي حاجة كانت coordinate قبل خاصها تبقى coordinate من بعد.
شفت هادشي على `main`.
