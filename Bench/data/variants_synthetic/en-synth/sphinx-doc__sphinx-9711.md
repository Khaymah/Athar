needs_extensions compares extension versions as strings, not as versions. so '0.6' > '0.10' as strings and newer versions (e.g. minor > 9) get wrongly rejected.
repro with mplcursors:
[[A1]]
that builds fine with sphinx-gallery pinned at 0.9. after upgrading to 0.10:
[[A2]]
the build fails with the "not new enough" version error:
[[A3]]
sphinx_gallery.gen_gallery 0.10.0 should be accepted when the minimum is 0.6.0. Sphinx 4.1.2.
