في autodoc، الـ :meta public: لما بحطها في doc-comment مش بتعمل أي حاجة مع الـ variables اللي على مستوى الـ module.
مثلاً عندي variable private اسمه _foo وعليه #: :meta public:
[[A1]]
وبعمله document بـ automodule مع :members:
[[A2]]
الـ _foo مش بيظهر خالص في الـ docs بعد الـ build، والمفروض يظهر. ده على Sphinx HEAD بتاع 3.x مع sphinx.ext.autodoc.
