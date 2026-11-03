I'm documenting SWIG-wrapped C++ classes that have overloaded methods. the convention there is one signature per overload, all of them placed at the start of the docstring.
right now autodoc_docstring_signature only picks up the first signature. can you make it pick up all of the signatures?
