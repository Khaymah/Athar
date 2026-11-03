Right now `Text` always reads antialiasing from the global `rcParams["text.antialiased"]`, while other artists let you control it per-artist with `set_antialiased` / `get_antialiased`.
Can you add `get_antialiased` / `set_antialiased` to `Text`, and adjust `Annotation` too if needed? The per-artist value has to actually be used when drawing.
Heads up, I think the backends need touching: replace the direct `rcParams["text.antialiased"]` reads with `GraphicsContext` state.
