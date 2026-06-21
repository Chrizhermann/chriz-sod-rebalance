# Design 02a — Trash-Cut Proposal: SoD Prologue + Coast Way

Status: **proposal / not implemented** (markdown only; WeiDU tail-mod comes after sign-off).
Date: 2026-06-21. Scope: BD00xx, BD01xx, BD10xx, BD11xx, BD12xx + the BD006x travel-ambush pool.
Sources: inventory `docs/research/02a-encounters-prologue-coastway.md`, master dataset
`docs/research/sod_encounters_full.csv`, totals `docs/research/02d-encounter-totals.md`.
Related design: rest-ambush `docs/design/01-rest-ambush-design.md`, XP `docs/design/03-xp-reweight.md`.

## Framing & conventions

- **Counts are "Core baseline" = the fixed pre-placed actor population in each `.are`.** Placed actors
  do **not** scale with difficulty, so these cuts apply **identically on the user's Insane setting**.
  The "≈2× Insane" multiplier the user feels comes from the *dynamic* sources — difficulty-gated
  scripted blocks (already counted at their HARDEST branch here) and the rest/spawn-amount formula
  (`partyLevel × difficulty`, capped at `max`) — which Insane pushes to the cap. Those are addressed
  by the rest-header levers in Design 01, **not** by deleting placed actors. Net: a placed-actor cut
  is a clean, difficulty-independent reduction; the rest cap is the second, multiplicative lever.
- **Implementation** = `COPY_EXISTING` each `BD*.are`, remove the targeted actor-table entries (or
  flag them never-spawn), reversible backup. No `.bcs`/`.dlg` edits except where a "make meaningful"
  upgrade explicitly rebuilds a boss script. Scripted-wave removal = NOP the relevant `CreateCreature*`
  response blocks via `COMPILE`/`EXTEND` (reversible). Story dialogue and the Korlasz **surrender
  branch** are preserved.
- **XP caveat:** cutting ~370 mobs removes encounter XP. This MUST be compensated by the big-quest XP
  reweight in `03-xp-reweight.md` so total progression is preserved. Flagged per area where heavy.
- **"Keep" picks are category-level.** Exact elite-guard CRE selection (which skeleton/wight variant
  is the "elite") should be confirmed against CRE stats at implementation; resrefs below are the
  current placed roster, not yet stat-verified for relative power.

## Leave-alone: Ducal Palace + Baldur's Gate city

BD0010–BD0050, BD0100–BD0112, BD0116–BD0121 are ~99% non-combat (1000+ neutral ambience actors).
The only combat is two small **story** beats — **keep as-is**:
- **BD0100** palace assassination — `BDGASS5`×3 placed + `bdgass1/2/3` scripted (≈6). Story.
- **BD0103** Imoen's room — `bdgass1`/`bdgass4` (≈2). Story.
- **BD0117** doppelganger reveal — `bdffdopp`×1 (neutral→hostile). Story.
No cuts. (City rest headers are `BDNOREST` town no-rest; no change — see Design 01.)

---

## Part 1 — Korlasz Prologue Dungeon (the linear prologue combat)

### BD0113 — Wyrmling chamber — **KEEP (4 → 4)**
`BDWYRML1`×3 + `BDWYRMLI`×1. Small, thematic, already a tidy set-piece. No cut.
(Rest header: 57/57 felt @max3 — soften per Design 01.)

### BD0114 — Spider nest — **40 → 11 (−72%)**  ★ make-meaningful candidate #3
Current placed: `SPIDSM0_`×11, `SPIDSW`×8, `SPIDGI`×8, `SPIDPH`×6, `SPIDWR`×2, `SPIDPHAS`×2,
`BDSPIDGA`×2, `BDSPID7L`×1. Plus scripted `SPIDPHAS`×2 (hard) and a neutral beetle sub-script.

