# pylint-dev__pylint-4661

**Repo:** `pylint-dev/pylint`

## What the request must convey (all units, nothing extra)

1. pylint creates a `.pylint.d` data directory directly in user's home
2. request: comply with XDG Base Directory Specification
3. per spec, data goes in `$HOME/.local/share/<PROGRAM_NAME>`
4. spec also defines `$HOME/.cache/<PROGRAM_NAME>` for cache, `$HOME/.config/<PROGRAM_NAME>` for config
5. goal: clean home dir; author thinks changing the storage path variables/constants suffices

## Attachments (paste the placeholder where you would paste the block)

_None: the request is prose only._
