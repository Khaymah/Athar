# sphinx-doc__sphinx-9711

**Repo:** `sphinx-doc/sphinx`

## What the request must convey (all units, nothing extra)

1. `needs_extensions` compares extension versions as strings, not as versions
2. effect: `'0.6' > '0.10'` as strings, so newer versions (e.g. minor >9) wrongly rejected
3. repro project mplcursors [[A1]]: builds fine with pinned sphinx-gallery 0.9
4. after upgrading to sphinx-gallery 0.10 [[A2]], build fails with "not new enough" version error [[A3]]
5. expected: `sphinx_gallery.gen_gallery` 0.10.0 accepted when minimum is 0.6.0
6. env: Sphinx 4.1.2

## Attachments (paste the placeholder where you would paste the block)

### `[[A1]]` (code)

```
$ git clone https://github.com/anntzer/mplcursors
$ cd mplcursors
$ pip install -r .doc-requirements.txt
$ pip install -e .
$ make -C doc html
```

### `[[A2]]` (code)

```
$ pip install sphinx-gallery==0.10
$ make -C doc html
```

### `[[A3]]` (code)

```
Running Sphinx v4.1.2
loading translations [en]... done
making output directory... done

Sphinx version error:
This project needs the extension sphinx_gallery.gen_gallery at least in version 0.6.0 and therefore cannot be built with the loaded version (0.10.0).
```