**Option A — Matriarch brood (recommended):** promote **`BDSPID7L`×1** to a Sword Spider Matriarch
(buff HP/THAC0/poison at implementation), surround with a tight brood.
- **KEEP (11):** `BDSPID7L`×1 (matriarch), `SPIDGI`×3, `SPIDPH`×2, `SPIDSW`×2, `BDSPIDGA`×2,
  `SPIDPHAS`×1.
- **REMOVE (29):** `SPIDSM0_`×11 (whole filler swarm), `SPIDSW`×6, `SPIDGI`×5, `SPIDPH`×4, `SPIDWR`×2,
  `BDSPIDGA`×0… (i.e. trim each stack to the keep count). **Drop the scripted `SPIDPHAS`×2 wave.**

**Option B — Plain cut:** same 40 → ~12, no matriarch buff. Lower effort; less memorable.

### BD0120 — Korlasz catacomb L1 — **12 → 6 (−50%)**
Current placed: `BDSHIS01`×3, `BDSHIS02-07`×1 each (shades), `BDOGRE01`×1, `BDSHME01`×1.
This is the dungeon's first room — keep some teeth as a warm-up before the climax.
- **KEEP (6):** `BDOGRE01`×1 (mini-boss ogre), `BDSHME01`×1, `BDSHIS01`×2, `BDSHIS02`×1, `BDSHIS03`×1.
- **REMOVE (6):** `BDSHIS01`×1, `BDSHIS04/05/06/07`×1 each.
(Rest header: **39/39 felt @max6 diff80 = always 6 skeletons** — the prologue's worst rest. Design 01
must drop this dungeon to near-restful: day/night→1–2, max→1–2.)

### BD0130 — Korlasz catacomb L2 (boss) — **~109 live → ~18 (−83%)**  ★ make-meaningful #1
Current: **81 placed** undead + **~28 scripted skeleton/bonebat reinforcement waves** (≈109 live).
Placed roster (top): `BDSHAD04`×8, `BDSHZOM1`×6, `BDSKGR04`×5, `BDSKGR02`×4, `BDSKGR00`×4, `GHAST`×4,
`BDBONBAT`×4, `BDSHIS09`×4, `BDSKGR05`×3, `BDSHSOUL`×3, `BDSKGR01`×3, `BDWIGHT1`×3, `BDWRAI02`×3,
`BDSKGR06`×2, `BDSKGR07`×2, `BDWIGHT2`×2, `BDWIGHT3`×2, `BDSHIS10`×2, `BDSKGR03`×2, + singles
(`BDMUMM01`, `BDOGRE02`, `BDGHASTG`, `BDSHME01-03`, `BDUNSLGU`, `BDSHKFAM`, `BDSHADGR`, `BDKORME8/9`,
various `BDSHIS0x`). Boss **`bdkorlas`** is script-handled (surrender branch via `BD_KORLASZ_SURRENDER`).

**Rebuild as a real boss fight:**
- **DROP all ~28 scripted reinforcement waves** (NOP the wave `CreateCreature*` blocks). They are the
  attrition engine; their removal is the single biggest quality win here.
- **KEEP ~17 as a curated honor guard + Korlasz (≈18 total):**
  `bdkorlas` (boss — buff to boss-tier at implementation; **preserve surrender branch**),
  `BDSHKFAM`×1 (her shadow familiar — thematic), `BDMUMM01`×1 (mummy lieutenant),
  `BDWRAI02`×2 (wraith guards), `BDWIGHT1`×2 + `BDWIGHT2`×1 (wight honor guard),
  `BDSHAD04`×2 (shadow assassins), `BDSHADGR`×1 (greater shadow), `BDSKGR05`×2 + `BDSKGR06`×2
  (elite skeleton warriors), `BDOGRE02`×1, `BDGHASTG`×1.
