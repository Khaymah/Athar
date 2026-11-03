pylint creates a `.pylint.d` data directory directly in my home dir. can we make it comply with the XDG Base Directory Specification?
per the spec, data goes in `$HOME/.local/share/<PROGRAM_NAME>` (it also defines `$HOME/.cache/<PROGRAM_NAME>` for cache and `$HOME/.config/<PROGRAM_NAME>` for config).
goal is just a clean home dir, I think changing the variables/constants for the storage path should be enough.
