# Playtest log — 2026-07-11 (live install, pre-stream run)

Live install = `C:\Games\Baldur's Gate II Enhanced Edition modded`, mod at v0.5.0
(100-250 + 900) plus the direct-override dig-site polish. User plays, drops
observations; each becomes a tracked issue with research attached, fixed in parallel.

Status legend: **OPEN** (captured, researched, not fixed) · **FIXING** · **DONE**

---

## PT-1 — SoD starts in the Korlasz dungeon for ~2 seconds — OPEN (question)

**User:** "Does SoD have to start in the dungeon for 2 seconds? Can we not just fire
everything one to one in the palace or would that be too hard to change?"

**Research (already known — comp140 design, `lib/comp140.tpa` header + `baf/blk0120.baf`):**
Not a bug; a deliberate, documented trade-off. The party lands in BD0120 (dungeon
entry) because BD0120's area script is where the ENTIRE bootstrap runs:
- EET new-game machinery (`K#*` blocks), gear/gold handouts, BDKEYR, the Imoen
  import strip, the BG1 journal cleanup;
- every BDINTRO companion block (import wiring, the fresh-flow JoinPartyOverride
  pool, Safana auto-join, C0Aura/L#BRIST third-party mod hooks);
- **the fresh-start Bhaalspawn ability grants** (`BD0120.baf:481-573`, SPIN101-106 via
  `Switch("K#BhaalSpawnAbilityN")`) — these only fire on an ORDINARY BD0120
  area-script pass with `bd_plot!=0` + `K#NewGame=2`. Chaining the exit cutscene
  directly (BDDEBUG-style) silently costs fresh starts their Bhaalspawn abilities.
One implementation covers EET import AND fresh start precisely because we let BD0120
run. `blk0120.baf` already EXTEND_TOPs a `FadeToColor([1.0],0)` as the first action
of the first pass, so the visible flash is area-load time only.

**Assessment:** "fire everything in the palace" = re-hosting all of the above into
BD0103, including third-party mod hooks we do not control. High-risk, low-reward —
recommend NOT doing it. What IS worth investigating: whether the residual ~2s can be
shortened further (the 1-3 interposed script passes run on a black screen; check
whether the exit block can fire on pass 1 instead of waiting for the grant blocks).

---

## PT-2 — NPCs spawn then despawn on the first trip down from the bedroom — OPEN (bug?)

**User:** "When going down one floor from the bedroom for the first time in SoD, why
do we see some people, that despawn? Why are they spawned in the first place? I would
prefer they not spawn at all."

Bedroom = BD0103 (palace guest room). One floor down = BD0102 (great hall).

**Research (partial — needs finishing):**
`BD0102.baf` re-stages the SAME council cast at MANY plot values — each block does a
fresh `CreateCreature` set of BDGASS6 (Assassin), BDELTAN, BDBELT, BDSKIE, BDENTAR,
4× bdfistcc, bdjospil, BDSCHAEL/BDLIIA at different coordinates (lines 30-44, 79-92,
130-145, 181-196, 231-245, 261...). Our prologue rework (140/150/180/185/190) moves
the party through plot 50 → 55 on a compressed timeline, so a stale-plot staging
block plausibly fires, creates the cast, and a later block or an override script
destroys them again in view of the player.
Our own celebration guests (`csrnobm`/`csrnobf`/`csrffgd`, comp180) DO self-destroy —
`baf/csrnobx.baf`: `!Global("BD_PLOT","GLOBAL",50) -> DestroySelf()` — but that should
fire before the player ever sees them (they only exist during the plot-50 evening).

**To pin down (agent task):** which exact creatures the player sees; whether it is
(a) our comp180 guests despawning in view, (b) a vanilla BD0102 staging block firing
at a plot value our rework no longer intends, or (c) Entar/Skie remnants racing
comp185/190's removal. Then suppress at the SOURCE (never create) rather than letting
them spawn and pop.

---

## PT-3 — Safana/Coran tavern cutscene fires with Safana already in the party — **OPEN (CONFIRMED BUG, shipped comp110)**

**User:** "In my real playthrough the Safana/Coran cutscene in the city in the tavern
triggered, even though I had Safana in my party, and I had to dismiss Safana and get
her in the party again, even though I had her in the party from BG1. That should not
happen."

**Root cause — CONFIRMED (`research/data/sod_baf/BD0110.baf`, Elfsong Tavern):**
`BD_SPAWN_SAFANA("BD0110")` is a THREE-state machine, not a boolean:
- `0` → spawn/revive Safana into the tavern (blocks at BD0110.baf:1-23 and :26-34)
- `1` → **"Safana is in the tavern, breakup scene PENDING"** — block at BD0110.baf:53-74
  fires on `Global("BD_SPAWN_SAFANA","BD0110",1) + CombatCounter(0)`: it puppeteers
  `ActionOverride("SAFANA", MoveToPointNoInterrupt(...))`, faces her off against
  BDCORAN, and ends with `StartDialogNoSet("BDCORAN")`, then sets the var to 2.
- `2` → scene resolved, nothing further fires.

Our skip block `baf/skip0110.baf` writes **1**:
```
IF Global("BD_SPAWN_SAFANA","BD0110",0) InPartyAllowDead("safana")
THEN SetGlobal("BD_SPAWN_SAFANA","BD0110",1) Continue()
```
It correctly suppresses the two spawn blocks (both gated `== 0`) — but 1 is exactly
the value that **ARMS the Coran breakup cutscene**, with the party's own Safana as its
puppet. We didn't fail to suppress the scene; we scheduled it.

**Fix:** write **2** (scene already resolved) instead of 1 — one character in
`chriz-sod-remix/baf/skip0110.baf`.

**⚠ SAME BUG CLASS — audit ALL 9 skip blocks (comp110).** Every one pre-sets a vanilla
spawn-guard to `1`. Wherever a LATER block in that area fires on value `1`, we arm a
scene instead of skipping it. Must check each area script for blocks gated on the
value we write:
`skip0101` (Viconia/BD0101) · `skip0108` (Minsc+Dynaheir/BD0108) · **`skip0110`
(Safana/BD0110 — BROKEN)** · `skip0111` (Rasaad/BD0111) · `skip1000` (Edwin+Baeloth/
BD1000) · `skip2000` (Khalid+Dorn/BD2000) · `skip2100` (Neera/BD2100) · `skip7000`
(Rasaad/BD7000) · `skip7100` (Jaheira/BD7100).

**Save impact:** the user's live save already ran the scene. The fix prevents it going
forward; the already-consumed beat needs no repair beyond what he did (dismiss/
re-recruit), since the var is now 2 = resolved.
