# sphinx-doc__sphinx-8056

**Repo:** `sphinx-doc/sphinx`

## What the request must convey (all units, nothing extra)

1. napoleon numpy-style `Parameters`: multiple params combined on one line, allowed by numpydoc guide (section 4)
2. docstring like [[A1]] renders incorrectly in HTML; screenshot of output [[A2]]
3. with `optional` added [[A3]], output identical to screenshot; optional-ness not shown at all
4. expected render roughly: x1, x2 (_array_like, optional_) - Input arrays, description of x1, x2.
5. env: Sphinx 3.0.3, Python 3.7.7, macOS 10.15.5, Firefox/Safari; extensions list [[A4]]

## Attachments (paste the placeholder where you would paste the block)

### `[[A1]]` (code)

```
x1, x2 : array_like
    Input arrays, description of `x1`, `x2`.
```

### `[[A2]]` (image)

````
<img width="406" alt="图片" src="https://user-images.githubusercontent.com/20618587/83668496-566d3680-a5d0-11ea-8a15-5596f77b6c20.png">
````

### `[[A3]]` (code)

```
x1, x2 : array_like, optional
    Input arrays, description of `x1`, `x2`.
```

### `[[A4]]` (code)

```
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "nbsphinx",
    "sphinx.ext.mathjax",
    "sphinxcontrib.bibtex",
    "sphinx.ext.doctest",
]
```
