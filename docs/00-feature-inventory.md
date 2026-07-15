# chriz-sod-remix — Feature Inventory

**Living reference doc** (generated 2026-07-10, from the tp2/lib components, the dev
WeiDU.log, and the design docs; keep updated per pass). Single deduplicated view of the
mod: code/component reality drives status; design detail is folded into the matching
component. This is INVENTORY, not decisions — decisions live in
`docs/01-remix-wishlist.md` and `docs/design/`.

Source-of-truth files: `chriz-sod-remix/setup-chriz-sod-remix.tp2` (v0.6.3, 31
component declarations), `docs/01-remix-wishlist.md` (scope anchor),
`docs/design/wave1/`, and `docs/design/chapters/`.

---

## 1. Implemented (built + installed on the dev install)

Five install GROUPs in the WeiDU UI: **@1000** Wave-1 global levers, **@1001**
Prologue-city, **@1002** Coast Way, **@1003** road north, and **@1004** coalition camp.
All are in-place patches (COPY_EXISTING / EXTEND_TOP / EXTEND_BOTTOM /
DECOMPILE_AND_PATCH); nothing is uninstalled. Every
component carries a REQUIRE_PREDICATE that the SoD loose `BD*` content exists, so the
whole mod no-ops cleanly on a BG2:EE-only install. The dev target has **30 selected
components installed**; 901 is the unchosen half of the exclusive 900/901 pair. The
live install remains on v0.5.0 and is not the implementation target.

### Global levers (Wave 1 — GROUP @1000)

| # | Feature | What it does | Deps |
|---|---------|--------------|------|
| 100 | Rest-ambush felt-rate 5× reduction | Remaps each area's `.are` day/night rest-% down ~5× (via `restmap.tpa`) across the 30 areas with an active rest table; the engine rolls per in-game hour, so listed 6–18% = felt 39–80%/8h → knocked to felt ~8–15%. Reads current value (composes with other mods); leaves BDNOREST cancellers + empty tables. Changes **frequency only**, not pack size. | pred `bd0120.are` |
| 110 | Keep all companions at SoD start | Strips the 28 BD0103 `LeaveParty()+DestroySelf` dismiss blocks (29 names) so the whole BG1 party carries into SoD; +9 recruiter-site EXTEND_TOP skip-blocks (BD0101/0108/0110/0111/1000/2000/2100/7000/7100) suppress duplicate recruit-spawns / Dorn gear-grab for kept members. | pred `bd0103.bcs` |
| 120 | Remove the hooded man (mid-campaign) | Excises Irenicus from his 5 mid-campaign scenes (BD0103 bedside, BDCUT10/11 interrogation vision, BDCUT28 Bhaal-vision, BD5100 cameo, BDSCRY/BDIMOEN dangling options). Sets nothing the endgame reads; the endgame chain is deliberately left for the ending rework. | pred `bd0103.bcs` |
| 130 | Skip the four chapter rest-dreams | EXTEND_TOP on BDBALDUR.bcs pre-sets `bd_ddd=4` (natural post-all-dreams value) so PLAYER1D's dream launchers never fire; the four nights become ordinary rests. PLAYER1D.BCS left untouched (EET-compat). | pred `bdbaldur.bcs` |

### Prologue — city (GROUP @1001)

