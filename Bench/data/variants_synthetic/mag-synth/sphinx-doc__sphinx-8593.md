ف autodoc، `:meta public:` ف doc-comment ماكيدير حتى تأثير على les variables ديال الـ module.
مثال: عندي variable privée `_foo` معاها `#: :meta public:` [[A1]]، وكندوكيمونتيها بـ `automodule` مع `:members:` [[A2]].
اللي كيطرا: `_foo` ماكايناش ف الـ docs اللي تبناو.
اللي كنتسنا: `_foo` تبان ف الـ docs.
l'env: Sphinx HEAD ديال 3.x، `sphinx.ext.autodoc`.
