# astropy__astropy-14539

**Repo:** `astropy/astropy`

## What the request must convey (all units, nothing extra)

1. `io.fits.FITSDiff` reports differences between identical files, even a file vs itself
2. repro in [[A1]]: `BinTableHDU` with VLA column (`format='QD'`), compare file to itself via `FITSDiff` and `fits.printdiff`
3. actual output [[A2]]: `.identical` is `False`, says column `a` data differs in row 0
4. expected: differences reported only if they exist; same file vs itself never differs
5. author suspects VLA (variable-length array) handling; bug not reproduced without a VLA column
6. seen on astropy `5.2.1`

## Attachments (paste the placeholder where you would paste the block)

### `[[A1]]` (code)

```python
from astropy.io import fits
col = fits.Column('a', format='QD', array=[[0], [0, 0]])
hdu = fits.BinTableHDU.from_columns([col])
hdu.writeto('diffbug.fits', overwrite=True)

print(fits.FITSDiff('diffbug.fits', 'diffbug.fits').identical)
fits.printdiff('diffbug.fits', 'diffbug.fits')

```

### `[[A2]]` (code)

```
False
 fitsdiff: 5.2.1
 a: diffbug.fits
 b: diffbug.fits
 Maximum number of different data values to be reported: 10
 Relative tolerance: 0.0, Absolute tolerance: 0.0
Extension HDU 1:
   Data contains differences:
     Column a data differs in row 0:
     1 different table data element(s) found (50.00% different).
```
