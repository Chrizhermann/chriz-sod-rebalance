# 17 — BG2(:EE) XP / Level-Tiered Encounters

**Provenance:** Research data gathered by subagent 2026-07-10 from the dev BG2EE+EET install
(read-only) + repo decompiles. DATA ONLY — decisions live in `docs/design/`.

**Sources / method (reproducible):** all 327 `AR*.BCS` area scripts extracted from the dev
install's BIFFs and decompiled to BAF in a scratch dir; `SPAWNGRP.2DA` + sample `AR*.ARE`
extracted and struct-parsed. SoD side grepped from `research/data/sod_baf/`. Install is
strictly read-only; nothing written to the game dir. Extraction command used:

```
weidu.exe --game "<dev install>" \
  --tlkin "<dev install>/lang/en_US/dialog.tlk" \
  --out . --biff-get "AR.*BCS"          # then: weidu.exe ... AR*.BCS   (decompile)
```
(The `--tlkin` is required — weidu's language auto-detect fails on this install with
`None of the dialog paths were a match against en_us`; pointing `--tlkin` straight at the TLK
bypasses it.)

**Verified against:** the 327 decompiled vanilla area scripts. No `AR*.bcs`/`AR*.are` are loose
in `override/` on the dev install (glob-verified) → the biffed vanilla scripts documented here
**are** the live BG2 area scripts (SCS did not overlay area scripts as loose overrides on this
install). Anything not directly observed is marked **UNVERIFIED**. Caveat: 2/327 scripts
(`AR5002`, `AR5501` — both Hexxat-DLC `OHH*` areas) only partially decompiled (an unresolved
extended trigger `0x40a8`); the recovered portions show no XP/level/difficulty gating, only DLC
companion spawns.

---

## 0. TL;DR — the headline findings

