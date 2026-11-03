عايز أطلب feature: الـ linkcheck builder بيشيّك على الـ external links بس، ياريت يشيّك على الـ local (internal) links كمان.
عشان تشوفها: اعمل project بـ sphinx-quickstart، وحط ده في index.rst
[[A1]]
وبعدين شغّل make linkcheck، هيطلعلك:
[[A2]]
الـ external link بيتقال عليه broken، إنما الـ local link (doesntexist) بيتكتب جنبه -local- وخلاص من غير ما يتشيّك عليه. المفروض الـ local link يتشيّك عليه هو كمان ويتبلّغ عنه لو بايظ.
Sphinx 1.7.6 و Python 3.6
