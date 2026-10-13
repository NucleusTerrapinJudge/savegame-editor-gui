# Security Policy

## Supported versions

| Version | Supported |
|---------|-----------|
| 0.9.x   | yes       |
| < 0.9   | no        |

## Reporting a vulnerability

savegame-editor-gui handles untrusted binary input from arbitrary save files.
A malicious `.sav` can absolutely exploit this tool — crafted length fields,
cyclic struct references, and zstd bombs are all in scope.

Report privately via GitHub Security Advisories. Do not open a public issue
for memory-safety or path-traversal bugs.

## Threat model

- **Parser DoS** — a save declaring a 4 GiB string field. All handlers enforce
  `MAX_FIELD_BYTES` from `config/limits.py`.
- **Path traversal on export** — the "Export profile" feature writes to a
  user-chosen path; we `Path.resolve()` and reject anything outside the
  configured export root.
- **Pickle-free** — we never `pickle.load` a save. Everything is `construct`
  or hand-rolled `struct` parsing.

## Out of scope

- Editing saves for online/multiplayer games in a way that trips anti-cheat.
  That's your account, your ban, your problem. We don't ship bypasses here.
- The `.spud` format. Different project, different repo.