1. **The "lich at high XP" the user remembers is real and is a *scripted area* mechanism, but
   it is rare.** Across all 327 BG2 area scripts, **only two** gate spawns on raw XP:
   **`AR1401` (Umar Hills)** and `AR0406` (Athkatla, a DLC companion). AR1401 is the canonical
   example — it spawns three escalating waves keyed on **`XPGT(Player1, …)`**, topping out in a
   **Glabrezu** (a tanar'ri demon, not literally a lich) once the PC passes **1,000,000 XP**.
2. **The engine's real "party-power" primitive is `LevelParty*` (party *average* level), not
   XP.** ToB areas tier encounters with `LevelPartyGT/LT` bands, usually combined with party
   size (`NumInParty*`). This is the closest vanilla analogue to the user's "median XP" idea.
3. **Data-driven layer:** ARE **spawn points** can name a **`SPAWNGRP.2DA` group** instead of a
   creature; each group is an 8-row weak→strong creature ladder with a per-group difficulty
   weight. Area scripts then `SpawnPtDeactivate()` the easy or hard variant by party level
   (`AR5200`). Spawn *count* scales as `partyLevel × difficulty` (same engine path as the
   rest-ambush struct).
4. **No vanilla BG2 area computes a median, or gates anything on "≈2,000,000 XP."** The largest
   XP thresholds found are `XPGT(Player1,999999)` (AR1401) and the AR0406 companion bands.
5. **SoD already uses every idiom you'd need.** SoD companion scripts gate on `XPGT(Player1,N)`
   bands (join catch-up), and SoD area/creature scripts use `LevelParty*`/`Difficulty*` 317
   times across 30+ files. **BD1100/BD1200 themselves currently have *zero* level/XP gating** —
   greenfield. (BD1200 *is* the Coldhearth Lich's area: the 22,000-XP kill.)

---

## 1. Mechanism A — Area-script XP gating (`XPGT` / `XPLT` bands)

### Trigger idioms (verified in-scripts)
- `XPGT(O:Object*, I:XP*)` — object's total XP strictly greater than value.
- `XPLT(O:Object*, I:XP*)` — strictly less than.
- Bands are built by pairing them: `XPGT(Player1,299999) XPLT(Player1,1000000)` = "300k–1M".
- The object is almost always **`Player1`** (the protagonist). There is **no** median/party-XP
  trigger in the engine; `CheckStatGT(...,XP)` is **not used by any area script** (0 hits) and
  XP is not a `stats.ids` stat here.

### ⭐ Example 1 — `AR1401` (Umar Hills): three XP-tiered ambush waves
The plot spawns a base wave, then adds a **reinforcement wave whose creatures escalate with the
PC's XP**. The three blocks are mutually exclusive via the XP bands and a shared once-global
(`UmarPlotStarted` 1→2), so exactly one reinforcement set fires.

```
// base wave (UmarPlotStarted 0 -> 1): Umar + Imp + Salamander + Skeletons/Zombies + Skel Warrior
IF Global("UmarPlot","GLOBAL",1) !Global("RangerProtector","GLOBAL",6)
   Global("UmarPlotStarted","AR1401",0)
THEN SetGlobal("UmarPlotStarted","AR1401",1)
     CreateCreature("rumar01",…) CreateCreature("rzomb01",…) CreateCreature("skelwa",…) …

// MID tier — 300,000 to 1,000,000 XP: Salamanders + Wraith + Skeleton Warrior
IF … Global("UmarPlotStarted","AR1401",1)
   XPGT(Player1,299999)  XPLT(Player1,1000000)
THEN SetGlobal("UmarPlotStarted","AR1401",2)
     CreateCreature("icsalfir",…) CreateCreature("wraith01",…) CreateCreature("skelwa",…)

// HIGH tier — 1,000,000+ XP: Specters + GLABREZU + Wraith + Specters
IF … Global("UmarPlotStarted","AR1401",1)
   XPGT(Player1,999999)
THEN SetGlobal("UmarPlotStarted","AR1401",2)
     CreateCreature("spectr01",…) CreateCreature("demgla01",…) CreateCreature("wraith01",…)
```
Evidence: `AR1401.BAF` blocks at the `UmarPlotStarted` sequence (base ~L46-63; mid L65-78; high
L80-92). Creature IDs: `rzomb01`=Zombie, `skelwa`=Skeleton Warrior (low); `icsalfir`=Salamander,
`wraith01`=Wraith (mid); `spectr01`=Specter, **`demgla01`=Glabrezu** (high).

**Pattern to copy:** a plot-gated set-piece where a once-flag guards a *single* reinforcement
block chosen from `XPGT/XPLT` bands, keyed on `Player1`. This is exactly the shape the SoD
dig-site request describes.

### Example 2 — `AR0406` (Athkatla): XP-banded companion power
The Hexxat DLC recruit `ohhfak8` is (re)created inside XP bands so she joins at a level
appropriate to the party: `<125k`, `125k–180.5k`, `180.5k–300k`, `300k–600k`, `600k–1M`, `1M+`
(`XPGT(Player1,1000000)`), each setting `OHH_HEXXAT_INIT` to a tier her own script reads.
Evidence: `AR0406.BAF` ~L169-270. This is the **companion-scaling** flavor of the same idiom —
the analogue of SoD's own join-catch-up ladder (§4), not a monster-difficulty gate.

---

## 2. Mechanism B — Level / party-size gating (`LevelParty*` + `NumInParty*`)

**`LevelParty(I)` / `LevelPartyGT` / `LevelPartyLT` test the party's *average* level** (per
IESDP; corroborated here by vanilla thresholds — ToB areas use `LevelPartyGT(19..25)`, values
that are meaningful only as an *average*, not a sum). This is the engine's native
"is the party strong enough" measure and the nearest thing to a "party XP tier". Found in
**8 area scripts**, all SoA-late/ToB: `AR3001/3007/3012/3013/3016` (Saradush), `AR4000`
(ToB opening / Watcher's-Keep approach), `AR4500` (Pocket Plane), `AR5200` (ToB wilds).

### Example 3 — `AR4000`: Illasera ambush scaled by level × party size
Four mutually-exclusive spawn blocks pick the encounter version from **average level crossed
with headcount** (the `19/20` split = "pre-ToB vs ToB-tier", `NumInParty 3/4` = "small vs full"):
```
IF … OR(2) NumInParty(1) LevelPartyLT(10)      THEN …   // trivial party
IF … LevelPartyGT(19) NumInPartyLT(4)          THEN …   // strong, small
IF … LevelPartyLT(20) NumInPartyGT(1)          THEN …   // weak, grouped
IF … LevelPartyGT(19) NumInPartyGT(3)          THEN …   // strong, full  (hardest)
```
Evidence: `AR4000.BAF` ~L210-255 (`IllaseraSpawn`).

### Example 4 — `AR4500` (Pocket Plane): compute a difficulty *tier global*, then spawn from it
Two-stage pattern worth copying wholesale. **Stage 1** derives a tier (`Chall1_Diff` = 2/3/4)
from `LevelPartyGT/LT` bands × party size; **Stage 2** spawns tier-matched creatures:
```
// stage 1 — derive the tier
IF Global("BeginChallenge1","GLOBAL",1) Global("Chall1_Diff","AR4500",0)
   NumInPartyAliveGT(3) LevelPartyGT(23)   THEN SetGlobal("Chall1_Diff","AR4500",4) Continue()
… LevelPartyGT(21) LevelPartyLT(24) …      THEN SetGlobal("Chall1_Diff","AR4500",3) …
… LevelPartyGT(18) LevelPartyLT(22) …      THEN SetGlobal("Chall1_Diff","AR4500",2) …
// stage 2 — consume the tier
IF … Global("Chall1_Diff","AR4500",4) THEN CreateCreature("chevil01",…)   // hard variant
```
Evidence: `AR4500.BAF` tier-compute L363-431, consumers at L540/L614 (`Chall1_Diff==4`).

### Example 5 — `AR5200` (ToB wilds): level gate toggles which *spawn point* is live
The area ships two named spawn points, `EASYA` and `HARDA`; an `OnCreation()` block turns off
the wrong one by average level (split at 20):
```
IF OnCreation() Global("CheckLevel","AR5200",0) LevelPartyGT(19)
THEN SetGlobal("CheckLevel","AR5200",1) SpawnPtDeactivate("EASYA")   // strong party -> keep HARDA
IF OnCreation() Global("CheckLevel","AR5200",0) LevelPartyLT(20)
THEN SetGlobal("CheckLevel","AR5200",1) SpawnPtDeactivate("HARDA")   // weak party  -> keep EASYA
```
Evidence: `AR5200.BAF` L1-19. This is the **most SoD-idiomatic** pattern — SoD BD areas already
use named spawn points + `SpawnPtActivate/Deactivate`. (See §3 for what EASYA/HARDA point at.)

---

## 3. Mechanism C — Data-driven spawn points + `SPAWNGRP.2DA`

### The ARE spawn-point struct (verified offsets; header dword @0x60 = offset, @0x64 = count)
Per `bg-modding/ie-areas.md` + parse: entry 0xC8 bytes — `+0x00` name(32) · `+0x20/22` x,y ·
`+0x24` **10×resref creature table** · `+0x74` table count · `+0xAC` max spawns · `+0xB4`
enabled. **Engine spawn count scales `spawnamount = partyLevel × difficulty`, capped at max** —
the same rule as the rest-interrupt struct (`ie-areas.md`). So even with a fixed creature list,
a stronger party fights *more* of them.

### Two spawn-point styles (both verified by struct-parse)
- **Direct creatures** — e.g. `AR1400.ARE` (Umar Hills entrance): spawn points hold real
  resrefs (`BEARGR`, `CATTIG01`=tiger, `BEARBL`=black bear, `DOGWIL01`) — ambient wildlife, no
  tiering.
- **`SPAWNGRP.2DA` group reference** — e.g. `AR5200.ARE`: the `EASYA` point's table = **`RDFIRE1`**
  and `HARDA` = **`RDFIRE2`**. These are *column names* in `SPAWNGRP.2DA`, not creatures. The
  engine expands the group to an actual creature at spawn time.

### `SPAWNGRP.2DA` structure (extracted from DEFAULT.BIF; verified by parse)
- **62 columns** = named spawn groups (`RDGnoll`, `RDUndead`, `RDTan1`, `RDEye`, `RDFIRE1`…).
- Row **`Difficulty`** = a per-group weight (RDGnoll=20 … RDTan2=250) — the "cost/power" rating.
- Rows **`1`–`8`** = the creature resref for that group at each **power level** (weak→strong;
  `*` = empty). Exact ladders (parsed):

| Group | diff | tier1 | tier2 | tier3 | tier4 | tier5 | tier6 |
|---|---:|---|---|---|---|---|---|
| `RDGnoll` | 20 | gnlwar01 | gnlsla01 | gnlvet01 | gnleli01 | gnleli01 | gnlcap01 |
| `RDUndead` | 100 | Mummy01 | Mummy01 | Ghast01 | Mummy01 | Ghast01 | * |
| `RDUndea2` | 140 | Shadow01 | Shadow01 | Wraith01 | Wraith01 | shadfi01 | * |
| `RDTan1` (demons) | 200 | dquas01 | dglab01 | dglab01 | demmau01 | demmau01 | dquas01 |
| `RDTan2` (demons) | 250 | dglab01 | dglab01 | dquas01 | dquas01 | demsuc01 | demmau01 |
| `RDEye` (beholders) | 100 | Eyesek01 | Eyesek01 | Eyeegl01 | Eyeegl01 | Eyesnt01 | Eyesek01 |
| `RDFIRE1` | 200 | giafir01 | giafir01 | * | * | * | * |
| `RDFIRE2` | 200 | golbur01 | golbur01 | * | * | * | * |

So AR5200's EASY→HARD swap is `giafir01` (fire giant) → `golbur01`. Note ladders are **variant
pools**, not always monotonic (RDUndead alternates Mummy/Ghast; RDFIRE* only populate tiers 1-2).

**UNVERIFIED:** the exact engine rule for *which* of rows 1–8 fires for a given spawn (community
docs suggest a random/weighted pick bounded by the point's difficulty budget and party level; I
did not confirm it binary/in-game). Treat SPAWNGRP row-selection as fuzzy. Also, the numeric
`enabled`/`max`/frequency fields on the AR5200 points read as 0 in the file (they are
script-controlled), so the **load-bearing tiering there is the `LevelParty` → `SpawnPtDeactivate`
script gate (§2 Ex.5)**, not the ARE defaults.

---

## 4. Mechanism D — Game-difficulty gating (`Difficulty*`)

`Difficulty(I:diff*DIFFLEVL)` / `DifficultyGT` / `DifficultyLT` test the **game difficulty
slider** (`DIFFLEVL.IDS`: e.g. NORMAL, HARD/CORE, INSANE), not party power — but vanilla often
ORs it with a level check to reduce or boost spawns. Found in `AR3012`, `AR3013`, `AR4500`.

Example — `AR3013` (Saradush) thins the demon wave on easy settings *or* a weak party:
```
IF OnCreation() Global("ReduceDemons","AR3013",0)
   OR(2) DifficultyLT(NORMAL) !LevelPartyGT(16)
THEN SetGlobal("ReduceDemons","AR3013",1)
```
Evidence: `AR3013.BAF` L106-115. This is the "spawn *fewer/weaker* below a threshold" flavor —
complementary to the "spawn *more/deadlier* above a threshold" flavor of §1-2.

---

## 5. Trigger / action reference (for an EXTEND_TOP implementation)

| Primitive | Meaning | Notes for tiering |
|---|---|---|
| `XPGT(obj,n)` / `XPLT(obj,n)` | obj total XP >/< n | Band with both. Vanilla always uses `Player1`. |
| `LevelPartyGT(n)` / `LevelPartyLT(n)` | party **average** level >/< n | The party-aggregate primitive; no per-slot juggling. |
| `NumInParty(n)` / `NumInPartyGT/LT`, `NumInPartyAliveGT/LT` | headcount | Combine with level to scale for party size. |
| `Difficulty(x)` / `DifficultyGT/LT` (`DIFFLEVL.IDS`) | game difficulty slider | For INSANE-only extras / easy-mode thinning. |
| `SpawnPtActivate("name")` / `SpawnPtDeactivate("name")` | toggle an ARE spawn point | The AR5200 tiering lever. |
| `CreateCreature("res",[x.y],dir)` | scripted spawn | The AR1401 lever. |
| once-`Global(...)` guard + `SetGlobal(...)` | fire tier **once** | Mandatory — see §6. |

---

## 6. Application notes for SoD `BD1200` (DATA, not decisions)

Context: BD1100/BD1200 = the dwarven dig site / **Coldhearth Lich** area, remix party ≈ level
8-12. Goal: a BG2-style "deadlier creatures if the party is strong" wave.

**Expected party XP here (grounds thresholds):** SoD's own join-catch-up bands (`BDMINSC` etc.)
top out at `XPGT(Player1,249999)`, i.e. the game assumes ~135k-250k+/char at SoD *start*; the
dig site is shortly after. So `Player1` XP at BD1200 is roughly **150k-400k** for a level-8-12
PC — meaning **AR1401's 300k/1M thresholds are too high for SoD**; a SoD-tuned ladder would sit
lower (illustrative only: e.g. `<250k` / `250k-500k` / `>500k`, or gate the deadliest wave at
`XPGT(Player1,~450000)`). Cross-check against `docs/research/03-xp-economy.md` before choosing.

**Options, best-fit first:**
1. **`LevelPartyGT(n)` bands (recommended aggregate).** `LevelParty*` already means "party
   *average* level," so it *is* a party-wide tier with no empty-slot problem — the engine
   averages only real members. One `LevelPartyGT(11)` (or 10/12) split cleanly separates
   "under-levelled" from "strong" without touching XP at all. This is the ToB idiom (§2) and is
   the truest match to the user's "compute the party's median and react" intent.
2. **`XPGT(Player1,n)` bands (recommended if you want an XP feel / matches AR1401).** Simplest,
   and in SoD the PC has levelled alongside the party so `Player1` XP ≈ party median in practice.
   One trigger, no counting. This is literally the Umar Hills shape.
3. **Named EASY/HARD spawn points + `SpawnPtDeactivate` by level (most SoD-idiomatic).** Author
   two spawn points in BD1200's ARE (or two scripted waves), then an `OnCreation()` EXTEND_TOP
   block deactivates the wrong one by `LevelPartyGT` — the AR5200 pattern. Plays nicely with
   SoD's existing spawn-point usage.
4. **True per-player "median" (NOT recommended — awkward in BCS).** There is no median trigger.
   You would `XPGT(Player2,n) … XPGT(Player6,n)` per slot and *count* how many pass, but BCS has
   no clean counter. **Caveat:** for an empty slot, `Player2..Player6` resolve to an invalid
   object and the `XPGT` simply evaluates **false** (no error) — so naive "all six > n" logic
   fails for any party < 6. Prefer #1 (`LevelParty` already aggregates) over hand-rolling this.

**Mandatory implementation caveats:**
- **Fire the tier ONCE.** `XPGT/LevelParty*` re-evaluate every script pass; without a once-global
  (AR1401's `UmarPlotStarted` 1→2 guard) crossing a threshold mid-fight double-spawns. Gate the
  whole thing behind a plot/`OnCreation` once-flag and `SetGlobal` it immediately.
- **EXTEND_TOP staging (compat).** Per `bg-modding/ie-scripting.md`: once-flag the block as its
  first action and end with `Continue()` so SoD's own EET bootstrap / other EXTEND_TOPs in
  BD1200 still run the same pass.
- **`AddexperienceParty` unit** (`03-xp-economy.md`): thresholds are on *per-character* total XP
  (what `XPGT` reads), which is the right unit for a level-8-12 gate.

**SoD baseline facts (grepped `research/data/sod_baf/`):**
- SoD uses `XPGT(Player1,N) XPLT(Myself,N)` bands only for **companion join catch-up** (BDMINSC/
  BDCORWIN/BDEDWIN/…) — no SoD *area* script tiers a monster spawn by XP.
- `LevelParty*`/`Difficulty*` appear **317×** across 30+ SoD scripts (mostly boss/NPC AI:
  BDARCH00, BDBARD01, BDBELHIF, BDABISHA, BDASHIRU; some area scripts: BD2000/3000/4000/5000/
  5100/7000…). The triggers are native and known-good on this engine build.
- **BD1100 and BD1200 contain no `LevelParty`/`Difficulty`/`XP` gating today** (not in the match
  set) — adding a tiered wave is greenfield and won't collide with existing gates.