| # | Feature | What it does | Deps |
|---|---------|--------------|------|
| 140 | Skip the Korlasz dungeon (instant exit) | Productionizes Beamdog's debug-skip: party lands in BD0120 so all bootstrap runs, BDINTRO staging is gutted, default journal chain + `bd_plot=50` written, `bdcut00z` fired via EXTEND_BOTTOM (so EET Bhaalspawn grants fire first); black-cover fade. **Foundation of the whole prologue pass.** | pred `bd0120.are` |
| 145 | No auto-granted starting party | Removes the 9-NPC + Safana fresh-pool `JoinPartyOverride` joins so a fresh/imported-into-fresh SoD start wakes solo; continuous BG1→SoD path (comp 110) untouched. *(Declared after 150 in the tp2 → installs after 150.)* | REQUIRE 140 |
| 150 | No assassination night, crusade council | "Strangle-by-flag" kills the first-night palace assassination; 14-day timeskip moved behind a "retire for the night" servant choice (csrserv); BD0100 night-ambush set swept; BD0102 council re-gated LT52 → exactly `bd_plot=51`, crusade-only, captured-assassin corpse dropped. **Prereq for 160/180/185/190/195.** | pred `bd0120.are` |
| 160 | Imoen stays and is recruitable | Imports keep build/XP/gear (defused BD0120 strip → parked → swapped into bedroom); fresh starts get `csrimo` BG1-chassis clone (XP floor 64k); BDDIALOG IMOEN2 row re-pointed to `csrimoen`; adds the XP catch-up ladder vanilla omits for Imoen. | REQUIRE 140+150 |
| 170 | The Korlasz jailbreak | Re-timed BD0116 fight on vanilla rematch scaffolding: rebuilt `csrkorl` (Mage 12, Slow+Confusion+Glitterdust sequencer) + named 6-member crew (Hasska/Vhast/Sillune/Porios/Grit/dying Fist) carrying the re-homed dungeon loot; difficulty-branched roster; HARDEST buff layer resolved by spell NAME; SCS detect-and-adapt. Stairs-top BD0102 hint beat re-times the trigger. | REQUIRE 140 |
| 175 | XP ledger: Liia's reward after the jailbreak | The skipped dungeon carried ~24,700/char guaranteed XP; the jailbreak returns ~1,600/char in kills. Liia's return-beat close pays **24,000/char** as one quest reward (user option c, 2026-07-10; anchor-checked patch of csrcele state 2, award before DestroySelf). **Unit-corrected 2026-07-12: delivery is now `AddXPObject(Player1..6,24000)` — the original single `AddexperienceParty(24000)` divides among the party and paid only ~4,000/char (user-verified in-game).** | REQUIRE 170+180 |
| 180 | Celebration + Caelar's proclamation | Victory beat on first walk into BD0102 (nobles + Fist dressing w/ click-dialogs, Liia toast / Belt seconds, BG1 register, palace locked for the night); opens the jailbreak-quest journal and hands over Caelar's proclamation naming the Bhaalspawn (`csrpam`); Liia return beat + Fist march after the jailbreak. | REQUIRE 140+150 |
| 185 | Entar Silvershield removed (stays dead) | Unspawns his plot-51 war-council appearances (2 spawn coords, 14 staging actions, count-guarded); rebuilds the plot-56 departure send-off around Belt; drops his roll-call name + the "weren't you killed?" resurrection reply. **City chapter only** (trial/BDCUT62/CRE-DLG deferred to the epilogue pass). | REQUIRE 140+150 |
| 187 | Assassination night set never spawns | Schedule-zeroes the nine always-placed BD0100 night actors (Corwin, three assassins, two guards, three corpses), preventing the one-frame render/pop that comp150's script sweep could not stop. The sweep remains as protection for saves with BD0100 already baked. | REQUIRE 150; pred `bd0100.are` |
| 190 | Skie's second-night bedroom visit removed | A Skie-free dawn wake mirrors the two BD0103 night blocks and pre-sets `BD_MDD005=1` so they can never fire (party sleeps to dawn, `bd_plot` 54→55 as before); BDSKIE night root (state 16) sealed with False(). | REQUIRE 150 |
| 195 | Assassination/poison references scrubbed | Zero-new-text cleanup after 150: reply/state False() gates + 2 ALTER_TRANS re-routes (BDSCHAEL 227 retire-commit moves onto the "ready to march" reply + EXIT; BDLIIA 13 "how fares Imoen?" → training advice) across Corwin/Eltan/Edwin/Liia/Fist/debug. de Lancie supply-poison quest explicitly out of scope. | REQUIRE 150 |
| 197 | Skie: talk-to-join recruit at the palace | Replaces the contradictory "talking to Daddy" opener with the signed-off short Entar-death exchange, restores Beamdog's cut `JoinParty()` scaffold, retires Skie's remaining SoD plot surface, and guards every remaining script target for an in-party Skie. Estate/gear inheritance remains deferred. | REQUIRE 150+185+210 |

