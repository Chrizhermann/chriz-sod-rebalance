# 19 — Dig-site scrying pool: full mechanics trace + PT-6 decision base

**Status: research complete (2026-07-13). All decisions OPEN — user picks.**
Issue: GitHub #6 (PT-6). Playtest source: `docs/playtest/2026-07-11-stream-playtest.md` PT-6.

Verified against: decompiled SoD scripts (`research/data/sod_baf/`) + live decompiles from
the **dev install** (`BDSCRY.dlg`, `cutskip.bcs`, `BDWIGHDD.CRE` — i.e. post-mod state with
comp120/comp220 installed).

## 1. The machine, end to end (verified)

**Pool object** `BDODSCRY.bcs` on BD1200 @(1325,2095):

1. 3× Silver Scepter `BDMISC55` slot into the pedestal (`BD_SDDD12_COUNTER` 0→3);
   the 3rd gives **+3,000 party XP** (`AddexperienceParty`).
2. Pool is cloudy (`BD_SDDD12_CLOUDY`=1). One **Essence of Clarity `BDMISC59`**
   clears it (CLOUDY→0, `TakePartyItem` — **the vial is consumed**).
3. Clicking the clear pool starts `BDSCRY.dlg` (invisible CRE "BDSCRY").

**Vision picker** `BDSCRY.dlg` (states 0 first time, 4 on re-visit):

| Reply | Once-flag (LOCALS) | Launches | Scene |
|---|---|---|---|
| "Imoen..." | `bd_sddd12_imoen` | `bdscry01`→(bdliia dlg)→`bdscry02` | BD0118: Imoen + Liia Jannath casting practice |
| "Caelar Argent..." | `bd_sddd12_caelar` | `bdscry03`→`bdscry3a`→(dlg)→`bdscry04`→`bdscry4a` | BD0071: Caelar + Oloneiros + ~150-spawn crusader army |
| "The Hooded Man..." | `bd_sddd12_hood` | `bdscry05`→(bdhepher dlg)→`bdscry06` | BD0070: Hephernaan + `CreateCreatureDoor("bdireni")` |

Every vision tears down through **`bdscry07`**: murky ambients back on,
**+500 XP to each of Player1–6** (`AddXPObject`), `EndCutSceneMode()`.

**The vial economy (key mechanic, easy to miss):** each dialog choice sets
`BD_SDDD12_CLOUDY` back to **1** *before* launching its cutscene. So the pool
re-clouds after every vision and **each vision costs one vial**. `bdscry07`'s
ambient flips are cosmetic; the global is reset in the dialog.

## 2. PT-6 findings

### 2a. Hooded-man vision: ALREADY REMOVED — no action needed
comp120's `csrhood.d` `ADD_TRANS_TRIGGER BDSCRY 0/4 ~False()~ DO 2` kills the
"The Hooded Man..." reply in both picker states (plus Imoen's dangling
follow-up in `BDIMOEN` 67). **Verified live** on the dev install: the installed
`BDSCRY.dlg` shows `False()` on transition 2 in states 0 and 4. The playtest
doc's "known comp120 sites" list (BD0103, BDCUT10/11, BDCUT28) was incomplete —
the component always covered the pool. `bdscry05/06` stay on disk as dead code
(unreachable, harmless).

### 2b. CUTSKIP: NOT APPLICABLE — verified clean
No `BDSCRY*` script calls `SetAreaScript("cutskip",OVERRIDE)` — the visions
never register with SoD's cutscene-skip rig, so they are not skippable and have
no mirrored end-state. Installed `cutskip.bcs`, `CUTSKIP1.bcs`, `CUTSKIP2.BCS`:
**zero** scry/`SDDD12` references. The issue-#5 failure mode cannot occur here.

### 2c. The missing vial: regression confirmed AND it gates content
`BDMISC59` world sources: the `Shelf` container @(1146,1230) in BD1200
(intact), and `BDWIGHDD` @(2474,1951) — schedule-zeroed by comp220
(`comp220_lists.tpa:177`, idx130). Sources 2→1.

Because each vision consumes a vial (§1), the count matters:

| State | Visions available | Vials | Result |
|---|---|---|---|
| Vanilla | 3 | 2 | max 2 of 3 watchable (vanilla already short-changes you) |
| + comp120 | 2 (Imoen, Caelar) | 2 | exactly balanced |
| + comp220 (current) | 2 | **1** | **only one of Imoen/Caelar watchable** |

`BDWIGHDD` itself is plot-inert — verified: death variable is `BDWIGHDD` (it is
NOT Brother Deepvein's quest wight `BD_DOD_WIGHT1`, a different actor), zero
script references anywhere in the 1232-script corpus, vial carried droppable
(item flags 0x0). Restoring or not restoring it breaks nothing either way.

### 2d. Third-party surface (compat)
Aura (Aura_BG1_2_EET) EXTERNs an interjection off `BDSCRY` state 0
(`C0AuraBDSCRY` → `C0AURA2J` 1965). Any approach that **keeps the dialog file
and gates replies** (comp120-style) or that simply never activates the pool
leaves Aura's hook dormant-safe. Deleting/replacing `BDSCRY.dlg` would be
Artisan-grade fragile — off the table per compat-first rule.

## 3. XP ledger stakes (for whichever option is picked)
- Scepter completion: +3,000 party (one-time).
- Per vision watched: +500 × 6 player slots via `AddXPObject` (up to 2 visions
  post-comp120, vial-limited to 1 today).
- A full-cut would remove up to 3,000 + 2×3,000-equivalent slot XP; a vial fix
  restores the second vision's 500/member to reachability.

## 4. Options (ALL OPEN — user picks)

**Vial fix (issue options a/b/c, plus one the trace surfaced):**
- **(a) Re-home** the wight's vial into an existing container near (2474,1951).
- **(b) Restore `BDWIGHDD`** — drop its entry from the comp220 cut list (one
  schedule un-flip; the list generator's count-guard `csr_cutn_bd1200` moves
  129→128 with it, regenerate or hand-adjust both).
- **(c) Fold into the vision pass** — decide vial economy as part of the
  content rework / full-cut below.
- **(d) — new, from the trace:** make one vial unlock the pool permanently:
  drop the `SetGlobal("BD_SDDD12_CLOUDY","MYAREA",1)` from BDSCRY states 1+2
  (D-file ALTER on our own tail component). One vial → both remaining visions;
  no ARE/CRE touch at all. Smallest diff that fully restores content access.

**Vision content (parked/decided elsewhere):**
- Hooded-man vision: **done** (comp120, §2a) — close this sub-item.
- Imoen vision: go-or-replace — user call. Nuance: with comp160 (Imoen stays in
  BG studying), the vision is arguably MORE canon than in vanilla.
- Caelar vision: park with the item-13 arc treatment (rewrite when Caelar's
  arc text lands).
- **Full-cut of the whole gimmick** (scepters/essence/visions): on the table,
  NOT decided. Mechanically clean path if picked: gate `BDODSCRY.bcs`'s dialog
  block (and scepter-slot blocks) rather than touching `BDSCRY.dlg` (§2d
  compat); ledger repay per §3.
