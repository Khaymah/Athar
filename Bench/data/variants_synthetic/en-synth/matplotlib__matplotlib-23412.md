on Patch objects the offset in a dash-tuple `linestyle` has no effect on the edge line. repro, two overlapping `Rectangle`s with the same dash pattern but different offsets:
[[A1]]
the edge dashes just overlap, offset is ignored: [[A2]]
expected the offset to shift the dashes like it does for `Line2D`. Line2D code: [[A3]] and its output: [[A4]]
same issue with the `Ellipse` patch. seen on 3.3.4 (macOS, MacOSX backend) and 3.5.0 (Ubuntu 18.04, agg backend)
