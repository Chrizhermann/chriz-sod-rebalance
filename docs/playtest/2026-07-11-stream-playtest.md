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

## PT-2 — NPCs spawn then despawn on the first trip down from the bedroom — **ROOT CAUSE CONFIRMED + SHIPPED (comp187)**

**User:** "When going down one floor from the bedroom for the first time in SoD, why
do we see some people, that despawn? Why are they spawned in the first place? I would
prefer they not spawn at all."

Bedroom = BD0103 (palace guest room). One floor down = BD0102 (great hall).
**Correction (2026-07-13): the sighting is BD0100, the upper hall the descent route
passes through** (BD0103 → BD0100 → BD0102) — the original BD0102 mapping was an
inference, and BD0102's staging turned out to be a red herring.

**Root cause — CONFIRMED (issue #3, 2026-07-13):** `bd0100.are` pre-places the
assassination-night fight set — Corwin (BDSCHAEL), Assassin1-3 (BDGASS5, EA=255
hostile), FF Guard 1/2 (BDFISTCC) and three BDFFDEAD corpses — with always-on
appearance schedules (dev ARE parse: 9 actors, 0xFFFFFFFF/0x00FFFFFF; they are the
area's ONLY placed actors). comp150 cut the assassination night and sweeps all nine
via `baf/csrswp.baf` (bddest ×9) on the area's FIRST script pass — but the engine
renders placed actors BEFORE the first script pass runs (the same verified behavior
that forces `blk0120.baf`'s first-action fade, cf. PT-1), so the set is visible for
a beat and pops in view. `CSR_SWEEP` is once-flagged → happens exactly once, on the
first descent — matching "for the first time" exactly. BDDEST.SPL itself is clean
(opcode 20 invisibility + opcode 168 remove-creature, both instant — SPL-verified);
only the pre-script render window shows them.

The issue's three candidates all cleared: (a) comp180 celebration guests self-despawn
overnight — BD0100/BD0102/BD0103 are all MASTAREA.2DA master areas, so their creature
scripts keep running while the party sleeps upstairs (and no second-descent pop was
ever reported); (b) the five BD0102 council variants are correctly re-gated to
`BD_plot==51` by comp150 (installed-bcs verified); (c) comp185 unspawns Entar and the
plot-55 Skie/Corwin housekeeping is comp197-guarded — neither races anything on the
first descent.

**✅ SHIPPED (2026-07-13, comp187, installed + verified on dev):** "the assassination
night-set never spawns" — zeroes the nine actors' appearance schedules in bd0100.are
(the engine-verified comp197/bd4000 pattern; +0x40 = 0 → present at no hour), matched
by actor name + CRE resref, count-guarded 9-or-FAIL. Suppressed at the SOURCE: they
never exist, nothing renders, nothing pops. `csrswp` stays untouched as belt-and-braces
(saves with a baked bd0100 still get swept; its no-Continue still eats the OnCreation
"To arms!" rally pass). Requires comp150 (without it the set is a live scene).
Downstream verified inert: `Dead("Assassin1-3")` is false for never-created creatures —
the same value the bddest sweep produced — so `BD_HELPED_KILL_ASSASSINS` stays at
csrarr's pre-set 1, and vanilla's >51 cleanup bddest lines no-op harmlessly.

**User-save note (live):** the pop is a one-time visual and already happened on the
stream save (bd0100 is baked with CSR_SWEEP=1 there); nothing to repair. Fresh games
load the patched ARE and never show the set.

---

## PT-3 — Safana/Coran tavern cutscene fires with Safana already in the party — **FIXED 2026-07-12 (source in v0.6.0, issue #1)**

**Fix applied 2026-07-12:** `skip0110.baf` now writes **2** (BD0110's vanilla terminal
value) instead of 1. The source fix shipped with the v0.6.0 pass; the dev install got
it recompiled via the v0.6.1 re-stack (verified: first block of the installed
`BD0110.bcs` writes 2). The LIVE install was fixed the same day via a direct override
byte-patch of `BD0110.bcs` (single byte `1`→`2` at offset 265, inside our EXTEND_TOP
block only; the two vanilla spawn blocks that legitimately write 1 are untouched;
byte-verified; pre-fix backup in `<game>/chriz-sod-remix-hotfix-backups/`). Inert for
the user's current save (the scene already fired there and set the global to 2
itself), correct for all future visits.

**Skip-block family audit (the ⚠ below) — COMPLETE, only skip0110 was affected.**
Verified two ways: (1) all `Global(...)` trigger conditions on the 12 spawn-guard
globals across the 9 vanilla area scripts — every script except BD0110 tests its
guard exclusively at `==0`, so `1` IS the vanilla terminal value there and the other
8 skip blocks are correct as shipped; (2) a full sweep of the dev install's override
(all 417 mods' `.bcs` + 4500 `.dlg`, using the compiled concatenated form
`<AREA><NAME>` for BCS and the source form `"<NAME>","<AREA>"` for DLG) — none of the
12 globals is referenced anywhere outside its own area script, so no dialogue reacts
to the values we write. BD0110 is unique in the whole family in having a `==1`-gated
block.

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

---

## PT-5 — Coast Way Crossing magic wall still appears — **ROOT CAUSE CONFIRMED: CUTSKIP mirror**

**User:** "The magical wall in the top right of the Coast Way Crossing was still there
when I tested, did we already remove it?"

**Yes we removed it — from the wrong number of places.** Verified chain (2026-07-11):
- comp200.2's patch IS live: `bdcut14.bcs` on BOTH installs no longer contains
  `bdwforce`/`force_wall` (string-verified). The `Force_Wall_Door` ARE default is
  OPEN (flags 0x201) and the `Force_wall` animation (BDFORCEW @3585,1160) defaults
  HIDDEN (flags 0x1002) — so the normally-played cutscene shows no wall.
- **BUT `CUTSKIP.bcs` — SoD's cutscene-SKIP rig — carries a mirrored end-state for
  the bridge scene** (verified in the compiled file: a block with `bdcrus12/13/14`,
  `minhp1`, `force_wall`, `force_wall_door`) and the file also references
  `bd1000/bd_caelar_timer`. **Skipping the cutscene replays the vanilla end-state:
  wall shown, door closed — and likely the 3-round parley timer instead of our
  FIVE_ROUNDS.** (A second force_wall pair sits next to `bdcaelar`/`bdbence` = the
  parley-end mirror that hides/opens again — benign.)
- Note: CUTSKIP was NOT in our decompiled corpus (`research/data/sod_baf/` has no
  CUTSKIP.baf) — corpus gap, which is why the mirror was missed.

**Fix:** comp200 must patch the mirrored CUTSKIP block the same way (remove the wall
actions; THREE→FIVE_ROUNDS if present), count-guarded.

**✅ SHIPPED (2026-07-12, comp245 v0.6.0, verified on dev):** new component (not a
comp200 edit — avoids mid-stack churn) removes the mirror's wall
(`AmbientActivate("force_wall",TRUE)` + `CloseDoor("force_wall_door")`; the mirror
carries NO bdwforce cast and NO VFX — structurally different from BDCUT14, caught by
the count-guards on the first attempt) and bumps the mirror's parley timer to
FIVE_ROUNDS (it DID set the vanilla THREE_ROUNDS — the suspicion above confirmed).
The wall-down restore pair stays as harmless no-ops.

**✅ SYSTEMIC AUDIT COMPLETE (2026-07-13, from CUTSKIP.baf source — now in the
corpus):** the rig is one big `Switch("BD_CUTSCENE_BREAKABLE","GLOBAL")` whose
RESPONSE #N mirrors the cutscene that set BREAKABLE=N. Findings: BDCUT10 and
BDCUT28 (comp120's hooded-man scenes) NEVER set BD_CUTSCENE_BREAKABLE → not
skippable → no mirror, no bypass; the only BDIRENI reference in the rig is a
`DestroySelf()` cleanup (no-op when he doesn't exist). BDCUT14 → mirror #14
(fixed, comp245); BDCUT45A/B → mirrors #61/#62 (fixed, comp280). Our own custom
cutscenes never opt into breakability → unskippable by construction. **Zero
remaining CUTSKIP exposures.** House rule stands for FUTURE cutscene edits: check
whether the scene sets BD_CUTSCENE_BREAKABLE, and if so patch its mirror response.

**⚠ SYSTEMIC: audit CUTSKIP mirrors for EVERY cutscene we patch.** Confirmed pattern:
any component that edits a BDCUT* scene can be bypassed by the skip rig. Check at
minimum: comp120 (BDCUT10 hooded-man launch, BDCUT28 ending) and every future
cutscene edit. Add "check CUTSKIP" to the house checklist.

**User-save repair (live):** if the wall is still up on the save, console:
`C:Eval('OpenDoor("force_wall_door")')` and `C:Eval('AmbientActivate("force_wall",FALSE)')`
(door + animation state persist in the baked area). Confirm with the user whether he
skipped the bridge cutscene (validates the diagnosis).

---

## PT-6 — Dig site: missing "essence" vial + the scrying-pool visions — **CONFIRMED comp220 regression + content pass**

**User:** "There seems to be one vial missing in the dwarven dungeon 2nd level.
Something 'essence', with which you can have a vision in the pool there (which is
crazy stupid, why is this here). All those visions need to be rewritten, I am pretty
sure they have Imoen learning magic, which needs to go or be replaced, a vision of
Caelar, which needs to be rewritten at some point I think, and a vision of the Hooded
Man/Irenicus, I believe."

**Mechanics (verified, `BDODSCRY.baf` = the pool object, BD1200 @~1325,2095):**
3× Silver Scepter `BDMISC55` slot into the pedestal (3rd gives +3,000 party XP) →
pool activates; `BDMISC59` **Essence of Clarity** clears the cloudy pool
(`BD_SDDD12_CLOUDY` 1→0) → visions. Vision cutscenes: `BDSCRY01` (VFX bed),
**`BDSCRY02` = the Imoen vision** (IMOEN2 + bdliia casting practice — exactly what
the user remembers), `BDSCRY03` (+ the Caelar / hooded-man visions in the chain —
launcher tail still to trace).

**The missing vial — comp220 regression CONFIRMED:** `BDMISC59` has exactly two
world sources: the `Shelf` container @(1146,1230) in BD1200 (intact — containers
untouched) and **`BDWIGHDD`, which is in comp220's cut list** (droppable copy).
Sources went 2→1. Scepters are safe (3 containers, all intact).

**Fix options (user to pick):** (a) re-home the wight's vial into an existing
container near its coords; (b) restore that single BDWIGHDD (one schedule flip);
(c) fold into the vision-content pass below and decide there.

**Vision-content pass (new scope, user-directed):**
- Imoen-learning-magic vision: "needs to go or be replaced." Nuance to flag: with
  comp160 (Imoen stays in BG studying), the vision is arguably MORE canon than in
  vanilla — user still wants it gone/replaced; his call on the replacement.
- Caelar vision: rewrite "at some point" — park with the item-13 arc treatment.
- Hooded-man/Irenicus vision: must GO — **verify whether comp120's five-appearance
  removal already covers the pool vision** (its known sites: BD0103, BDCUT10/11,
  BDCUT28 — the pool vision may or may not be among the five).
- User verdict on the whole gimmick: "crazy stupid, why is this here" — a full-cut
  of the pool sequence (scepters/essence/visions) is on the table as the simple
  option; NOT decided.

**Save impact:** the user's live save already ran the scene. The fix prevents it going
forward; the already-consumed beat needs no repair beyond what he did (dismiss/
re-recruit), since the var is now 2 = resolved.

---

## PT-4 — Skie still runs her full vanilla palace plot ("talking to Daddy") — **FIXED (comp197 merged, PR #8; lines signed off 2026-07-13; in-game verify next playtest)**

> **Build note (2026-07-12, issue #2, branch `fix/issue-2-skie-minimal-join`):**
> shipped as **component 197** — new short palace exchange (Entar's death → talk-to-
> join), Beamdog's cut-content `JoinParty()` machinery resurrected, full SoD plot
> surface retired (Boareskyr banter Skie-free with the bridge wrap preserved, BD3000
> missing-Skie quest gated, BD4000 placed actor unscheduled), in-party guards on every
> script targeting `"bdskie"`. Design record: `docs/design/chapters/01-prologue.md`
> §12 (incl. the in-game verify checklist + a console re-arm for the current live
> save). The 11 new lines await sign-off: `chriz-sod-remix/languages/english/
> csr197skie.tra`.

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
