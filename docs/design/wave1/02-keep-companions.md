# Wave 1 — Keep All Companions at SoD Start

**Status: SIGNED OFF (user, 2026-07-03).** All script facts below verified against the live
install (file:line evidence in the session's verification transcripts).

## Decided (user, 2026-07-03)
- **Step 1 (this component):** nobody is force-stripped after Sarevok — the whole BG1 party,
  including the 17 companions with zero SoD content, walks into SoD and stays. Silent
  passengers are acceptable.
- **Step 2 (later, separate):** optionally place non-party companions somewhere in SoD as
  pickups, maybe with a little dialogue.
- Imoen is **not** part of this component — her absence is structural (escort NPC, poisoning
  plot) and is handled in the prologue chapter pass.

## How the strip works (verified)
The full party already transfers into SoD (`BDSODTRN`) and walks Korlasz's dungeon. The strip
is a single script: `BD0103.bcs` (Ducal Palace guest room), gated `BD_PLOT<51` —
**28 independent per-NPC blocks** (L227–621), each just `[bdresurr,] LeaveParty(),
SmallWait(1), DestroySelf(), Continue()`. No flags, no cross-dependencies. Mod NPCs (Aura,
Bristlelick) and jastey-Ajantis have their **own** strip blocks patched into the same script.

## The patch (3 parts)

**1. BD0103 block surgery.** Remove/neutralize exactly the 28 vanilla per-NPC strip blocks.
They have no guard variable, so this is `DECOMPILE_AND_PATCH` + targeted block removal.
Preserve verbatim: the final scene block (L728–786: `BD_PLOT=51`, TextScreen, Treasury Note,
14-day AdvanceTime, bed-positioning — it already positions all six sleepers, so a full party
works), the K#FP EEex stat-capture blocks (user's fixpack), the `BD_HAS_*` import-dedup
flags, and the Imoen container move. **Mod-NPC strip blocks stay untouched** — their mods
own their SoD behavior.

**2. Recruiter-site skip-blocks.** Every SoD recruiter site is `BeenInParty`-forked and the
level-7 CREs share the originals' death variables (verified byte-level, all 15), so a kept
original naturally suppresses the duplicate `CreateCreature`. BUT 10 revive-existing blocks
lack an in-party guard and would **MoveGlobal-yank a kept party member** out of formation,
reset their `bd_joined` locals, set EA NEUTRAL, and swap AI mid-party (Dorn even has his gear
confiscated at BD2000). Fix: `EXTEND_TOP` each script with a skip-block —
`InPartyAllowDead(x) → SetGlobal(<spawn-guard>) + Continue()`:

| Script | NPC(s) (unguarded block) |
|---|---|
| BD0101 | Viconia (Minsc/Dynaheir/Safana already guarded) |
| BD0108 | Minsc, Dynaheir |
| BD0110 | Safana |
| BD0111 | Rasaad |
| BD1000 | Edwin, Baeloth |
| BD2000 | Khalid, Dorn (incl. `dorn_chest` gear confiscation) |
| BD2100 | Neera |
| BD7000 | Rasaad |
| BD7100 | Jaheira |

**3. Nothing else needed.** BD0120's giant companion-spawn pool is new-game-only
(`SOD_fromimport=0`, dead code on EET imports). The camp system (`BDPARTY`) only relocates
existing globals. SoD's end strip (`BDCUT61`) removes Player2–6 generically — no seam work
(and our ending rework replaces that sequence later anyway).

## Known step-1 limitations (by design, revisit in step 2)
- Kept **BG1-only** companions dismissed mid-SoD stand where dismissed and get left behind
  (their dialogues have no camp logic). SoD-native ones are rescued by the vanilla camp
  catch-up blocks at BD1000/BD3000.
- SoD-native kept companions are already SoD-wired by `BDINTRO` at import (SoD dialog + AI),
  so they banter normally; the 17 others stay on BG1 dialogue = silent.
- The party-wide backpack impound (`PlayerChest00`, migrates with the camps) is left as-is —
  it's not companion-specific and the gear stays reachable.

## Pre-implementation check (one console test on the dev copy)
`BeenInParty()` semantics for a *currently-in-party* member underpin the suppression logic
(HIGH confidence, engine-standard). The patch is robust under either semantics, but verify
once in-game before shipping.

## Compat
`EXTEND_TOP` composes with anything; the BD0103 surgery pattern-matches the vanilla blocks
and skips gracefully if a block is absent (already modified by something else). Works
identically on EET and standalone SoD (same scripts); no engine/2DA edits.
