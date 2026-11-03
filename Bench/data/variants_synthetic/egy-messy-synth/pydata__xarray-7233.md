`Dataset.coarsen(...).construct(...)` بيحول الcoordinates اللى مش dimensional ل data variables
ع `main` اهو coord اسمه `day` علي dim `time` و بعدين `coarsen(time=12).construct(time=("year", "month"))` و الoutput m3ah
[[A1]]
المفروض اى حاجه كانت coordinate قبل كدا تفضل coordinate بعدها
