# matplotlib__matplotlib-25775

**Repo:** `matplotlib/matplotlib`

## What the request must convey (all units, nothing extra)

1. `Text` antialiasing always read from global `rcParams["text.antialiased"]`
2. other artists support per-artist control via `set_antialiased` / `get_antialiased`
3. request: add `get_antialiased` / `set_antialiased` to `Text`; adjust `Annotation` too if needed
4. the per-artist value must actually be used when drawing
5. author's note: backends need touching; replace direct `rcParams["text.antialiased"]` reads with `GraphicsContext` state

## Attachments (paste the placeholder where you would paste the block)

_None: the request is prose only._
