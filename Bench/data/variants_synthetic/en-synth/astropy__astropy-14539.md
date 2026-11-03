io.fits.FITSDiff is reporting differences between identical files, even when I compare a file to itself. repro: BinTableHDU with a VLA column (format='QD'), then compare the file to itself with FITSDiff and fits.printdiff
[[A1]]
output: .identical is False and it says column a data differs in row 0
[[A2]]
it should only report differences if there actually are some, same file vs itself should never differ. I suspect the VLA (variable-length array) handling, couldn't reproduce it without a VLA column. this is on astropy 5.2.1
