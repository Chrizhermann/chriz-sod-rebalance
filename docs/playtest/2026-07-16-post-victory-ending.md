# Runtime verification — post-victory ending (component 290)

**Update 2026-09-06:** The [current isolated runtime record](2026-09-06-ending-runtime.md)
records the original EET guard softlock, corrective tail component 291, and passing
R0, R1, R6, plus the user-approved reduced single inventory handoff. Standalone is
pending; the original expanded matrix below was not completed. The September run
uses separate game/profile copies, superseding this document's historical shared
profile staging notes for that run. The actual dev installation subsequently received
tail component 291 and passed all 43 installed-state checks; live remains untouched.

Target: **dev EET install** `C:\Games\Baldur's Gate II Enhanced Edition modded - dev eet
install`, mod v0.6.4, component 290 tail-installed 2026-07-16 (sole last WeiDU.log row).
Static state re-confirmed **2026-08-12**: `verify_ending.py --platform eet` = **40/40 PASS**
against the dev install; TP2 versions repo↔dev match; append-only log intact.

This document is the evidence record for plan Task 6 (EET runtime matrix) and Task 7
(standalone smoke). A row is DONE only with a real in-game run recorded here — static
decompilation never closes a row.

Status legend: **PENDING** · **STAGED** (save prepared, not run) · **PASS** · **FAIL**

---

## Shared staging notes (read first)

