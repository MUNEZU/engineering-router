# Explore

Dispatch one `code_explorer` for one independent codebase question only when
the root needs help locating the primary files, entry points, symbols, or call
path. Small lookups remain in the root.

Give the explorer the repository location, bounded question, allowed scope,
known clues, and expected return. Treat suggested files and diagnoses as leads,
not conclusions. The explorer starts with fresh context and stays read-only.

Require a concise result containing the primary files and symbols, how they
connect, the likely impact boundary, and brief evidence. Keep raw search output
and unrelated architecture out of the handoff. The root combines the map with
the accepted contract before choosing implementation.
