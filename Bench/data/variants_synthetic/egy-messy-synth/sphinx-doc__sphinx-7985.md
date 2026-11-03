فى فكره feature keda لو ينفع الbuilder بتاع `linkcheck` يشيك على اللينكات اللوكال (الداخليه) كمان مش الexternal bs
اعمل project ب `sphinx-quickstart` و حط [[A1]] فى `index.rst` و شغل `make linkcheck` هيطلعلك [[A2]] اللينك الexternal مكتوب عليه `broken` انما اللوكال `doesntexist` متكتب `-local-` و خلاص محدش شيك عليه
المفروض يتشيك عليه هو كمان ولو بايظ يقول
Sphinx 1.7.6 و Python 3.6
