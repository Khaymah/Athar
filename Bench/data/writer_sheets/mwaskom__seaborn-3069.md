# mwaskom__seaborn-3069

**Repo:** `mwaskom/seaborn`

## What the request must convey (all units, nothing extra)

1. proposal: `so.Nominal` scales (incl. inferred ones) should mimic categorical axis of seaborn categorical plots
2. behavior 1: axis limits at +/- 0.5 around first/last tick, not normal margin logic
3. behavior 2: no grid, even when active style would draw one
4. behavior 3: if on y axis, invert the axis
5. impl note 1: tricky; suggested approach is invisible artist with sticky edges + margin 0 (hacky); maybe sticky edges on spine
6. impl note 2: likely in `Plotter._finalize_figure`; open question: how user forces grid via theme, maybe grid set on scale
7. impl note 3: easy, but unclear where it belongs

## Attachments (paste the placeholder where you would paste the block)

_None: the request is prose only._