### Coast Way (GROUP @1002)

| # | Feature | What it does | Deps |
|---|---------|--------------|------|
| 200 | Coast Way Crossing: fewer spiders, fairer bridge | Cuts the 8-spider west installation (appearance dword zeroed) + the Spiders02 re-arm point + the two west web traps (east group stays); drops the bridge wall-of-force from BDCUT14; interrupt timer THREE_ROUNDS → FIVE_ROUNDS. | pred `bd1000.are` |
| 210 | Coast Way Forest removed; Rasaad recruits at camp | Zeroes BD7000's static WMP visibility flag (the only reveal) → area permanently unreachable; Rasaad's spawn state machine cloned to the BD1000 Fist camp `[640.3690]`; the Skie sub-quest dies with the area. Save-baked worldmaps keep BD7000 visible on in-flight saves (harmless). **Prereq for 900/901.** | pred `bd1000.are` + `bd7000.are` |
| 215 | XP ledger: BD7000 removal compensated | Closes comp210's ledger hole: BD7000 carried 20,665 party XP (orc warband 3,165 + Tsolak kill 8,500 + the 9,000 stake quest — one award; the ×12 in BDISABEL.dlg is reply-branch duplication). **16,500 party-total** (80%; ≈2,750/char at 6) riding the guaranteed chapter-9 transition award in BD7100.bcs. Shipped 2026-07-13. | REQUIRE 210; pred `bd7100.bcs` |
| 220 | Dwarven dig site re-garrisoned | Cuts ~169 pre-placed undead (BD1100 69 / BD1200 100 + 11 moves) to a designed shape: 1 horde room, an honor guard (2 mummies + 2 elite skeleton warriors) standing on the vacated "Drowned in Blood" coords before the lich (2026-07-10 polish — literal replacement per the locked placement rule), pushover groups, umber-hulks-only dig monsters; no-save cheese hard-banned; 80% of cut kill-XP returns as one **106,700 party-total** chunk on the lich clean-kill (engine-divided like the kill XP it replaces; ≈17,783/char at 6 — unit-corrected 2026-07-12). Quest wiring (Semahl, Deepvein, Coldhearth) preserved. | pred `bd1100.are` + `bd1200.are` |
| 225 | Scrying pool: one text-only Caelar omen | Requires all three Silver Scepters and both Essences; keeps the 3,000 party-total scepter reward, then consumes both Essences atomically, shows the approved abstract Caelar text, grants 1,000 XP once to Player1–6, and leaves the pool permanently dormant. The cut wight stays cut and its vial moves to `Sarcophagus01`; all Imoen/Caelar/Hooded picker routes and cinematics are unreachable while `BDSCRY.DLG` remains structurally intact for Aura compatibility. **Dev-installed and semantically verified; runtime pending.** | REQUIRE 120+220; pred `bd1200.are` + `bdodscry.bcs` + `bdscry.dlg` |
| 245 | Coast Way bridge: wall removal is skip-proof | Patches CUTSKIP's mirrored BDCUT14 end-state so skipping the scene cannot re-raise comp200's removed force wall or restore the vanilla three-round timer; keeps the wall gone and the timer at FIVE_ROUNDS. Establishes the rule that every BDCUT patch must audit CUTSKIP. | REQUIRE 200; pred `cutskip.bcs` |
| 900 | Treasure from removed content: **collect** | Mod-wide treasure choice, "collect" flavor: the BD7000 loot (Gemblade+1, Suncatcher+2, Boot-and-a-Half of Speed, Wand of Paralyzation ×5, Ring of Free Action, SODTRE08 ×2 / 09) lands in camp chest Container009 `(509,3220)`; sets `csr_keep_treasure=1`. **Installed on dev.** | SUBCOMPONENT @902 (XOR 901); REQUIRE 210 |

