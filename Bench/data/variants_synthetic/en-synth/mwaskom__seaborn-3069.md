proposal: `so.Nominal` scales (incl. inferred ones) should mimic the categorical axis you get in seaborn's categorical plots. three things:
1) axis limits at +/- 0.5 around the first/last tick, not the normal margin logic
2) no grid, even when the active style would draw one
3) if it's on the y axis, invert the axis
notes: (1) is tricky, the approach I'd suggest is an invisible artist with sticky edges + margin 0 (hacky), or maybe sticky edges on the spine. (2) probably lives in `Plotter._finalize_figure`, open question is how a user forces the grid via the theme, maybe grid gets set on the scale. (3) is easy but not sure where it belongs.