- **REMOVE ~63 placed:** all `BDSHIS0x` shade clutter (~14), `BDSHZOM1`×6, `GHAST`×4, `BDBONBAT`×4,
  `BDSHSOUL`×3, `BDSKGR00/01/02/03/04/07` archer/grunt mass (~20, keep none of the filler tiers),
  `BDUNSLGU`×1, `BDSHME01-03`, `BDKORME8/9`, etc.
- **Heavy XP loss here** → route the removed XP into the Korlasz quest-completion reward (Design 03).

**Prologue dungeon subtotal: ~165 live → ~39 (−76%).**

---

## Part 2 — Coast Way Crossing & approach

### BD1000 — Coast Way Crossing (Flaming Fist camp) — **24 → 8 (−67%)**
Enemies are on the wilderness fringe (the camp NPCs are 136 neutral, untouched). Placed enemy:
`BDSPIDGA`×4, `SPIDSW`×4, `SPIDGI`×3, `SPIDHU`×3, `SPIDPH`×3, `ZOMBIE`×2, `BDDEADOG`×2, `BDMENGO`×1,
`BDWRAI01`×1, `BDBEARBR`×1.
- **KEEP (8):** one spider den — `BDSPIDGA`×2, `SPIDGI`×2, `SPIDHU`×1, `SPIDPH`×1 — plus `BDBEARBR`×1
  and `BDWRAI01`×1 (lone wraith for flavor).
- **REMOVE (16):** `SPIDSW`×4, `BDSPIDGA`×2, `SPIDGI`×1, `SPIDHU`×2, `SPIDPH`×2, `ZOMBIE`×2,
  `BDDEADOG`×2, `BDMENGO`×1.
- **Spawn points:** all **7 are already `enabled=0`** (Wolves×2, Worgs, Spiders×2, Bears×2, max 6) —
  **leave disabled** (do not enable). The rest header (49/57 felt @max3) is the active dynamic source;
  soften per Design 01.

### BD1010 — Spider/Mimic cave — **~18 → ~9 (−50%)**  ★ make-meaningful (variety beat, alt #3)
Placed: `SPIDSW`×2, `SPIDWR`×2, `SPIDPH`×2, `BDSPIDGA`×2, `SPIDPHAS`×1 (+`BDDEADOG`×1). Scripted
**`BDMIMIC`** ambush + `JELLOC`×4 + `BDOTYG01` + phase spiders (difficulty-scaled; HARDEST branch ≈9).
The Mimic trap is characterful — **preserve it** as the encounter's hook; cut the spider filler.
- **KEEP:** `BDMIMIC`×1 (the set-piece), `BDOTYG01`×1, `JELLOC`×2 (from 4), `SPIDPH`×2, `BDSPIDGA`×1.
- **REMOVE:** `SPIDSW`×2, `SPIDWR`×2, `BDSPIDGA`×1, `SPIDPHAS`×1, `JELLOC`×2.
- **Judgment call:** this is a lighter (50%) cut because it's set-piece-leaning; deepen to ~65% if the
  user wants strict ~70% everywhere.

---

## Part 3 — Coldhearth Lich crypt (BD1100 / BD1200)  ★ make-meaningful #2

> **Region flag:** BD1100/BD1200 sit in the scoped BD11/BD12 numbering but are an **optional,
> Coast-Way-tier crypt**, not the linear prologue. The biggest single undead glut in the whole region
> lives here (203 combined). Confirm inclusion — it's the highest-payoff cut.

