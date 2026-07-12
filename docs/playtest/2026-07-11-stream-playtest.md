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

### PT-3b — generalization (user, 2026-07-11): NO kept companion may trigger their city scene

User: "we also have to make sure Rasaad, Garrick, Coran, Dyna, Minsc (anyone else?) do
not trigger their scenes/conversations in the city, if you already have them in the
party." This is broader than the skip blocks, because **comp110 keeps ALL 28 BG1
companions in the party** (removes the palace strip) — so any SoD scene that assumes a
companion is NOT in the party can now misfire. Two mechanisms:

- **(A) SoD-joinable recruitment sites — the 9 skip blocks.** Safana proved the guard
  value can arm the recruit/breakup scene. Covers Viconia, Minsc, Dynaheir, Safana,
  Rasaad, Edwin, Baeloth, Khalid, Dorn, Neera, Jaheira.
- **(B) BG1-cameo scenes co-starring a kept companion.** e.g. the BD0110 tavern scene
  is Safana **and Coran** (BDCORAN) — Coran is not a SoD recruit, he's the co-star, so
  fixing (A) for Safana fixes his appearance too.

Named-NPC → site map (verified from the .baf corpus, 2026-07-11):
| NPC | Site(s) | Mechanism | Note |
|---|---|---|---|
| Safana | BD0110 `safana7` | A (skip0110) | **CONFIRMED broken** — writes 1 = arms scene |
| Coran | BD0110 (BDCORAN, with Safana) | B | co-star of the Safana scene; fixed by the Safana fix |
| Rasaad | BD0111 `rasaad7`:43 + BD7000 | A (skip0111, skip7000) | two sites |
| Minsc | BD0108 `MINSC7_`:66 (+ appears BD0101:238) | A (skip0108) | check the BD0101 appearance too |
| Dynaheir | BD0108 (with Minsc) | A (skip0108) | shares the Minsc site |
| **Garrick** | **none found** | — | BG1-only, no recruitment site in the corpus — **verify he has ANY SoD scene**; if a party-banter cameo exists, confirm it tolerates in-party |

"anyone else?" — the audit must sweep the full kept-companion list, not just the named
five. Priority order: the 9 skip-block sites first (A), then a grep for any other
`StartDialog*`/`StartCutScene*` in a city area gated on a kept companion without an
`InParty`/`BeenInParty` guard (B).

**Save impact:** the user's live save already ran the scene. The fix prevents it going
forward; the already-consumed beat needs no repair beyond what he did (dismiss/
re-recruit), since the var is now 2 = resolved.

---

## PT-4 — Skie still runs her full vanilla palace plot ("talking to Daddy") — **OPEN (Skie pass not built)**

**User:** "Skie is still there talking about me talking to her daddy and everything. I
thought we wanted to skip all that and just have her there joinable? Maybe talk about
her father's dead for a moment and keep it short for now." + (side note) "She will
have inherited all her father's stuff. But we can plan more for that later (nothing
special or huge impact)."

Screenshot: palace Skie, *"I heard you talking to Daddy and the other dukes about
Caelar. Are you going to Dragonspear?"* → 3 vanilla replies.

**Not a regression — nothing built yet.** The Skie recruitment rework is **researched
only** (`docs/research/15-skie-recruitment.md`); no component ships it. So palace Skie
is 100% vanilla. Two problems visible at once:
1. The intended "strip her SoD plot, make her a plain talk-to-join recruit" (wishlist,
   locked 2026-07-10) simply isn't implemented.
2. Now that comp185 killed Entar, her "talking to Daddy" line is an active **lore
   contradiction** — she references a living father who is dead in our timeline.

**Surface (research/15, verified):** palace Skie = `BDSKIE.dlg` **state 8** (first
meeting), opened by `BDCUT04A.baf:12 StartDialogNoSet(Player1)`; ×5 council spawn
variants `BD0102.baf:33,82,133,184,235`; she leaves via `BDSKIE.baf:63-79`
(`EscapeBD0102`→`DestroySelf`). The **only two `JoinParty()` calls** in the whole
file are **state 6** (first recruit) and **state 2** (re-recruit), gated to camp
areas BD0120/BD0130. Her BG1 soundset is already on `BDSKIE.CRE`. comp190 already
killed the night-visit subtree (states 16-32); comp185 removed Entar.

**Minimal-viable shape (user: "keep it short for now"):** re-point the palace
first-meeting away from the vanilla council plot to a SHORT exchange — one or two
lines acknowledging Entar's death — ending in the talk-to-join handshake (route to
the state-6 `JoinParty()` path, or a trimmed equivalent that works in the palace, not
just camp). Suppress the rest of her SoD plot surface (Bence intro 33-36,
`bd_skie_plot` subquest 37-62, BD4000 static actor) per the locked scope. New dialogue
lines will be presented for word-level sign-off (BG1/BG2 register).

**Deferred side note (log only):** Skie inherits Entar's estate/possessions — flavor,
possibly a gear grant on recruit. "Plan more for that later, nothing huge." Do NOT
scope into the minimal pass.

**Dependency flag for parallel work:** PT-2 (despawning hall NPCs) and PT-4 both touch
the BD0102 palace staging and possibly Skie's spawn/despawn — coordinate or serialize
these two; they are the likeliest worktree collision.
