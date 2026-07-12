# Chapter Pass — Prologue (Korlasz dungeon + Baldur's Gate city opening)

**Status: IMPLEMENTED as components 140-180 + 145 (v0.2.x), installed on the dev EET
copy, file-level verification green. THREE IMPORT PLAYTESTS DONE (2026-07-06/07):**
playtest 1-2 soft-locks fixed (bdcut00z ender + one-shot exit launch), playtest 3
"looked pretty good" — fixes locked from it: no auto-granted party on fresh/import
(comp 145, §10), Imoen join ungated, Korlasz opener rewritten, undead filler cut +
Insane defensive layer (§2a scaling), crew repositioned, Vhast human + full plate,
Sillune Short Sword +1, sequencer targets nearest PC (§2a). **Continuous BG1→SoD path
(SOD_fromimport=1) not yet playtested.** All design decisions below are user-locked
through sparring rounds 1-4 (2026-07-05/06) + playtest lock-ins (2026-07-06/07).
Research basis: `docs/research/10a-11b`.
Implementation deviations approved during build: (a) comp 140 exits via an
EXTEND_BOTTOM block on bd0120.bcs (bd_plot=50 → bdcut00z) instead of a direct cutscene
chain — required so EET fresh-start Bhaalspawn-ability grants still fire; (b) comp 150
gates three transitions beyond the 11b list (BDBELT 40 t2, BDRASAAD 28.0/32.1/36.0,
BDDYNAHE 23 t1) to avoid dialog dead-ends — pending user sign-off; (c) sequencer =
Slow + Confusion (SPWI401, not the spec's typo SPWI410) + Glitterdust.

---

## 1. Remove the Korlasz dungeon — DECIDED (signed off 2026-07-05)

**Spine = Beamdog's own debug skip** (`BDDEBUG.baf:151-160`): `bd_plot=50`,
`bd_npc_camp_chapter=1`, `StartCutSceneEx("bdcut00z",FALSE)`. Implemented as an
**instant exit**: party lands invisibly in BD0120 for 2-3 script passes (all bootstrap
runs untouched — Bhaalspawn abilities, Key Ring, gold, Imoen import handling, BDINTRO
companion wiring blocks 1-539 incl. mod hooks), then we patch only BDINTRO's staging +
walk-in blocks (541-688) to set `chapter=7`, `DREAM=7`, `bd_plot=50`, sprite flags and
launch `bdcut00z`. One implementation for EET import AND fresh start. `bdcut00z` is never
reimplemented (it owns the gold impound + `BD_SAFEHOUSE_DONE` + the BD0103 move).
**Never touch `SODSTRTA.2DA`.**

Default outcome state: `BD_KORLASZ_SURRENDER=1` + journal chain (256379 → 259573 →
269028). Fiction (one Liia/Fist line + the DPALACE text): *the Fist cleared the tomb;
Korlasz surrendered and sits in the palace cells.* Canon-consistent — BD0116 spawns her
in the basement cell whenever she isn't dead; her own line says she was taken to the
palace, not the jail.

## 2. The Korlasz jailbreak — DECIDED as the build-v1 core fight

Location: **BD0116 palace basement** (treasury + wine cellar + jail cells), on the
vanilla rematch scaffolding (TrapBDKorlasz region → `BD_KORLAS_FREED` → she breaks out,
kills a guard, forced dialog → hostile; journals 261626/261627). We re-time the trigger
onto our quest beat and replace the lone under-equipped mage with a designed party.

**Decided elements (user, 2026-07-05):**
- **Mini-quest hint:** a small journal quest pointing at her — during/after the
  celebration someone (Liia or a Fist officer) mentions Korlasz is held below and asks
  the hero to look in / give a statement. Journal opens ("visit Korlasz in the palace
  cells"), closes on her death.
- **Prepare-for-a-fight foreshadowing, nothing crazy** — assets verified (research 11a §5):
  a stairs-top beat in BD0102 plays SoD's own off-screen-fight faker (the repeating
  `sorcr05/poisn05/fchil05` sound trio Beamdog uses in BD0109/0111/0121) + the `HIT_03B`
  door-banging cue, spawns a dying Fist guard clone (SEQ_DIE, one line — Beamdog's own
  jailbreak already stages exactly this with BDFIST1A/1B), sets `BD_KORLAS_FREED=1` and
  opens journal 261626 ("…Korlasz is loose in the Ducal Palace…" — fits verbatim).
  The breakout itself stays player-paced in BD0116; the forced cell-dialog funnel
  (BDCUTKOR → states 24-27) must stay intact — it sets `BD_SPAWN_KORLASZ=2`, without
  which the quest-done journal never fires.
- **NO surrender/parley** in this fight — a real fight to the death. (Her vanilla
  rematch line is already "I'll not be imprisoned again!"; `BD_SPAWN_KORLASZ=2` + journal
  261627 on kill keep downstream state coherent. The 71%-HP parley is not carried over.)
- **Proper prebuffs:** with SCS — caster brains prebuff natively (dw#mg13's set is
  verified ⊆ her spellbook), gated `FILE_EXISTS_IN_GAME`; without SCS — scripted
  force-buff openers per caster (the vanilla rematch pattern: Stoneskin/MGoI/Mirror
  Image), so the fight is prebuffed on every install.
- **Named, smaller, more interesting party** — template CONFIRMED (user, 2026-07-06):
  the **Undercity party before the Temple of Bhaal** (Rahvin/Haseo/Wudei/Gorf/Shaldrissa/
  Carston — named members, one distinct role each, SCS slot pattern per research 10d).
- **Scaling required** (user): v0.1 scales composition via explicit `Difficulty()`
  branches (the engine's only native mechanism for placed fights — the slider itself only
  doubles enemy damage on Insane). Party-level-reactive top-ups: roadmap.
- Fight is the **pilot for the wishlist item "SCS-style scripting on important fights"** —
  patterns land in the methods cookbook (#13).

### 2a. Roster DRAFT v1 — for person-by-person discussion (names are placeholders)

Fiction that carries the loot: the Fist stored the **confiscated tomb assets in the
palace treasury** (same room as your impounded gold); her crew **raided it mid-breakout**
— everything worth keeping from the dungeon is on their bodies when you win.

Roster locked person-by-person (user, 2026-07-06); Korlasz's exact level still open:

| # | who | chassis (verified) | build (LOCKED) | role | carries (= the re-homed loot) |
|---|-----|--------------------|------------|------|-------------------------------|
| 1 | **Korlasz** | BDSHKORL/bdkorlas, Mage 8, HP 32 | **Mage 12 (LOCKED** 2026-07-06 — Semaj parity; "more exciting than round 1, below Sarevok-tier"**)** | boss caster; **prebuffs "like a Semaj" — SCS-only** (matching dw#mg brain; no scripted prebuff fallback without SCS, per user); Confusion/Slow/Dire Charm rotation + restored consumables (Minor Globe + Prot. Elemental scrolls, Vocalize, Potion of Clarity — revives 4 dead vanilla AI blocks); **signature sequencer, see below** | family papers (Sarevok's Notes*, Bhaal Research, her journal + orders), Knave's Robe, Cloak of Protection +1, Bracers AC6, Staff +1 |
| 2 | **"Mother Hasska"** — cleric of Bhaal, organized the break-out | BDKORME9, C6, plate/shield | Cleric 9 | frontline anchor; heals/buffs Korlasz; smites; **cleric prebuffs like Wudei** (the Temple-of-Bhaal cleric, dw#pr brain) with SCS | **Helm of Unwavering Purpose**, plate, morningstar, **Wand of the Heavens** (she uses it), **treasury key BDKEY10** (raid fiction — verify Ophyllis-subplot interaction at implementation) |
| 3 | **"Vhast"** | BDKORME8, F5 (chassis is a halfling → rebuilt **human**, user 2026-07-07) | **plain Fighter 10, human** | bruiser; **chugs an oil of speed at fight start** (SCS potion blocks when present — standard SCS behavior; scripted UseItem fallback otherwise) | **Sword of Ruin +2** (2-hander, wielded); **full plate + helmet, both UNDROPPABLE** (plat04/helm01, user 2026-07-07); on Insane also a **Potion of Superior Healing** (droppable if unused) |
| 4 | **"Sillune"** | BDSHIS07, T5 | **plain Thief 9** | backstab + restealth; **3 invisibility potions** arm the restealth cycle; wields a **Short Sword +1, UNDROPPABLE** (sw1h08, user 2026-07-07 — "magical shortsword") | **gem bag**, the gems + ~4,100 gp tomb cash ("grabbed the valuables for the escape") |
| 5 | **Porios** — the tomb sentry, captured too (existing named NPC) | BDPORIOS, M5 | **Mage 8; NO flee behavior — fights to the end** (user cut the coward beat) | support caster (Mirror Image/Haste/MM) | his **Cloak of Minor Arcana** (unique) |
| 6 | **"Grit"** — Korlasz's dust-mephit familiar | BDSHKFAM | as-is | harassment, Glitterdust | — |

*BDSHSARE's flag (`BD_SAREVOK_SECRET`, feeds the chapter-10 masks quest) is re-homed onto
item acquisition (PartyHasItem watcher), not the old BD0130 container.
**Wand of Fire: DROPPED entirely** (not carried, not loot). **Journal 266701 (assassin
text): swapped for a new crusade-only .tra line.**

**Scaling (LOCKED 2026-07-07, playtest 3):** EASY/EASIEST = 1,2,3,5 · NORMAL and up =
all six. **Undead filler CUT** (user: undead don't fit a palace jailbreak — no added
bodies at any difficulty). Insane (HARDEST) instead adds a **defensive layer on the
anchors**: Protection from Magical Weapons on Korlasz, Stoneskin on Porios, Luck + a
Potion of Superior Healing on Vhast. Spell resrefs are resolved **by name at install**
(Spell Revisions shifts the slots — PfMW=spwi611 / Luck=spwi209 / Stoneskin=spwi408 on
this install vs vanilla spwi610/212/415) and injected via EVALUATE_BUFFER, so the layer
is correct on vanilla, SR, and SCS alike. Crew spawn positions sit SOUTH of the cell in
the open room (playtest 3: the draft Y≈300 spots jammed them into the cell, off-screen).
Non-casters get SCS generic brains + potions when SCS present; SoD-native stack
otherwise (cookbook #13).

### Korlasz's sequencer (verified SCS mechanics, 2026-07-06)

How SCS does it (verified by decompiling Semaj's and Shaldrissa's brains on this
install): sequencers are **fixed at install time** — the SSL loadout generator grants the
mage a marker spell (`dw#msN`) and emits a `HaveSpellRES("dw#msN")`-gated block in the
generated brain that fires the paired combined-SPL `dw#msNB` at the target (plus cosmetic
force-casts of the components). Not runtime-random, not per-playthrough. And the contents
are modest at this tier: **Semaj (M12) gets a Minor Sequencer = 2× Color Spray;
Shaldrissa (M13) gets 2× Larloch's Minor Drain.** So SCS will NOT hand Korlasz anything
juicy on its own — a hand-picked **full Spell Sequencer (3× ≤L4)** instantly puts her
above her reference class without breaking tier.

**Design (Option B, recommended):** roll our own the SCS way — marker SPL + combined-SPL
pair + one HaveSpellRES-gated block mirroring the dw#mg437 pattern, layered on her
override slot. Fires once at combat start after prebuffs; works both with SCS (on top of
the assigned dw#mg brain — we simply don't grant any dw#ms token, so no double-fire) and
without. Content candidates (all within her verified book, standard resrefs → SR-safe by
composition):
1. **Control bomb (rec):** Slow + Confusion + Glitterdust — her vanilla AI identity,
   fight-defining opener, save-counterable.
2. Alpha strike: 3× Flame Arrow on the squishiest target.
3. Mixed: Slow + 2× Flame Arrow.

**DECIDED (2026-07-06): option 1, the control bomb** — built as csrseq1/csrseq1b.
**Targeting fix (2026-07-07, playtest 3):** the opener fires at the **nearest PC**
(`See([PC])`/`LastSeenBy`), never nearest-enemy — the vanilla cell guards (bdfist1b,
GOODCUTOFF) usually stand closest when she turns, and nearest-enemy targeting wasted
the one-shot bomb on a guard. If no PC is visible the marker waits; the brain fights on.

**Per-playthrough randomization: DEFERRED** (user, 2026-07-06 — other mods do
per-playthrough rolls, too much to plan now). Roadmap note: cheap later via a runtime
roll among 2-3 sequencer variants at first combat.

## 3. Item re-homing — DECIDED

Item list per research 10a approved; **delivery = carried by the jailbreak party** (see
roster). No evidence chest. Cut with the dungeon (decided): Ammon's Cobalt-Moss quest,
Restless Spirit quest, torch/brazier puzzle, Sarevok-sword rumor flavor. The
`BD_TAKEN_GOLD` impound → BD4100 return chain stays untouched.

## 4. Palace night: assassination CUT ENTIRELY — DECIDED

The Imoen wake-up, the bdgass assassination, the poisoning, the bedside morning: all
removed. v0.1 explicitly tolerates imperfect story logic; **the war council happens
because there is an unsanctioned crusade** — that alone carries the night.

**Mechanics verified (research 11a/11b). The cut is a "strangle-by-flag": nearly every
assassination block has its own once-flag, so a single new arrival block pre-sets them all
— only three scripts need real surgery.**

- **Arrival block (BD0103, once):** activate the suite exits (`TranBD0100a/b` ship
  deactivated — only the cut Liia scene opened them in vanilla), park `bd_001_plot=10`,
  pre-set `BD_INTRO_IMOEN_CUT=1` (the BDCUT02 launcher has NO plot gate — first stroll
  through the living room would fire the assassination), `bd_imoen_bed=1` (dead-Imoen
  dressing), **`BD_MDD007=2`** (kills the bedside-morning block AND pre-arms the Skie
  scene — zero trigger edits needed there), `BD_ORIGINAL_ASSASSIN_INTRO=1` (hall assassin
  wave), `BD_HELPED_KILL_ASSASSINS=1` (selects the Liia-first council variants); move the
  Treasury Note + journal 267494 here (the only pointer to the impounded gold — and the
  basement errand it creates walks the player toward the jailbreak).
- **BD0100 sweep (once, <52):** despawn the ARE-placed night set (3 hostile assassins,
  Corwin, 2 guards, 3 corpses sit there whenever bd_plot<52 — vanilla just never lets
  you in early). Vanilla's own >51 cleanup then dresses the hall normally.
  **PT-2 amendment (comp187, 2026-07-13):** the sweep alone is not render-proof — the
  engine draws placed actors BEFORE the first script pass runs (the same behavior that
  forces blk0120's first-action fade), so the set visibly popped once, on the first
  descent from the bedroom (issue #3). comp187 zeroes the nine actors' appearance
  schedules in bd0100.are (the comp197/bd4000 pattern) so they never exist; the sweep
  stays as belt-and-braces for saves with a baked bd0100 and to keep eating the
  OnCreation rally pass.
- **Night block:** AND-gate the `TextScreen("DPALACE")` block behind a new
  `C#SODR_BEDTIME` global (set by a "retire for the night" choice); keep TextScreen /
  `bd_plot=51` / 14-day advance / beds; replace only the Imoen-wake tail with the
  **wake-for-council beat: a BDSERV clone with a NEW dialog resref** (verified: vanilla
  never spawns BDSERV anywhere; do NOT attach its vanilla dlg — its plot-54 state would
  bypass the Skie scene). Staging template = the existing Skie block (fade → DayNight →
  sleep → wake → dialog). Also reset `BD_LEFT_THE_PALACE=0` so Corwin's post-council hub
  (companion locations + Ophyllis pointer) still plays.
- **Council:** the five BD0102 OnCreation variants each set `bd_plot=52` themselves and
  fire only at the two stairway landings (front door/basement never trigger them). Add
  `Global("BD_PLOT","GLOBAL",51)` to all five (else the council fires during the roam at
  50) and delete the `CreateCreature("BDGASS6")` — fun verified fact: the "captured
  assassin" is a CORPSE (state DEAD, no dialog); there was never an interrogation.
  **Crusade-only council with zero new text:** entry BDLIIA 9 → re-point 4 transitions
  (BDELTAN 4→BDBELT 35 — precedent BDENTAR 7 does exactly this; BDBELT 38→39; BDLIIA 11
  replies→BDELTAN 8; drop the one "assassins tried to kill me" reply) — refugee/trade
  reports, "every sword north", the pitch, Corwin assignment all remain; journal 266701's
  QUEST_DONE text mentions the assassins → swap or accept (v0.1: accept).
- After that, **vanilla runs untouched and verified end-to-end**: council → Corwin hub →
  roam at 52 → goodnight → plot 54 → Skie 3 a.m. (fires via the pre-armed MDD007) →
  55 → blessing → send-off plaza (57) → parade (60-63) → 65 → chapter 8.
- **Roam-at-50 is safe (verified):** Minsc/Dynaheir/Rasaad recruiters key on
  `Chapter=7`; Safana/Coran, Garrick, Sundries, FF-HQ (chapter<9), Ophyllis/doppelganger/
  Korlasz-cell are ungated. bd_plot≥51 only gates palace dressing/music cosmetics.
- **Reference cleanup policy (user):** cheap-now list = the city/prologue dialog lines in
  research 11b list (b) (Eltan/Liia/Belt small talk, Corwin escort lines, Garrick,
  Safana/Rasaad/Dynaheir recruit replies, Rohma scene) — remove in v0.1, they're single
  transition gates. Parked to later chapter passes = list (c): Caelar parley (ch8), Edwin
  recruit, Corwin romance, crusader lines, Darnas kidnap-for-blood reveal (ch12).
  Vanilla's actual premise, for the record: the "assassins" were Caelar's agents on a
  capture-alive mission for the hero's divine blood (Darnas reveal) — the blood-portal
  plot has zero mechanical dependency on the palace night; rewording those three later
  beats is text-only work for their passes. `bdgassa1.spl` is shared by Tiax/Dauston
  scenes — never delete the spell.
- **Rioters instead of assassins on the 2nd floor: SKIPPED (user, 2026-07-06).** The
  palace night stays quiet; crusade tension moves to street/crowd vignettes during the
  roam — roadmap item.
- Crusade premise note (user): SoD's premise is weak; the hero's personal stakes in the
  crusade get brainstormed later as a long-run fix. v0.1 = council pitch as-is minus
  assassination beats.

## 5. Imoen — DECIDED (detection deferred)

- **Was in party (EET import):** patch the BD0120 strip from DestroySelf to
  `LeaveParty()` + `MoveGlobal` of her **imported instance** into the BD0103 bedroom —
  she keeps her imported build/XP/gear; rejoins with one dialog line on waking. Safe
  because this pass deletes the poison-plot blocks that damage/destroy/duplicate her.
- **Not in party:** the pre-placed bedroom actor gets a short join dialog instead of the
  sickness plot; leveled to the SoD baseline (fresh floor 64,000 XP), BG1-tier gear;
  `Imoen_equipment` default stock stays as room supplies.
- **Unconditional presence** — no BG1-death detection (user: EET's back-from-the-dead
  Imoen was always weird anyway; skip/defer).
- Implementation notes (research 11a/11b): the placed bedroom actor keeps existing but
  `bd_001_plot=10` parks ALL her vanilla dialog states — her new join states key on our
  own global, so no vanilla state can hijack. If she is NOT taken along, later content
  already works ("she stayed with the Fist" is all it assumes — the poisoning is never
  required). **Parked for the ch12 pass:** the scrying vision (BDSCRY01 stages Imoen +
  Liia in BD0118) assumes she's in Baldur's Gate — needs an in-party gate when we get
  there. (Also corrects 10c: BD0118 is not unused; that vision is its one tenant.)

## 6. Celebration — DECIDED; REWRITTEN 2026-07-07 (playtest 3, user direction)

~~Short praise beat built from existing duke lines~~ — the reused BDLIIA council pitch
("We would have you join them") opened the scene with a dangling "them"; scrapped.
**Standing style rule locked here (applies to ALL remix writing): BG1/BG2 register over
SoD's — Liia speaks like her BG1 speeches, villains like Sarevok/Irenicus ("peak
writing"); dropping voice-overs to rewrite is always acceptable.** The v1 scene:

- **All-custom text, no VO, no crowd-cheer sound** (user cut it). Liia toasts the
  victory over Sarevok (BG1 duchess register), Belt seconds soldier-blunt, then Liia's
  closing keeps the two hooks: Korlasz statement (jailbreak opener journal) + Caelar's
  proclamation hand-over.
- **The hall is dressed:** 8 nobles + 2 Flaming Fist guards spawn for the evening
  (click-dialogs: nobles congratulate, guards mind the doors — BG1-style one-liners);
  all despawn when the night passes (vanilla dresses the palace with its own nobles
  from plot 52).
- **The palace is locked for the evening** (user: you shouldn't be able to just walk
  out): both front-door variants (TranBD0101/TranBD0010) deactivated at bd_plot=50,
  ARE-default state restored the next morning — read from the ARE at install time, so
  EET (BD0010 active) and standalone SoD (BD0101 active) both restore correctly.
  Basement + upper floors stay open; the whole quest surface is interior. Vanilla only
  touches these doors at plot 55→56, so days 51–55 are untouched.
- **Korlasz return beat (user 2026-07-07):** coming back up after the jailbreak, a
  fresh Liia meets the player — what happened below? — simple answers, she orders two
  Fist guards down to secure the cells (they march to the basement stairs), thanks the
  player a second time. Very short, ambient (no cutscene). **Playtest-4 fix:** she
  spawns on the news but only **walks up and talks on See(Player1)** (own brain,
  csrliiax) — the area-script dialog start had reached the player down in BD0116
  (BD0102's script keeps running; shared master area).
- **Imoen XP catch-up (playtest-4 fix):** vanilla gives every SoD joinable a
  per-companion XP-tier ladder (snap toward Player1's tier at join + after the
  safehouse flag; 250k/200k/161k/135k/110k/90k, `ChangeStat XP SET`) — **except
  Imoen** (BDIMOEN.baf has none; she leaves before it matters in vanilla). Component
  160 now compiles the verbatim ladder as `csrimoxp` and assigns it to both
  instances (csrimo override slot; imported IMOEN2's race slot via the strip patch).
  Join floor stays 64,000 (CRE 0x18 — the joinable-XP field, NOT 0x14 kill-XP).
- **Korlasz dialogue polished** (§2a funnel, states 24–27 now all custom): the
  "tortured in private... this horror" melodrama (nonsense mid-jailbreak — she stands
  free and armed) replaced; BG2 villain register; Minsc's interjection vocabulary
  ("punish/murder") and Safana's "That makes two of us." kept tracking.
- **Council next morning audited (2026-07-07): left vanilla.** With the celebration no
  longer burning BDLIIA state 11, the council chain reads coherently (trade disruption
  → forces dispatched → "not enough" → "we would have you join them" now has its
  antecedent → Belt backs you → cutscene). Voiced throughout except Liia 11/Eltan 8;
  rewrite only if the user calls specific lines.

No fireworks (no VFX asset in SoD; roadmap if ever). Roadmap: staged celebration scene,
crowd set-piece, street vignettes of crusade tension.

## 7. XP ledger entry (prologue) — VERIFIED + DECIDED + SHIPPED (component 175)

**Delivery rule (user, 2026-07-06):** any remix XP compensation is granted as ONE
collected `AddexperienceParty` award after Korlasz's defeat — never dripped as separate
grants at arrival. (v0.2.0 grants zero remix XP; the XP messages seen at arrival are
vanilla/EET catch-up systems — SoD's per-companion XP-floor snap — which stay as-is per
user.)

**Playtest 5 (2026-07-10, user):** "didn't really get much XP for killing Korlasz or
reporting to Liia." Confirmed: the jailbreak awards only creature kill-XP and no quest
award anywhere — the gap below.

Vanilla prologue XP removed by the dungeon skip — parsed 2026-07-10 from the dev
override (ARE actor tables + CRE 0x14; quest awards from decompiled dialogs).
Guaranteed content, Normal difficulty, per char at party of 6:

| Removed (vanilla) | Party total | Per char |
|---|---:|---:|
| Placed hostile garrison (BD0113 5,600 · BD0114 47,515 · BD0120 4,150 · BD0130 55,215) | 112,480 | 18,747 |
| Korlasz herself (kill path; surrendering paid ~167/char more — unit-corrected 2026-07-12) | 2,500 | 417 |
| Imoen exit wrap-up (`AddXPObject(Player1..6,5000)`, BDIMOEN.d:303-308) — the old "30k wrap-up" note = 30k *party*, i.e. 5k/char | 30,000 | 5,000 |
| Ammon Ossa moss turn-in (`AddexperienceParty(3000)`, BDAMMON.d:269) — Ammon + the moss live in BD0120; NOT re-homed, dead in the remix. **Unit-corrected 2026-07-12: AddexperienceParty divides → 3,000 party ≈ 500/char, not 3,000/char** | 3,000 | 500 |
| **Guaranteed total (kill path)** | **147,980** | **24,663** |

*(Unit note 2026-07-12 — user verified in-game that `AddexperienceParty` DIVIDES among
the party. The per-char total above was computed as party÷6 and therefore survives the
correction: 18,747 + 417 + 5,000 + 500 ≈ 24,663 ✓. The option-(c) 24,000/char reward
stays correctly sized; its DELIVERY was re-encoded the same day to
`AddXPObject(Player1..6,24000)` because the original single `AddexperienceParty(24000)`
paid only ~4,000/char.)*

Optional extras excluded from the headline: the Sarevok-chest skeleton trap (Normal
+6,050 party ≈ +1,008/char — the chest FLAG is re-homed to the jailbreak, its trap XP is
not) and Hard/Insane-only scripted spawns (+8,000 party spiders). Research-02a
correction: BD0130's "~28 scripted waves" do not exist — the only scripted spawn is that
single optional trap.

Remix currently grants: jailbreak kill-XP only — csrkorl 4,500 + crew 4,750 (+ Grit's
familiar chassis) ≈ 9,250–9,700 party ≈ **1,600/char** — and closes journal 261627 with
zero XP. **Gap ≈ 23,000/char.**

**DECIDED (user, 2026-07-10): option (c) — 24,000/char, delivered as Liia's quest
reward on the return beat** (the turn-in feel), not on the kill. Still ONE award per
the locked delivery rule.

**SHIPPED as component 175** (REQUIRE 170+180; declared after 180 in the tp2, since it
patches 180's dialog) and installed+verified on dev: csr175.d ALTER_TRANSes csrcele
state 2 ("korlret2" — Liia's closer, reached only while CSR_KORL_RET=1 and flipping it
to 2, so the award cannot repeat), inserting `AddexperienceParty(24000)` BEFORE the
`DestroySelf()` (actions queued after DestroySelf on the speaker are dropped by the
engine). comp175.tpa anchor-checks the dialog first, comp180-style (exactly 4 states;
state 2 SAY contains "see to what remains") and FAILs loud on mismatch.
Build note: WeiDU's `STATE_WHICH_SAYS` was tried first and is a GLR parse error in
this position on weidu 24600 — the binary anchor-check pattern is the house standard.

## 8. Compatibility notes
- Tail-mod patches on BD0120/BDINTRO/BD0103/BD0116 + new .d/.cre; no engine 2DAs; K#/mod
  blocks preserved verbatim. Component 120 already edited BD0103 — patterns must match
  patched text; install order 120 → prologue components.
- SCS detect-and-adapt with vanilla fallback throughout (cookbook #13).
- Ships as separate components: dungeon-skip · jailbreak fight · night/council rework ·
  Imoen · celebration (fight/celebration require the skip).

## 9. The hero's personal stake — Caelar's open challenge (user direction, 2026-07-06)

User idea, building on the verified vanilla premise (her agents wanted the Bhaalspawn
captured alive for the divine blood): instead of the cut covert kidnap attempt, **Caelar
challenges the Bhaalspawn openly** — a public proclamation that she is coming for the
hero of Baldur's Gate, no matter what. Why this works better than vanilla:
- Fixes the exact logic hole the user called out: nobody follows a shining crusader who
  sends assassins; an **open, honorable demand is on-brand** for a lawful-good aasimar.
- The chapter-12 blood reveal (Darnas) stays fully intact — she really does need the
  hero; only the *method* changes from covert to declared. Hephernaan's deception layer
  is untouched.
- Gives the MC stakes from minute one and sharpens the council pitch: the dukes send you
  north partly because *you* are the one she's demanding.

PROPOSED v0.1 delivery (cheap):
1. **Repurpose the Crusader Pamphlet items** (BDSHPAM1/2 — currently dying with the
   dungeon) as her posted proclamation with new text naming the Bhaalspawn; readable
   during the city roam.
2. **One new council line** (Belt/Eltan references the proclamation) — single .tra
   addition to the otherwise zero-new-text council.
3. Roadmap: street-crier vignette; chapter-8 parley rewording (she references her open
   challenge instead of "the poison my agents sought to use") — parked for that pass;
   feeds the Caelar arc-treatment doc.

**Public reason (user-confirmed direction, 2026-07-06):** yes — at the surface it's
simply *because Bhaalspawn*: her proclamation frames the child of Bhaal as necessary to
her holy campaign ("even the blood of the Lord of Murder can serve the light" framing) —
honest about the WHAT, silent about the WHY (the portal blood-price stays hidden until
the Darnas reveal in ch12, unchanged).

OPEN (stakes): proclamation tone — a demand ("come north and stand with the crusade") vs
a warning ("I am coming for you, willing or no")? And do you learn of it during the roam
(pamphlet first, council references it — my rec) or first at the council?

## 10. Fresh start / import: NO auto-granted party — DECIDED (2026-07-07, playtest 3)

A fresh SoD start (new SoD character, or a BG1 character imported into fresh SoD —
both `SOD_fromimport=0`) is vanilla-granted an alignment-picked default party via
BDINTRO's `JoinPartyOverride` pool; with the dungeon skipped they materialized in the
palace bedroom out of nowhere (playtest 3: Jaheira/Khalid/Minsc/Dynaheir/Safana). **Cut:
you wake alone** (Imoen at the bedside per §5) **and gather your own party in the city**
— the SoD recruiters are all there anyway. The continuous BG1→SoD transition
(`SOD_fromimport=1`) keeps the full carried party (wave-1 component 110), untouched;
Safana's import auto-join blocks are preserved. Implemented as component 145 (requires
140).

Also locked in playtest 3 (2026-07-07):
- **Imoen's join/rejoin replies are NOT party-size-gated** — they stay visible with a
  full party and `JoinParty()` pops the engine's reform screen (matches every SoD
  recruiter).
- **Korlasz's breakout opener rewritten** (BDKORLAS state 24, new line unvoiced):
  vanilla "you delivered me to this hell" assumed the player caught her in the removed
  dungeon; the new line blames the PC as **Sarevok's killer**. All four replies
  unchanged.
- **Skie double-appearance guard DEFERRED to the Skie pass:** her 3 a.m. scene
  (`CreateCreature("bdskie")`, bd0103.baf) has no in-party guard — with Skie carried
  from BG1 it would spawn a second Skie. Guarding it needs a replacement for the
  `bd_plot` 54→55 advance the scene owns. User direction: if she's in the party she
  should just *start the conversation* herself — and generally, **the more Beamdog
  cutscenes removed, the better**.

## 12. Skie: minimal talk-to-join at the palace — BUILT (component 197), lines PENDING SIGN-OFF

Issue #2 / PT-4 (2026-07-11). User direction: *"skip all that and just have her there
joinable? Maybe talk about her father's dead for a moment and keep it short for now."*
Estate/gear grant on recruit deferred (user: "nothing special or huge impact").

**Shape (built 2026-07-12, dev-installed as comp197):**
- The vanilla palace meeting (BDSKIE 8–15, the "talking to Daddy" contradiction) is
  gated off; a new SHORT exchange takes its place at the same entry point (post-council
  click): opener acknowledging Entar's death → the ask → join / decline. Decline keeps
  her in the hall (re-offer state) until the plot-55 departure cleans her up.
- **Key finding:** her `JoinParty()` states (BDSKIE 5–7/1–4) are Beamdog **cut
  content** — gated to BD0120/BD0130, which she never reaches; vanilla SoD Skie was
  never recruitable. comp197 resurrects that machinery (join sets `bd_joined=1`,
  attaches BDSKIEC, the camp dismiss/re-recruit cluster works as shipped; a new
  catch-all state covers field re-recruit outside the two camp areas).
- **Plot surface retired:** BD2000 Boareskyr banter (spawn cut; Bence auto-starts the
  battle wrap himself — the bridge door `Bridge_Barrels` only opens in BDBENCE 32,
  re-routed Skie-free; `bd_plot` 293→294 kept, verified reader-less), the BD3000
  missing-Skie quest (BDBENCE 33/39 + script starter gated; BDNEDERL greeting
  re-pointed so the Marshal never asks), BD4000 placed actor (appearance schedule 0),
  BD4100 rescue (unreachable, `bd_skie_plot` parked at 0), BD7000/BD7100 vignette
  chain (already dead via comp210 — comp197 requires it).
- **In-party safety sweep** (she could never be a party member before, so vanilla
  targets `"bdskie"` unguarded): BD0102 plot-55 `bddest` → `!InParty` guard; BD7100
  bridgefort sweep `DestroySelf` → `!InParty` guard; BDSKIE.bcs auto-dialog /
  chapter-11 destroy / EscapeArea blocks → False()-gated; BDBENCE 32's
  `EscapeAreaObject("bdskie")` → scrubbed; dialog states 8/34/37/39/53 → False()-gated
  (in-party click hazards).
- BG1-carried Skie (comp110): the join replies hide while a DV `SKIE` is in the party
  — no second Skie can be recruited. The council-spawn *cameo* itself stays (PT-3b
  audit scope).

**PENDING SIGN-OFF:** the 11 new lines in
`chriz-sod-remix/languages/english/csr197skie.tra` (word-level, BG1/BG2 register).

**In-game verify checklist (next playtest):** palace click after the council reaches
the new state 91 (not the dream state 0 — trigger-less-state model, research 15 §3);
join works + she persists across the plot-56 departure; decline → re-offer → cleanup
at departure; Boareskyr wrap: Bence auto-talks after the battle, bridge opens, no
Skie; BD3000: Nederlok/Bence never mention her; dismiss in the field → re-recruit
catch-all. Live-save note: the user's current save already consumed the vanilla
meeting (`EscapeBD0102=1`, she despawned) — re-arm via console:
`C:CreateCreature("bdskie")` + `C:SetGlobal("EscapeBD0102","BD0102",0)`.

## OPEN — next sparring round
1. Sign-off on the §4 cut surface (strangle-by-flag + council re-points + cheap-now
   removal list).
2. ~~Korlasz's sequencer contents~~ — DECIDED 2026-07-06: the control bomb (§2a).
3. §9 stakes tone — DECIDED 2026-07-06 (proclamation shipped in comp180). Delivery edge
   still open: retiring for the night without entering the great hall skips the
   proclamation — fix or accept.
4. Component 150's three beyond-spec dialog gates (BDBELT 40 t2, BDRASAAD
   28.0/32.1/36.0, BDDYNAHE 23 t1) — build deviation pending sign-off.
