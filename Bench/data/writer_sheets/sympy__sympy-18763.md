# sympy__sympy-18763

**Repo:** `sympy/sympy`

## What the request must convey (all units, nothing extra)

1. LaTeX printing of `Subs` doesn't parenthesize the inner expression when multiplied
2. example expression [[A1]]
3. current `latex` output [[A2]], rendered image [[A3]]
4. desired output with inner expr wrapped in `\left(...\right)` [[A4]], rendered image [[A5]]

## Attachments (paste the placeholder where you would paste the block)

### `[[A1]]` (code)

```python
>>> from sympy import Subs
>>> from sympy.abc import x,y
>>> 3*Subs(-x+y, (x,),(1,))
```

### `[[A2]]` (code)

```python
'3 \\left. - x + y \\right|_{\\substack{ x=1 }}'
```

### `[[A3]]` (image)

````
![image](https://quicklatex.com/cache3/76/ql_9672fd7e62c909ff3d9ac8543c2e2576_l3.png)
````

### `[[A4]]` (code)

```python
'3 \\left. \\left(- x + y\\right) \\right|_{\\substack{ x=1 }}'
```

### `[[A5]]` (image)

````
![image](https://quicklatex.com/cache3/bf/ql_936ffdb876e784206d4c54bb93d28dbf_l3.png)
````
