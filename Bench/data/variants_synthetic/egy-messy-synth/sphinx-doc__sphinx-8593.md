`:meta public:` فى doc-comment ملهاش اى تاثير على الvariables اللى على مستوى الmodule فى autodoc
عندى variable private اسمه `_foo` و عليه `#: :meta public:` [[A1]] و بعمله document ب `automodule` و `:members:` [[A2]] و `_foo` مش موجود خالص فى الdocs بعد الbuild والمفروض يظهر
Sphinx HEAD بتاع 3.x و `sphinx.ext.autodoc`
