feature request: بغيت الـ builder ديال `linkcheck` يفحص حتى les liens المحليين (internal)، ماشي غير الخارجيين.
باش تعاود المشكل: دير projet بـ `sphinx-quickstart`، حط [[A1]] ف `index.rst`، ومن بعد دير `make linkcheck`.
الـ output [[A2]]: الـ lien الخارجي كيتعلم `broken`، ولكن الـ lien المحلي `doesntexist` كيتكتب غير `-local-` وماكيتفحصش.
اللي بغيت: حتى الـ lien المحلي يتفحص، وإلا كان مقطوع يتبلغ عليه.
l'env: Sphinx 1.7.6، Python 3.6.