### BD1100 — Coldhearth crypt, upper — **85 → 22 (−74%)**
Filler approach corridor. Placed (top): `BDMCARRI`×12 (carrion crawlers), `BDSHZOM1`×10, `ZOMBIE`×9,
`GHOUL`×9, `GHAST`×8, `BDWIGHT3`×6, `BDCCRAW1`×6, `BDGHASTG`×5, `BDUMBER1`×4 (umber hulks),
`BDWIGHT1`×4, `BDGHAST`×3, `CARRIO`×2, `BDWIGHT2`×2, + singles (`BDWIGHT`, `BDWRAI02`, `BDOTYG01/02`,
`BDMUMM01`). Keep a **sampler gauntlet** (one credible pack of each signature type):
- **KEEP (22):** `BDUMBER1`×2 (the scary ones), `BDMCARRI`×3, `BDCCRAW1`×2, `BDSHZOM1`×3, `ZOMBIE`×2,
  `GHOUL`×2, `GHAST`×2, `BDWIGHT3`×2, `BDGHASTG`×1, `BDMUMM01`×1, `BDWRAI02`×1, `BDOTYG01`×1.
- **REMOVE (63):** the bulk duplicates — `BDMCARRI`×9, `BDSHZOM1`×7, `ZOMBIE`×7, `GHOUL`×7, `GHAST`×6,
  `BDWIGHT3`×4, `BDCCRAW1`×4, `BDGHASTG`×4, `BDUMBER1`×2, `BDWIGHT1`×4, `BDGHAST`×3, `CARRIO`×2, etc.

### BD1200 — Coldhearth crypt, lower (boss) — **118 → 28 (−76%)**
The `BDCOLDH` **Coldhearth Lich** + `BDMISC60` **phylactery** puzzle (kill → respawns unless
phylactery destroyed) is the region's best mechanic — make it the star with a curated throne guard.
Placed (top): `BDBONBAT`×17, `BDDEAD01`×10, `BDSHSOUL`×10, `BDSKGR04`×9, `BDSHZOM1`×9, `ZOMBIE`×6,
`BDSKGR05`×5, `BDWIGHT1`×5, `BDSKGR03`×4, `BDWIGHT2`×4, `BDSKGR06`×4, `BDSKGR01`×3, `BDSKGR02`×3,
`GHOUL`×3, `GHAST`×3, `BDWIGHT3`×3, `BDGHASTG`×3, `BDMUMM01`×3, `BDWRAI02`×3, `BDSHAD04`×2,
`BDSHADGR`×2, `BDSKGR08`×2, `BDSKGR07`×2, + uniques `BDBRONZE`×1, `BDUNSLGU`×1, `BDWIGHDD`×1.
- **KEEP (28, + the lich):** `BDCOLDH` (boss, **preserve phylactery mechanic intact**), the uniques
  `BDBRONZE`×1 + `BDUNSLGU`×1 + `BDWIGHDD`×1 (distinctive guardians), `BDSHADGR`×2, `BDSHSOUL`×3
  (thematic for a lich), `BDMUMM01`×2, `BDWRAI02`×2, `BDBONBAT`×4 (atmosphere, from 17),
  `BDSKGR05`×2 + `BDSKGR06`×2 (elite skeletons), `BDWIGHT1`×2 + `BDWIGHT2`×1, `BDSHAD04`×2.
- **REMOVE (~90):** `BDBONBAT`×13, `BDDEAD01`×10, `BDSHSOUL`×7, `BDSKGR04`×9, `BDSKGR01/02/03/07/08`
  (≈14), `BDSHZOM1`×9, `ZOMBIE`×6, `GHOUL`×3, `GHAST`×3, `BDWIGHT3`×3, `BDGHASTG`×3, `BDWIGHT1`×3, etc.

**Coast Way + Coldhearth subtotal: 245 → 67 (−73%).**

---

## Part 4 — World-map travel-ambush arena pool (BD006x)

> **Mechanic flag:** these are entered via **overland-map travel ambush** ("You have been waylaid…"),
> **not rested in**, and the pool is **shared game-wide** (not prologue-specific). Cutting per-instance
> size here reduces every chapter's travel ambushes. Two independent levers: (a) per-instance mob count
> (this section), and (b) travel-ambush **frequency** (a separate worldmap setting — flag for Design 01
> follow-up; not an `.are` rest header).

Thin hard (repeatable trash). Per arena (placed; `*D` corpse props already excluded):

