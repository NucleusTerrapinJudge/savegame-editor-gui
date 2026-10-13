# Contributing to savegame-editor-gui

Thanks for wanting to help peel save files apart. This repo is a pipeline
architecture: **ingest handlers** read raw bytes, **processors** decode and
patch the logical tree, **output drivers** re-serialize and write back.
Every contribution should slot into one of those three layers.

## Ground rules

- Python 3.11+. Run `ruff check` and `mypy savegame_editor` before opening a PR.
- New save format support goes in `savegame_editor/ingest/` as a handler class
  implementing `BaseIngestHandler`. Register it in `ingest/registry.py`.
- Never mutate a save in place. All writes go through `output/atomic_writer.py`
  so a crashed patch never bricks the user's progress.
- Add a fixture under `tests/fixtures/` — a real (small) save, or a synthetic
  header if the title's saves are huge. Tests must pass offline.

## Commit style

`ingest: add UE5 GZIP header sniff`
`processor: fix inventory slot offset for v1.2.7 saves`
`output: checksum recompute for CRC32-trailer saves`

## What lives where

| Layer      | Folder                | Responsibility                       |
|------------|-----------------------|--------------------------------------|
| Ingest     | `savegame_editor/ingest/`     | Detect + read raw container   |
| Processors | `savegame_editor/processors/` | Decode, patch, validate       |
| Output     | `savegame_editor/output/`     | Re-encode, checksum, atomic write |
| GUI        | `savegame_editor/gui/`        | Qt views + worker bridge      |
| Models     | `savegame_editor/models/`     | Pydantic schemas              |

## Legal-ish

You are editing your own saves on your own disk. Don't ship other people's
save files in PRs — they may contain account tokens. Redact before committing.