Component 901 is the declared but unselected XOR alternative: remove the treasure with
BD7000 and set `csr_treasure_removed=1`. It is not one of the 30 installed component rows.

### The road north / Ch. 9 (GROUP @1003) — quick-win pass, shipped 2026-07-11

| # | Feature | What it does | Deps |
|---|---------|--------------|------|
| 230 | Road north: fewer, cleaner enemy camps | Main-line trash cut: BD7100 63 cuts (hobgoblin/orc camps, beetles, displacer pack, small spiders of both nests, troll thin-out 32→21 in four kept clusters; ogre camp + gargantuan/sword-spider elites + all ~24 camp NPCs + BD7110 troll lair stay), BD2000 8 (beetles/worgs/wight; siege pickets + scripted battle untouched), BD2010 27 (warren core of 8 stays). 29,025 cut kill-XP → **+23,200 party-total** once-block (≈3,870/char at 6; unit-corrected 2026-07-12) on the Boareskyr resolution (`bd_plot > 292`, both branches; the script's 6000/3000 are Dorn/patrol side quests, deliberately not ridden). | pred `bd7100/bd2000/bd2010.are` |
| 240 | Forest of Wyrms: bugbear cave removed, temple behind the dragon | Retargets the only two BD7220-bound travel regions at each other (BD7210 `TranBD7220` → BD7230 `ExitBD7220`, BD7230 `TranBD7220` → BD7210 `ExitBD7220`; names kept so `EscapeAreaObject` still works — the temple's fleeing cultist now runs into the dragon cave). BD7220 = unreachable, file untouched, reversible; spectacles gimmick survives (bdmisc01 lives on BDZAVIAK/BD0109). Plus BD7200 28 cuts (bugbear door-guards/displacers/wolves/small spiders; wyverns+phase spiders+hill giant stay) and the 6 post-Neothelid invisible ambushers (BD7230AM goes inert; loot mundane). 28,395 ledgered (incl. 14,810 from the cave) → **+22,700 party-total** once-block (≈3,780/char at 6; unit-corrected 2026-07-12) on the Neothelid kill. | pred `bd7200/7210/7220/7230.are` |
| 250 | Morentherene: a real dragon on Hard/Insane | Two CREATE-built stat spells applied asleep via vanilla's own ApplySpellRES delivery (EXTEND_TOP bd7210.bcs, difficulty-gated once-blocks). Hard+: +56 HP (168), AC −6, THAC0 −2, saves +3, MR 35. Insane stacks to: 230 HP, AC −9, THAC0 −4, saves +5 total, MR 50, 4 APR. Breath/wing buffet/AI untouched (SCS-safe); Core and below vanilla. Baseline verified: 112 HP, AC −1, THAC0 2, saves 5–8, MR 15. | pred `bd7210.are` + `bdmorent.cre` |
| 255 | Boareskyr battle: durable explosive barrels | BDKEGX 25 hp / 0% fire resist → **120 hp / 75% fire** (cold stays 50): the battle's loss condition no longer pops to random mephit splash "with no counter" on higher difficulties. CRE-level patch covers placed + scripted barrels; nothing scripts BDKEGX by name; story detonations use Kill() and still work. Fast fix — the elemental/portal sequence rework stays open (04-coalition.md). | pred `bd2000.are` + `bdkegx.cre` |

### The coalition camp / Ch. 10–12 (GROUP @1004) — quick-win pass, shipped 2026-07-12

| # | Feature | What it does | Deps |
|---|---------|--------------|------|
| 260 | Coalition camp arc: fewer, cleaner enemies | 183 cuts / 129,495 XP across the scouting maps: BD7300 119 of 139 hostiles (beetles/boars/displacers/hobgoblins/orogs/wolves/ogre camp; hill giants 10→3+leader, phase spiders 7→4; the nymph pocket + its dead-orog field, ettins, elite spiders, all neutrals stay), BD7400 21 (beetles, banned bone bats + shadowed soul, burning skeletons 9→4), BD7310 1 (banned Unsleeping Guardian), BD5000 32 (displacer pack, orc camp, greater wyverns 4→1; crusader camp + Murs' 12k ogre quest untouched), BD5100 10 (corrupted-grove pockets B/C thinned, pocket A intact; myconids + all neutrals stay). **+103,600 party-total** (≈17,270/char at 6; unit-corrected 2026-07-12) riding the guaranteed ch-11 transition 20k in BD4000.bcs. | pred 5×`.are` + `bd4000.bcs` |
| 270 | Kanaglym: fewer undead | NE graveyard 19→8 (3 banned shadowed souls; archers 9→3, armored 3→2, bladed 2→1; the 4k skeleton-warrior mini-boss anchors the rest). South quest cluster neutral-until-quest = untouched by construction; C0MNEV01 (foreign mod) never touched. **+5,200 party-total** (≈870/char at 6; unit-corrected 2026-07-12) riding the Kherriun 12,000 award (both branches, one fires). | pred `bd5300.are` + `.bcs` |
| 280 | No party dispel at the basement reveal | BOTH reveal variants strip the party (6× bddispel on Player1–6 in BDCUT45A **and** BDCUT45B) and CUTSKIP mirrors both (12 more) — all 24 removed; ward flare, bdglowgr glow and every enemy-side dispel stay. Corrects the earlier "45B only dispels enemies" note. | pred `bdcut45a/b.bcs` + `cutskip.bcs` |

### Meta

`chriz-sod-remix` v0.6.3, tail-installable WeiDU mod; 31 component declarations in 5
install GROUPs; 30 selected components are installed on dev (901 is the exclusive
unchosen alternative); all in-place patches with loud count-guards (PATCH_FAIL on mismatch);
backup dir `weidu_external/backup/chriz-sod-remix`; EET and standalone BG:EE+SoD both in
scope.

**Locked decisions already shipped as components (traceability):** item 1 / wave1-02
keep-party → **110**; item 5 / wave1-01 rest-ambush 5× → **100**; item 10 / wave1-03
hooded-man (mid) + dreams → **120/130**; 2026-07-06/07 fresh-start grant cut → **145**;
2026-07-06 Entar stays dead (city) → **185**; 2026-07-09 Skie second-night visit →
**190**; Skie talk-to-join + SoD-plot retirement → **197**; assassination night,
render-proofing, and residue → **150/187/195**; 2026-07-08 Coast Way tiers +
skip-proof bridge → **200/210/220/245**; 2026-07-15 single Caelar omen / all old
scrying visions retired → **225**; treasure choice → **900 selected / 901 unselected**;
2026-07-10/11 road-north
quick-wins (trash cut, bugbear-cave removal + temple rewire, dragon tiers) →
**230/240/250**; 2026-07-12 coalition-camp quick-wins (scouting-map + Kanaglym cuts,
no reveal dispel, durable barrels) → **260/270/280/255**.

---

## 2. Locked policy and remaining unbuilt work

### Guiding principles (locked, cross-cutting)
- **Compatibility first** — must play well with vanilla, SCS, Spell Revisions, Artisan's
  Kitpack, CDTweaks, EET; explicit anti-goal is Artisan-style fragility.
- **Slim SoD down hard / removal over rewriting** — when a map goes, relocate its
  load-bearing content (triggers, items, quest-givers, NPCs).
- **Process order** — global/system levers → arc treatment → chapter-by-chapter passes.
- **BG1/BG2 writing register** for all rewrites (Sarevok/Irenicus peak); dropping VO to
  rewrite is always acceptable.
- **Test on the dev copy**; live install read-only.
- **Standalone BG:EE+SoD in scope** alongside EET — the ending replacement branches per
  platform (EET handoff vs native campaign end).
- **No global locks** for zero-ambush areas or creature softening — decided per-chapter.
- **No no-save/no-roll cheese anywhere** — shadowed souls (BDSHSOUL) banned in every SoD
  area; bone bats + the Unsleeping Guardian on the not-fun list. First realized in Coast
  Way (comp 220); applies to every later pass.

### Narrative arc (locked, not yet built)
- **Caelar Argent = main antagonist & final boss** (lore verified: crusade to free her
  uncle Aun Argent from Avernus).
- **Remove the ENTIRE post-victory epilogue, no replacement** — dream, Skie murder,
  arrest, trial, jail, breakout, endgame hooded-man; BG2 begins unexplained (original
  BG1→BG2 feel). Bounded by the EET seams (trial/jail self-contained; the transition
  must still end in BD6100 with the gear bank + K#TELBGT). This pass **unblocks**: Skie's
  death removal, the endgame hooded-man, and the epilogue-coupled Entar cleanup (BD0035
  trial placement, BDCUT62, BDENTAR.CRE/DLG deletion).

### Companions (locked, partially shipped)
- **Skie playable as a simple BG1-style talk-to-join recruit** — shipped by component
  197 using her existing BG1 soundset; components 190/210 remove the night visit and
  BD7000 sub-quest. Only the optional estate/gear inheritance remains deferred.
- **Keep Imoen / drop the poisoning + mage-training plot** — shipped across 150/195/160;
  component 225 removes the remaining remote-training scrying vision.
- **BG1-only dismissed companions stay where dismissed** (no camp catch-up) — accepted
  step-1 limitation; SoD-native kept companions retain vanilla camp catch-up.

### XP policy (locked, partially realized)
- **Anchor**: MC enters SoD ~220–250k, finishes ~700–750k (target gain ≈450–530k/char);
  tracked as a per-chapter ledger, not a global reweight.
- **XP-neutral per-chapter ledger** — re-inject removed XP into kept milestones each
  pass; known carriers: chapter transitions 65k/char, Coldhearth Lich 22k plus
  component 220's 106,700 party-total chunk (≈17,783/char at six), Kherriun 12k,
  Halatathlaer 32k, Daeros 18k.
- **Delivery rule (updated 2026-07-12):** remix XP compensation lands as one collected
  milestone award, never dripped. Party-total ledgers use `AddexperienceParty`; genuinely
  per-character amounts use one per-slot `AddXPObject` award.
- **Prologue ledger shipped:** component 175 grants 24,000 XP to each Player slot on
  Liia's post-jailbreak return beat.
- **Calibration lever**: +~10% main-quest rewards if the curve comes in low — only after
  playtesting, against a real save near the BG2 transition.

---

## 3. Deferred (flagged, waiting on a later pass)

| Feature | Waiting on / unblocked by |
|---------|---------------------------|
| Place non-party companions as SoD pickups (item 1 step 2) | A later companion pass (optional placement + a little dialogue) |
| Scripted travel-ambush rework / URE degut (item 8, wave1-04) | Its own pass; gut BD0060/0063/0064/0066 arenas (story vignettes URE6-10 stay) |
| Per-area zero-ambush designations (wave1-01) | Each chapter's trash/zero-list decision |
| Dream-content rewrite (wave1-03) | Maybe-someday; skip already shipped (130), content preserved in research/09 |
| Coldhearth Lich fight rework (Coast Way §3) | A dedicated lich pass (phylactery telegraph / power-down / SCS brain) |
| Skie estate/gear inheritance | Optional follow-up only; the talk-to-join core and BG1 soundset are already shipped by 197 |
| Full Corwin dialogue rewrite | Surface census prepped (docs/research/16); a later rewrite pass |
| Epilogue-coupled Entar removal (BD0035 trial, BDCUT62, CRE/DLG) | The epilogue pass (deleting now spams "creature not found") |
| Per-playthrough sequencer randomization (Korlasz) | Cheap roadmap note |
| Rioters-instead-of-assassins street vignettes (prologue §4) | Roadmap |
| Imoen BG1-death detection | Intentionally skipped — unconditionally present by design |
| Backtracking without EET (Coast Way §4) | Its own global pass |
| de Lancie supply-poison quest | Explicitly OUT of scope (excluded, not postponed) |

---

## 4. Planned / wishlist status

*(Wishlist items 3 "open chill start" and 4 "Korlasz drop / items re-sourced" are
substantively delivered by the prologue pass — 140/170/180 — though the wishlist text
predates it.)*

- **item 6 — Remove a lot of enemy groups** (per-chapter; Coast Way applies it).
- **item 7 — Replace enemy masses with a few fun enemies** (per-chapter; dig site is the model).
- **item 13 — Rework Hell/Avernus + end fight; Caelar dialogue; new portrait.** Blocked on the Belhifet-placement decision.
- **item 14 — Hephernaan not obviously the villain.**
- **item 15 — Cyric temple → one big Ziatar fight**, strip the filler.
- **item 16 — Morentherene much scarier:** the Hard/Insane stat component shipped as
  250; any deeper breath/AI redesign would be a separate future pass.
- **item 17 — SCS-style scripting for important fights** (piloted by 170/Korlasz).
- **Per-chapter baseline XP recount** (wave1-05 tooling).
- **Road north (Troll Claw → Forest of Wyrms → Boareskyr):** quick wins shipped as
  230/240/250/255; a broader narrative/set-piece pass remains open.

---

## 5. Open questions / next-round decisions

- **Belhifet placement** (ending shape): the fight before Caelar, or defeated *by* Caelar in a scene? Item 13 waits on this.
- **XP baseline trust**: calibrate against a real save near the BG2 transition.
- **Per-area rest treatment:** component 100 already shipped the frequency-only 5×
  remap; pack-size and zero-ambush-area decisions remain per-chapter questions.
- **Hooded-man tavern rumors (BDRUMOR3, ch 8/9/10)**: remove now or with the ending pass.
- **Travel-ambush frequency + per-arena treatment** (BD0066 goblin horde first cut candidate).
- **Prologue OPEN sign-offs**: §4 cut surface (OPEN#1), proclamation tone/delivery (§9/OPEN#3), comp150 beyond-spec gates (OPEN#4).

---

## Historical queue snapshot (recorded 2026-07-10; superseded)

This list records what was queued on that date; it is not current status. Components 175
and 197 and the road-north quick-win pass subsequently shipped. Current status lives in
the implemented tables above.

Done that day: commits; comp175 (24k Liia reward) built+installed; dig-site §3a executed
(guard replaces drowned; 106,700 party-total chunk, ≈17,783/char at six); ch9 early directions recorded (03-roadnorth.md);
ending scope confirmed pure-removal; placement + XP-fill principles locked.

1. **Playtest** — the city chapter (185/190/195), the jailbreak reward (175), and the
   dig site (guard + 106,700 party-total chunk) were installed on dev.
2. **Chapter-9 sparring round 1** — user takes a closer look at research/13 +
   03-roadnorth.md early directions (temple relocation is the big structural call).
3. **Ending/epilogue pass** — pure removal (band 590–671, research/14); seam mechanics
   only, no rewrites; unblocks Skie-death/Entar/hooded-man/BDRUMOR3 tails.
4. **Skie pass** — talk-to-join re-gating + full remaining plot removal (research/15).
5. **Tiered dig-site encounter (later)** — research/17+18 in flight (BG2 mechanism +
   lich-lite candidates).
6. **BG1 soundsets for returning BG1 companions in SoD** (backlog component).
7. **Corwin rewrite** (deferred; scope in research/16).

**Historical frontier at that snapshot:** Wave 1 + prologue + Coast Way (incl. polish)
were complete and installed; Chapter 9 and the ending/epilogue pass were then next.