| Arena | Theme | Before | Keep | After | Cut |
|---|---|---:|---|---:|---:|
| BD0060 | Orc/troll | 8 | `BDURE1A`×2, `TROLL01`×1 | 3 | −63% |
| BD0061 | Troll | 9 | `TROLL01`×2, `TROLFR01`×1 | 3 | −67% |
| BD0062 | Frost-troll + ooze | ~10 | `TROLFR01`×2, `JELLOC`×1 (drop ooze-wave script) | 3 | −70% |
| BD0063 | "Dead-magic" (URE2) | 5 | `BDURE2A`×1, `BDURE2B`×1 | 2 | −60% |
| BD0064 | Hill-giant | ~6 | `BDURE4A`×1 + scripted `BDURE4D`×1 | 2 | −67% |
| BD0066 | **Goblin horde** | 41 | `BDGOB01`×2, `BDGOB02`×2, `BDGOB07`×2, `ANKHEG`×2 | 8 | **−80%** |
| BD0067 | Myconid | 13 | `BDMYCRD`×2, `BDMYCBL`×1, `BDSHRIE2`×1 | 4 | −69% |
| BD0065/0070/0071/0072 | (empty) | 0 | — | 0 | — |

**Travel-ambush pool subtotal: ~92 → ~25 (−73%).**

---

## Region summary

| Sub-region | Before | After | Removed | % cut |
|---|---:|---:|---:|---:|
| Ducal Palace + city (story, leave alone) | 9 | 9 | 0 | 0% |
| Korlasz prologue dungeon (BD0113/0114/0120/0130) | ~165 | ~39 | ~126 | **−76%** |
| Coast Way Crossing + Coldhearth crypt (BD1000/1010/1100/1200) | 245 | 67 | 178 | **−73%** |
| Travel-ambush arena pool (BD006x) | ~92 | ~25 | ~67 | **−73%** |
| **Region total** | **~511** | **~140** | **~371** | **−73%** |

Hits the ~70% target with the deepest cuts concentrated where the glut is (Coldhearth 203→50,
Korlasz L2 ~109→18). Three encounters are *upgraded*, not just shrunk: Korlasz boss, Coldhearth lich,
spider matriarch.

## Judgment calls for the user

1. **Coldhearth crypt (BD1100/1200) inclusion** — it's optional Coast-Way-tier content, not linear
   prologue, but it's the single biggest undead glut (203). Include in this cut? (Recommended: yes.)
2. **Korlasz L2 aggressiveness** — ~109→18 (−83%) is the boldest cut. OK to go that hard, and do you
   want `bdkorlas` *buffed into a real boss* (more design + a `.bcs` touch) or just *fewer mobs around
   the existing Korlasz*? Surrender branch is preserved either way.
3. **Spider nest BD0114** — matriarch-brood upgrade (Option A, buff `BDSPID7L`) vs. plain hard cut
   (Option B)? And BD1010 Mimic — keep the lighter 50% cut (preserve the trap) or force ~70%?
4. **Travel-ambush pool is game-wide** — cutting BD006x per-instance size affects *all* chapters'
   travel ambushes, not just prologue/coastway. Confirm that's desired here, or defer the pool to a
   global pass. Also: pair with a travel-ambush **frequency** cut (separate worldmap lever)?
5. **Insane interpretation** — confirmed: placed-actor cuts are difficulty-independent (apply as-is on
   Insane). The ≈2× Insane feel is the dynamic rest/spawn lever (Design 01). Want both shipped together?
6. **"Sampler gauntlet" vs deep curation** in the crypts — keep one pack of each undead type (current
   proposal, preserves variety) or curate harder around a tighter theme?
7. **XP** — ~371 removed mobs is significant XP. Confirm the Design 03 quest-reward reweight covers it
   (esp. Korlasz + Coldhearth quest completions) so prologue progression isn't gutted.