- **Save directory is SHARED with the live install** (EET userdir):
  `C:\Users\chris\OneDrive\Documents\Baldur's Gate - Enhanced Edition Trilogy\save\`.
  Test saves show up in the live game's load menu too. Namespace every test copy
  `CSR END <case>` and delete them after the matrix closes. Do not touch live
  `Interval-Save*` folders.
- **Stage a case** = copy the seed folder to a fresh unused save number, e.g.
  `000000018-Kool Koveras-Chapter 10 Start` → `000000901-CSR END R2`. Check the save list
  for number collisions first.
- **Seed saves (verified present 2026-08-12):**
  - `000000435-safety safe` — BD4300 already baked into BALDUR.SAV **without** the
    import container → this is the guard-test seed (R0).
  - `000000018-Kool Koveras-Chapter 10 Start` — BALDUR.SAV has **no** BD4300 → the
    area builds fresh from the patched override ARE → happy-path seed (R1–R8).
- Console basics (EE console, dev install launched via its own `InfinityLoader.exe`):
  - marker item: `C:CreateItem("<resref>")` — trailing int = per-ability charges
    (`0` = empty, NOT default); plain form is right for ordinary MISC/RING markers;
  - area move: `C:MoveToArea("BD4300")`;
  - plot check: `C:GetGlobal("bd_plot","GLOBAL")`; shortcut staging (R1 fallback only):
    `C:SetGlobal("bd_plot","GLOBAL",586)` then `C:Eval('StartCutScene("BDCUT59B")')`;
  - **never** set `bd_plot=590` directly for a primary case — 590 must come from the
    real de Lancie → Bence conversation chain.
- Marker manifest discipline: one distinct ordinary item per party slot, written into
  the case row BEFORE the run; compare the multiset after AR0602 loads. Equipped,
  quick-slot, bag, and loose-inventory placements all count. Gold noted separately.
- Agent-side probing: dev has EEex 0.11.0-alpha but **NOT** eeexremote (live-only).
  Tail-installing eeexremote on dev would enable file-IPC console driving — **OPEN
  decision, not assumed.** All rows below are runnable by hand without it.

## Success contract (every R2–R8 row)

Dazzo end-rest option → fade black → next interactive frame is **SoA AR0602**. BD6100 is
never the party/current area, no ambush fight, no `sodcin05`/INTRO15F double-play visible
to the player beyond the normal SoA intro flow. Zero unexplained marker loss or
duplication; named-import items follow original K# store semantics; gold and containers
behave exactly like an unmodified SoD→SoA handoff. Journal entry 266908 erased.

---

## R0 — missing-container guard (fail-closed) — PASS after repair

Seed: `000000435-safety safe` (copy → `CSR END R0`). BD4300 in this save predates the
container patch, so the clone's guard MUST refuse the handoff.

Stage: give Player1 one unique marker (`C:CreateItem("<resref>")`), note it here.
Run: talk to Sergeant Dazzo, pick the ending option.
Expected: visible diagnostic (@29000 string) BEFORE any item sweep; fade returns;
cutscene mode ends; ALL gear still on the party; campaign does NOT move; save, reload,
confirm the save remains playable.

Result: original softlock reproduced; repaired guard, inventory retention, and
native save/reload **PASS**. See the [2026-09-06 record](2026-09-06-ending-runtime.md)
for marker `M290G001` and evidence.

## R1 — primary happy path, real conversation spine — PASS

Seed: preferred = a genuine save from immediately before BDCUT59; fallback = copy of
`000000018-Kool Koveras-Chapter 10 Start` staged via the console shortcut (move to
BD4300 at plot 586 + `StartCutScene("BDCUT59B")`). **The shortcut does NOT cover
BDCUT59/59A** — if used, record separate coverage for 59/59A (in-engine run from their
real source area) before closing this row.

Run: let the 586→587 timer chain finish; click de Lancie; follow her public dialogue
into Bence so `bd_plot` reaches 590 through the real conversation only.
Expected: all party victory barks at ~2 s cadence; public de Lancie chain + Bence 64–65
play; Bence exits; free control returns; player can talk, loot, save, reload before
Dazzo; NO private Waterdeep pitch, Corwin/Neera forced finale, Skie check, or any other
coda fires.

Result: **PASS** through native BDCUT58 staging, Caelar/Aun dialogue, full
BDCUT59/59A/59B, barks, public de Lancie/Bence dialogue, and playable celebration.
See the [2026-09-06 record](2026-09-06-ending-runtime.md).

## R2 — full six-person party, loaded inventories — PENDING

Marker in every Player1–6 slot (distinct resrefs, equipped + quick-slot + bag + loose),
near-full inventories. Run the success contract. Compare marker multiset in AR0602.

Result: _pending_ · Manifest: _pending_

## R3 — solo protagonist, empty and full inventory — PENDING

Two sub-runs from fresh copies: (a) inventory as empty as the game allows; (b) near-full.

Result (a): _pending_ · Result (b): _pending_

## R4 — Imoen + Skie in party — PENDING

Expected additionally: no Imoen displacement, no Skie death scene, no romance finale.

Result: _pending_

## R5 — one mod NPC + one dead/unconscious in-party companion — PENDING

Result: _pending_ · NPC used: _record_

## R6 — save/reload during celebration, then Dazzo — PASS

Result: **PASS** after native UI reload of `904VictoryBase`, followed by Dazzo and
the normal SoA arrival. See the [2026-09-06 record](2026-09-06-ending-runtime.md).

## R7 — multiplayer host/client smoke — PENDING

Result: _pending_

## R8 — once/re-entry protection — PENDING

Attempt to re-trigger Dazzo's ending option after it has fired once (reload the
pre-Dazzo save, run twice; and post-fire re-entry if reachable). Expected: no duplicate
CSRETBGT carrier, no duplicate import, `CSR_ENDING_USED` once-flag holds.

Result: _pending_

---

## Task 7 — standalone smoke (separate install) — PENDING

Target: `C:\Games\Baldur's Gate Enhanced Edition modded - scratch csr ending sod`
(disposable merged-SoD copy, prerequisite chain + 290 installed per plan Task 4).
Stage a save that has never visited BD4300; reach the preserved celebration; save at
free control. Dazzo → fade black → cutscene cleared → credits → main menu. No BD6100
visit, ambush, `sodcin05`, K# lookup, inventory mutation before termination, or
softlock. Repeat once from the saved celebration after reload; confirm Dazzo's ending
option is unavailable before plot 590.

Result: _pending_
