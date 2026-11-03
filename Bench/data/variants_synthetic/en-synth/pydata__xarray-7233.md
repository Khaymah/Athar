`Dataset.coarsen(...).construct(...)` turns non-dimensional coordinates into data variables.
repro + output below: coord `day` on dim `time`, then `coarsen(time=12).construct(time=("year", "month"))`
[[A1]]
everything that was a coordinate before should stay a coordinate after. seeing this on `main`.
