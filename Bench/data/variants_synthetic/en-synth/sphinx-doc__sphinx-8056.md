napoleon problem with numpy-style Parameters: the numpydoc guide (section 4) allows combining multiple params on one line, but a docstring like
[[A1]]
renders incorrectly in the HTML, this is what I get:
[[A2]]
and if I add optional like this
[[A3]]
the output is identical to the screenshot, nothing shows it's optional at all.
I'd expect it to render roughly as: x1, x2 (_array_like, optional_) - Input arrays, description of x1, x2.
Sphinx 3.0.3, Python 3.7.7, macOS 10.15.5, Firefox/Safari. extensions:
[[A4]]
