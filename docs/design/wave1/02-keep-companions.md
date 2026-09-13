# Wave 1 — Keep All Companions at SoD Start

**Status: SIGNED OFF (user, 2026-07-03); implemented as component 110; first in-game test
PASSED (user, 2026-07-05 — party kept through Korlasz dungeon + palace).** Duplicate-suppression
at the recruiter sites still to be play-verified (see testing notes). All script facts below
verified against the live install (file:line evidence in the session's verification transcripts).

**Continuity gap identified 2026-09-10:** component 110 protects party retention and
recruiter placement, but does not generally adapt returning companions' SoD quest roles.
The user approved a small conditional Khalid/Bridgefort rewrite as component 115;
see [the continuity record](../../plans/2026-09-10-khalid-continuity.md).
Component 115 is ready for v0.6.10. After correcting the arrival protection, native
BD2000 entry, normal wardstone transport and Adirran's briefing passed with Khalid
controllable; save 954 retains party allegiance 2. Native reload and later quest
branches remain unverified. The earlier finale test had bypassed fort continuity.

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

**3. Other transfer mechanics.** BD0120's giant companion-spawn pool is new-game-only
(`SOD_fromimport=0`, dead code on EET imports). The camp system (`BDPARTY`) only relocates
existing globals. SoD's end strip (`BDCUT61`) removes Player2–6 generically — no seam work
(and our ending rework replaces that sequence later anyway).

## Returning companions' quest continuity (2026-09-10)

The user raised Khalid's Bridgefort role as a missing consequence of keeping BG1 companions.
This is separate from optional step-2 placement of companions who were not in the party.
The initial audit below describes component 110's gap. The approved modest treatment
is implemented separately as 115 for v0.6.10. Native entry/control and initial briefing
are now accepted, separately from the earlier prologue and finale tests.

- **Implemented:** `baf/skip2000.baf:1-8` sets `bd_khal_spawn=1` for an in-party Khalid.
  This skips recruiter placement; it does not complete or reroute his Bridgefort quest.
- **Unchanged by 110:** `research/data/sod_baf/BD2000.baf:278-307` moves/faces Khalid in
  surrender; `:471`, `:577`, and `:589` give battle-command barks; resolution blocks at
  `:902-904` and `:921-923` write default-location/retreat locals. Component197 preserves
  that staging (`lib/comp197.tpa:156-165`). Party-member targets need separate guards.
  The first wardstone entry also moves Khalid separately (`BDCUT24.baf:22`); Jegg's
  stakeout scenes create an unguarded Khalid (`BDC205CA.baf:6`, `BDC205CB.baf:6`).
  Recruiter suppression is not campaign-wide duplicate protection.
- **Dialogue/progression:** import wires Khalid to `KHALIJ` (`BDINTRO.baf:294-301`),
  while recruiter placement assigns `BDKHALID`. Read-only inspection on September 10
  found command/turn-in entries in `BDKHALID`48-51/70 without matching `KHALIJ` entries.
  `BDBFORT`2/3 externally enter `BDKHALID`27/28, so initial entry is not simply absent;
  resolving that route for carried Khalid and resuming it still needs native acceptance.
- **Static contradiction:** `BDKHALID.baf:9-35` starts the Jaheira reunion at plot 251-294
  when she is visible without checking prior separation. Dev `KHALIJ`190/192 describe
  days without contact, even if both companions travelled together throughout SoD.
- **Approved treatment:** existing defender Adirran supplies the carried route's local
  briefing and commands; Khalid contributes from the party without forced departure.
  The original fort route stays when he was not carried over.
- **Implemented in 115:** conditional quest dialogue, journals, banter/biography and
  scene guards. Voghiln's Jaheira-rescue introduction is guarded for carried Jaheira:
  its original peaceful branch excludes in-party Jaheira and can fall into hostility.
  His independent recruitment remains. The linked record preserves September 10
  installer/dev evidence and the corrected September 14 entry/briefing acceptance.
- **Remaining audit:** Jaheira's Khalid-related dialogue, Dorn's captivity/release,
  Neera's fort introduction/personal quest, and other returning-companion assumptions.
  `baf/skip0110.baf:1-12` already suppresses Safana's Coran breakup for carried Safana;
  this does not establish coverage of the other companions.
- **Acceptance boundary:** carried Khalid's normal entry, wardstone transport and
  Adirran briefing passed without a manual control repair. His saved party
  allegiance 2 is verified; native reload, non-carried routes, dismissal/death/rejoin
  variants and later quest choices/rewards remain unverified. The user authorized
  shipment now; Wynan's separate observation is a non-blocking sidenote.

Track the chapter treatment in [road north](../chapters/03-roadnorth.md), item 9.

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
