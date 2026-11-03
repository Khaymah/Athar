feature request: the linkcheck builder only checks external links, would be great if it also checked local (internal) ones.
to reproduce: make a project with sphinx-quickstart, put this in index.rst
[[A1]]
then run make linkcheck. output:
[[A2]]
the external link is reported as broken, but the local one (doesntexist) just gets listed as -local- and isn't actually checked. I'd expect the local link to be checked too, and reported if it's broken.
Sphinx 1.7.6, Python 3.6
