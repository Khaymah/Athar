`xr.where(..., keep_attrs=True)` is overwriting coordinate attrs with the data variable's attrs.
looks like a regression from PR #6461 (a simple `lambda` change), probably broken since `2022.06.0`.
repro with the tutorial `air_temperature` dataset, checking `.time.attrs` of the `where` result:
[[A1]]
actual vs expected `time` attrs: [[A2]]
coordinate attributes should be preserved unchanged. I tried tracing the cause through the merge layers and couldn't, but if you come up with a fix idea I'm willing to send a PR.
env: [[A3]] (xarray `2022.10.0`)
