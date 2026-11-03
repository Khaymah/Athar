autodoc: :meta public: in a doc-comment has no effect on module-level variables.
e.g. a private variable _foo with #: :meta public:
[[A1]]
documented via automodule with :members:
[[A2]]
_foo is missing from the built docs, I'd expect it to show up. this is on Sphinx HEAD of 3.x, sphinx.ext.autodoc.
