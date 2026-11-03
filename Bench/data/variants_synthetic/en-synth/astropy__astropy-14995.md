NDDataRef arithmetic mask propagation is broken in astropy 5.3 when one of the operands has no mask, it was fine in 5.2. happens with handle_mask=np.bitwise_or, I get a TypeError for | between int and NoneType.
here's my session, mask × constant and mask × no-mask fail, the no-mask cases and mask × mask work:
[[A1]]
my guess is the missing mask is treated as Nones so bitwise_or gets an int and a None. what I expect: if only one operand has a mask, just copy that mask to the output, like v5.2 did. version info:
[[A2]]
