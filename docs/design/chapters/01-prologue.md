# Chapter Pass — Prologue (Korlasz dungeon + Baldur's Gate city opening)

**Status: v2 after sparring round 1 (2026-07-05).** Most of the shape is DECIDED; the
Korlasz roster is a DRAFT to be discussed person-by-person; council-seam mechanics and the
assassination-mention sweep are being verified (results → `docs/research/11*`).
Research basis: `docs/research/10a–10d`. Builds on installed components 110/120.

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
| 3 | **"Vhast"** | BDKORME8, F5 | **plain Fighter 10** | bruiser; **chugs an oil of speed at fight start** (SCS potion blocks when present — standard SCS behavior; scripted UseItem fallback otherwise) | **Sword of Ruin +2** (2-hander, wielded) |
| 4 | **"Sillune"** | BDSHIS07, T5 | **plain Thief 9** | backstab + restealth; **3 invisibility potions** arm the restealth cycle | **gem bag**, the gems + ~4,100 gp tomb cash ("grabbed the valuables for the escape") |
| 5 | **Porios** — the tomb sentry, captured too (existing named NPC) | BDPORIOS, M5 | **Mage 8; NO flee behavior — fights to the end** (user cut the coward beat) | support caster (Mirror Image/Haste/MM) | his **Cloak of Minor Arcana** (unique) |
| 6 | **"Grit"** — Korlasz's dust-mephit familiar | BDSHKFAM | as-is | harassment, Glitterdust | — |

*BDSHSARE's flag (`BD_SAREVOK_SECRET`, feeds the chapter-10 masks quest) is re-homed onto
item acquisition (PartyHasItem watcher), not the old BD0130 container.
**Wand of Fire: DROPPED entirely** (not carried, not loot). **Journal 266701 (assassin
text): swapped for a new crusade-only .tra line.**

**Scaling draft:** EASY/EASIEST = 1,2,3,5 · NORMAL = all six · HARD = + skeleton-guard
pair (the cells' previous occupants, raised) · HARDEST = + one elite undead anchor
(Unsleeping-Guardian tier). Non-casters get SCS generic brains + potions when SCS
present; SoD-native stack otherwise (cookbook #13).

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

## 6. Celebration — DECIDED: light for v0.1, bigger scene on the roadmap

Arrival → short praise beat in the great hall built from existing duke lines (Liia
234300, Belt 264733/264741, blessing chain) + the mini-quest hook (§2) → free roam.
No fireworks (no VFX asset in SoD; roadmap if ever). Roadmap: staged celebration scene,
crowd set-piece, street vignettes of crusade tension.

## 7. XP ledger entry (prologue) — numbers after fight lock
Removed: dungeon kills/quests, 30k wrap-up award, surrender cascade. Added: jailbreak
fight (six+ real kills incl. leveled boss), jailbreak quest award, celebration/completion
award. Calibrate after playtest per 05-xp-ledger policy.

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

## OPEN — next sparring round
1. Sign-off on the §4 cut surface (strangle-by-flag + council re-points + cheap-now
   removal list).
2. Korlasz's sequencer contents: control bomb (rec) / alpha strike / mixed (§2a).
3. §9 stakes: proclamation tone + where the player first learns of it.
