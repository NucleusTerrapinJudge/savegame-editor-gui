# Architecture

savegame-editor-gui is a **pipeline** tool. One save file flows through
stages left to right:

```
  [file] -> ingest -> decode -> patch -> validate -> encode -> write -> [file]
             |          |         |         |          |         |
          handler   processor  editor    validator  driver   atomic_writer
```

## Stages

1. **Ingest** (`savegame_editor/ingest/`)
   Sniff the container magic (`GVAS`, `SAV`, custom), pick a handler from
   `registry.py`, produce a `RawContainer` with `payload: bytes` and header KV.

2. **Decode** (`savegame_editor/processors/decoder.py`)
   Decompress (LZ4/Zstd/zlib), parse the logical tree into `SaveTree`.

3. **Patch** (`savegame_editor/processors/patcher.py`)
   Apply `PatchOp` records from the GUI — set gold, unlock item, edit stats.

4. **Validate** (`savegame_editor/processors/validator.py`)
   Range checks, checksum precompute, structural sanity.

5. **Encode** (`savegame_editor/processors/encoder.py`)
   Serialize `SaveTree` back to bytes in the original container format.

6. **Write** (`savegame_editor/output/atomic_writer.py`)
   Write to `.tmp`, fsync, `os.replace()` over the original, keep a `.bak`.

## Worker model

The GUI never blocks. Every pipeline run is submitted to `WorkerPool`
(`savegame_editor/utils/worker_pool.py`), which fans out to `QThread`s and
emits progress via Qt signals. Long ops report `(stage, percent)`.

## Why not C++/C#/Java?

We considered all three. Python wins for iteration speed on a moving target
of save formats. The hot path (LZ4 + AES) is already C under the hood via
`lz4` and `pycryptodome`. If we ever need a native decoder, it goes in
`native/` and gets called via `ctypes`.