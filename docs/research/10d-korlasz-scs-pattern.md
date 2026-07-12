# 10d — Korlasz Anatomy + SCS Boss-Party Pattern
**Status:** research complete (verified against the live install, 2026-07-05; produced by the prologue-pass verification workflow). Feeds `docs/design/chapters/01-prologue.md`.

# TASK D — Korlasz + the SCS boss-party pattern

## 1. Korlasz herself (all VERIFIED on the live install unless marked)

### CRE — `override/BDKORLAS.CRE` (4,204 bytes)
- **Mage 8, Generalist kit** (kit dword `0x40000000` = word-swapped `0x4000` MAGESCHOOL_GENERALIST), human female, NE. **HP 32/32**, AC 10, THAC0 18, 1 APR, saves 13/9/11/13/10, STR 10 / INT 17 / DEX 17 / CON 16 / CHA 15. **XP value 2500.** EA=128 (NEUTRAL — fight starts via dialog). Deathvar `BDKORLAS`, dialog `BDKORLAS`, anim 0x6210.
- **Spellbook** (install runs Spell Revisions, so SR names): L1 Mage Armor/Obscuring Mist/Magic Missile/Shield/Spook; L2 Horror/Mirror Image/Vocalize/Glitterdust; L3 Flame Arrow/Haste/Slow/Dire Charm; L4 Confusion/Minor Globe/Stoneskin; plus `SPWI420` (Simbul's Spell Matrix) oddly stored as a *priest* L1 entry. **Memorized:** MM×2, Spook×2, Mirror Image, Glitterdust×2, Haste, Slow, Dire Charm, Confusion, Stoneskin, + 6 Bhaal-cult innates (SPIN102/104×2/105/106×2).
- **Gear: nothing equipped, no weapon, no armor.** Sole inventory item = `DW#RND03` (SCS placeholder token: name strref 9999999, 0 abilities/effects, nothing in any .bcs/.spl/.eff converts it at runtime → **her drop is effectively empty**). Proven added by **SCS #6100 “Potions for NPCs”**: `weidu_external/backup/stratagems/6100/BDKORLAS.CRE` (pre-6100 state) has **0 items**; so does the earliest surviving state `weidu_external/backup/ArtisansKitpack/20000/BDKORLAS.CRE`.
- **Consequence (key finding):** her AI’s scroll/potion blocks — Protection from Elemental Energy scroll (BDSHKORL.baf:87–104), Potion of Clarity (:106–123), Vocalize scroll (:166–178), **Minor Globe scroll (:219–234)** — are **dead code on this install** (HasItem always false). She fights with spells only. Whether pristine SoD ships those items is unresolved (INFERRED that it does, given the bespoke script blocks), but post-EET-import she never had them.
- 10 embedded effects = Artisan’s Kitpack global class patches (8× op326 `C0PR#AT1/MF1/FS1/EK1`, 2× op233 proficiency) — no combat impact.
- **SCS did NOT touch her AI or stats.** SCS 35.21 leaves `BD*` (SoD) creatures alone: Korlasz/Porios/Ammon keep BD scripts, while the non-BD `GHAST.CRE` placed in the same BD0130 got SCS scripts (`dw#gpshm` override, `dw2mp2ge` default).

### Script stack (CRE slots: override=`BDKORLAS`, class=`BDENSHTV`, race=`BDSHKORL`)
- **BDENSHTV.baf** — SoD generic enemy framework: Die→Help; engage on attack/Range 30 (sets `BD_Engaged`, combat/retreat timers); out-of-combat 8-hour “rest” with `RESTORE_FULL_HEALTH` and AI-state reset; help-response chains; return to saved default location.
- **BDSHKORL.baf** (1,821 lines) — her personal brain + fight framework:
  - *Fight opener* (:12–24): in BD0130, `NumTimesTalkedTo(0)` + (See PC | TookDamage | AttackedBy) → `ApplySpellRES("BDSPY")` (op268 marker; removed by `BDUNSPY` op321 after first talk, :26–35), combat music `BDLBB`, `StartDialogNoSet(Player1)`.
  - *Precast* (:77–85): one free Stoneskin on BD0130 presence (`BD_Precast` LOCALS).
  - *Combat*: emulated Minor Sequencer = instant Mirror Image + Shield once (:151–164); then rotation with proper target guards (magic res, saves, Chaotic Commands, rage, spell-immunity, MISC73/HELM06 charm-wards): Stoneskin (:180), Mirror Image w/ True Sight checks (:195), **Confusion vs up to 6 nearest** (:256+, `DifficultyGT(EASY)`), **Slow ×6** (:424+, not EASIEST), **Dire Charm vs fighters/rangers** (:613+, `DifficultyGT(EASY)`), Haste on an ally (:236). On lower sliders she sheds tools; on HARDEST she gains nothing extra (the scroll blocks that would fire are dead).
  - **SURRENDER TRIGGER** (:37–51): `AreaCheck("BD0130")` + `Global("BD_Fin_Talk","LOCALS",0)` + **`HPPercentLT(Myself,71)`** + `See([PC])` → `BD_Fin_Talk=1`, `bd_plot=25`, `ClearAllActions()`, **`ChangeEnemyAlly(Myself,NEUTRAL)`**, `StartDialogNoSet(Player1)`. So at <71% HP she *always* stops the fight and parleys — she cannot be killed in phase 1.
  - *On surrender* (:53–63): `Global("BD_KORLASZ_SURRENDER","GLOBAL",1)` → ClearAllActions, `DropInventory()`, sound GAM_12D1, **`AddXPWorthOnce(Myself,TRUE)`** (party still receives her 2,500 XP), `EscapeAreaObject("Tranbd0120rope")`. In BD0120 she `DestroyAllEquipment()` (:65–75).
- **BDKORLAS.baf** (override) — only the **BD0116 endgame rematch**: `BD_KORLAS_FREED=1` → she force-buffs Stoneskin + Minor Globe + Mirror Image, spawns `cutspy`, kills a Fist enforcer, cutscene `BDCUTKOR` (“Never! I’ll not be imprisoned again!”) → dialog → `Enemy()`. Rematch uses only BDENSHTV + those 3 buffs (BDSHKORL combat blocks are BD0130-gated). BD0116.baf:1–13 spawns her in “Korlasz’s Cell” with `DestroyAllEquipment()` if she’s alive; :15–21 the `TrapBDKorlasz` region sets `BD_KORLAS_FREED`.

### Dialog — `BDKORLAS.dlg` (decompiled; scratchpad `BDKORLAS.d`)
- **State 4** (first talk, BD0130): three replies, each sets `bd_plot=25` → **state 5** → `SetGlobal("BD_Korlasz_Fight","BD0130",1)` + `Enemy()` → fight on.
- **State 7** (condition `Global("bd_plot","global",25)` — reached via the HP<71% re-talk): “I… am defeated” → **state 8** “I and my followers surrender”, with player choice:
  - **Accept** (2 flavors) → `bd_plot=26` → states 10/11: `bd_plot=27`, **`BD_KORLASZ_SURRENDER=1`**, **`AddexperienceParty(1000)`** (1,000 XP **divided among the party** — ~167/char at 6; corrected 2026-07-12, user-verified in-game), journal 259573 QUEST_DONE.
  - **Refuse** (“only one way you leave this place”) → state 9 → `Enemy()` → fight to the death.
- State 0: post-surrender idle line. States 12–16: BD0120 “Imoen at the door” renege variant (`bd_child_plot`,`bdimoedo`). States 17–23: post-surrender chatter. States 24–27: BD0116 endgame → `BD_SPAWN_KORLASZ=2` + `Enemy()`.

### Fight orchestration & payoffs (BD0130.baf)
- `BD_Korlasz_Fight=1` unlocks Massive_Door (:188–197); fight-over (=2 via `Dead("bdkorlas")` or surrender, :214–223) opens it (:199–212) and zeroes the rest-ambush header (`SetRestEncounterProbabilityDay/Night(0)`, :476–488). Kill journal :239–247.
- **Whole-dungeon surrender**: nearly every hostile in BD0120/BD0130 carries `BDSHSURR` in an **ARE actor script slot** (verified in both .ARE actor structs). BDSHSURR.baf: on `BD_KORLASZ_SURRENDER=1` — **undead: `AddXPWorthOnce` + `Kill(Myself)` (full kill XP for every remaining undead, free)**; humans: neutral + `DropInventory` + escape + XP-worth-once. So **surrender ≈ kill-everything XP + 1000/member bonus** — crucial for the XP-reweighting design.
- Sarevok-chest guard wave (:258–372) is difficulty-branched: HARDEST 12 / HARD 9 / NORMAL 8 / <NORMAL 3 creatures. `BDSARC03.baf` (sarcophagus spirit ambush) same pattern: 10/8/6/4.

## 2. Named/elite lieutenants — candidates for her rebuilt party

**BD0130 (boss level):**
| resref | name (actor) | class/level | HP | XP | notes |
|---|---|---|---|---|---|
| BDKORME9 | Follower of Sarevok (CLERIC) | Cleric 6 (half-orc) | 48 | 400 | plate+helm+shield+morningstar, full L1–3 priest book, potion — best “second” |
| BDSHIS08 | Elite Mercenary (ILLUSIONIST) | F/M 5/5 gnome illusionist | 35 | 450 | Spook/MM/MI/Haste memorized, darts; own script BDSHIS08 |
| BDKORME8 | Elite Mercenary (WIZARD_SLAYER) | Fighter 5 | 50 | 500 | anti-mage flavor |
| BDSHIS10 ×2 | Elite Mercenary (ELVEN_ARCHER) | Ranger 5 | 50 | 500 | ranged pressure |
| BDSHIS06 | Follower of Sarevok (BLACKGUARD) | cls 6 (paladin), lvl 4 | 40 | 450 | |
| BDSHIS07 | Follower of Sarevok (SHADOWDANCER) | Thief 5 | 30 | 350 | |
| BDSHIS09 ×4 | Follower of Sarevok (ASSASSIN) | Thief 5 | 30 | 300 | backstab swarm |
| BDKORME1/2 | Mercenary (machine room pair) | F/T 4/5, F 4 | 35/40 | 400 | **have dialogs** — stat-gated parley (STR>13 / WIS>13 talks them down; BDKORME1.d) |
| BDSHKFAM | Korlasz's Familiar | dust mephit (MEPDUS script) | 24 | 175 | flavor-perfect adds |
| BDUNSLGU | Unsleeping Guardian | shadow-class 7 | 58 | 4000 | mini-boss tier |
| BDSHADGR / BDMUMM01 | Greater Shadow / Mummy | 9 / 6 | 72/51 | 3000/3000 | elite undead anchors |

**BD0120:** Porios (`BDPORIOS`, mage 5, 750 XP, surrender questline via `BD_PORIOS_SURRENDER`), Ammon (`BDAMMON`, mage 5, dialog), `BDSHIS04` “Iron Throne Commander” (F4, 750 XP), `BDKORDE8` elven archer / `BDKORDE9` dwarf berserker (both 500/400 XP elites). Quest mummy Fanegonorom (`bdmummy`) is script-spawned (BD0120.baf:5531).

**Reusable activation pattern:** the 12 creatures nearest Korlasz carry **`BDSHKFIN`** in an ARE actor slot (BDKORME3–7, BDKORME8/9, BDSHIS09/10, 2×BDSKGR02): stay/turn NEUTRAL while she's neutral; when she goes hostile or dies (or they're attacked → they set `BD_Korlasz_Fight=1` themselves) they all `Enemy()`+`Help()` as one group (BDSHKFIN.baf:1–49). This is exactly the “boss + synced bodyguards + parley preserved” scaffold to reuse — a new single fight can simply re-point this script (or a copy) at the curated party.

## 3. The SCS boss-party pattern (verified on-install, SCS v35.21)

Installed AI components (WeiDU.log:296–344): #5900 init, **#6000 Smarter general AI**, #6010 calls-for-help, **#6030 Smarter Mages**, #6040 Smarter Priests, **#6100 Potions for NPCs**, **#7140 Improved Undercity assassins**, **#7230 Tougher chapter-five end battle**, #8040 tie level-dependent groupings to slider (plus many tactical components).

### Reference fight rosters
- **Undercity assassins — EET area `BG0123.ARE`**: Rahvin (F11, HP90; scripts `dw#gpsht` / `RAHVIN` / `dw1range`), Haseo (F11, `dw1melke`), Wudei (C12, `dw#pr303`), Gorf (ogre 9, `dw2mc2ge`), Shaldrissa (M13, `dw#mg566`), Carston (F9, `dw1range`), + 3–4 Skeleton Warriors (`dw#gpshm` + `dw1melge`/`dw1range`). (Final-battle trio Semaj `dw#mg437` / “Angelo” `dw#mg158` / Tazok sits in `BG0125.ARE`.)
- **Iron Throne top floor — EET area `BG0615.ARE`**: Zhalimar Cloudwulfe (F11, HP110; `dw#gpsht` / `ZHALIMAR` / `dw1ranbe`), Gardush (F10, `dw1melbe`), Alai (F/M 8/7, **`dw#mg13`**), Aasim (F/C 8/7, `dw#pr2`), Diyab (C/T 9/9, `dw#pr74`), Naaman (M 9/9, `dw#mg289`), Thaldorn (T6, `dw1melth`) — all keep vanilla `LEAVECH7` in one slot for the flee-at-chapter-end plot.

### How SCS builds a party member (the recipe)
1. **Override slot:** `dw#gpsht` (humanoids) / `dw#gpshm` (monsters) — 947-line generic aggro/shout coordinator (Shout 151/251 conventions, Enemy() wiring). Fully generic, reusable.
2. **Class or race slot:** a tiny fight-specific plot script (`RAHVIN.bcs`/`ZHALIMAR.bcs` are 394 bytes: `See([PC]) + NumTimesTalkedTo(0) → StartDialogue`).
3. **Default slot = the combat brain:**
   - Non-casters: **shared generic brains** — `dw1melge/melke/melbe/melth`, `dw1range/ranbe`, `dw2mc2ge/ms2be/mp2ge/rp2ge`… Driven solely by `INI("DMWW_genai_difficulty",…)` (571 checks in dw1melge) and potion items (`dw#ptn34/35/21` HasItem/UseItem blocks, dw1melge.baf:616–700). **Assignable to any custom CRE as-is.**
   - Casters: **install-generated numbered brains** `dw#mgNNN` / `dw#prNNN` (585 mage + 311 priest script families in this override!). Generated per spell-loadout, **but every cast and every prebuff is `HaveSpell()`-guarded** — verified in dw#mg13.baf (casts only MM, Chromatic Orb, Icelance, Acid Arrow, Sleep, Emotion, + defensive set, each behind HaveSpell). So they read the CRE's actual memorized book at runtime; missing spells silently no-op.
4. **Prebuffs (“instant prebuffing”):** inside the caster brain — on first sight of an enemy (`instantprep` LOCALS, or `offscreenprep`), it fires `ReallyForceSpellRES("dwswNNN")` — special “(cast previously)” instant variants — then `RemoveSpell()` the memorized slot (dw#mg13.baf:419–545: dwsw212 Mirror Image, dwsw305 Haste, dwsw114 Shield, dwsw408 Stoneskin). Gated by `INI("DMWW_mage_prep_difficulty",N)` with game-`Difficulty()` fallback. No separate prebuf script — the brain does it.
5. **Difficulty hooks:** SCS reads per-category settings from **Baldur.lua 'Game Options' via the EE `INI()` trigger**. Live values on this install (Trilogy documents Baldur.lua): `DMWW_mage_difficulty=4`, `DMWW_mage_prep_difficulty=5` (max prebuffing incl. out-of-sight), `DMWW_genai_difficulty=4`, `DMWW_priest_difficulty=3`, `DMWW_spawn_difficulty=7`; value 0 = follow the game slider (script blocks pair `INI(x,0)` with `Difficulty(HARD/HARDEST)`). Game slider is currently **5 = HARDEST/Insane** (DIFFLEV.IDS: 1 EASIEST … 5 HARDEST), LoB off, extra-difficulty damage active (`'Suppress Extra Difficulty Damage','0'`).

### What a NEW custom encounter must do
- **With SCS present:** put `dw#gpsht` in override; give non-casters `dw1mel*/dw1ran*` defaults (+`dw#ptn*` potions in inventory to enable potion blocks); for Korlasz herself either (a) keep/extend her vanilla `BDSHKORL` brain, or (b) assign an existing `dw#mgNNN` whose repertoire matches her book — **`dw#mg13` (Alai's) is a near-perfect fit**: its prebuff set (Shield/Mirror Image/Haste/Stoneskin) is entirely inside her current spellbook. Clone the SCS creature's memorized book where in doubt.
- **Caveat:** `dw#mgNNN` numbering is generated at SCS install time — stable on THIS install, not across installs/versions. A tail-mod for this install may hardcode them; anything distributable must resolve script names at install time.
- **Guard:** `ACTION_IF FILE_EXISTS_IN_GAME ~dw#gpsht.bcs~` (proves #6000) and per-script `FILE_EXISTS_IN_GAME ~dw#mg13.bcs~`; or `MOD_IS_INSTALLED ~stratagems/setup-stratagems.tp2~ 6030` (reads WeiDU.log — works here even though the `stratagems/` mod folder was deleted; only `weidu_external/backup/stratagems/` remains). **Without SCS:** fall back to the SoD-native stack (class `BDENSHTV` + a BDSHKORL-style bespoke brain) — the fight stays fully functional because that's exactly what vanilla SoD uses.

## 4. Insane-difficulty behavior for scripted (non-spawn) fights
- **Placed ARE actors and `CreateCreature()` results are never duplicated or stat-boosted by the difficulty slider.** The engine's Insane effect is the global **enemy-damage doubling** (active here: `'Suppress Extra Difficulty Damage','0'`); Legacy of Bhaal (separate `Nightmare Mode` toggle, OFF on this install) is the mode that inflates HP/levels.
- **All composition scaling in SoD is explicit script branching**: `Difficulty(HARDEST)/HARD/NORMAL/DifficultyLT(NORMAL)` blocks with different CreateCreature lists — verified twice in the prologue (BD0130.baf:258–372 → 12/9/8/3; BDSARC03.baf → 10/8/6/4). Korlasz's own AI scales *down* on Easy (loses Confusion/Dire Charm/Haste), not up on Insane.
- Rest-ambush spawn amounts use the ARE-header difficulty multiplier (prior project finding), not the slider; SCS's #8040 ties only SCS's own level-dependent groupings to the slider.
- **Design implication:** the rebuilt Korlasz fight should ship its own `Difficulty()` branches (e.g., extra lieutenants/second wave only on HARD+/HARDEST) — that is the native, save-compatible mechanism; Insane already contributes 2× enemy damage for free, and SCS AI sharpness follows the DMWW INI settings automatically.

**Files produced (scratchpad only):** `BDKORLAS.d`, `BDKORME1.d`, `dw#mg13.baf`, `dw1melge.baf`, `dw#gpsht.baf`, `RAHVIN.baf`, `ZHALIMAR.baf`, parsers `creparse.py`/`areactors.py` in `C:\Users\chris\AppData\Local\Temp\claude\C--src-private-chriz-sod-rebalance\3f405051-32e3-4471-9cb3-0ff63d4d5c2c\scratchpad`.

## Verified facts
- BDKORLAS.CRE (live override): Mage 8, Generalist kit (word-swapped 0x4000), HP 32/32, AC 10, THAC0 18, XP value 2500, EA=NEUTRAL(128), dialog BDKORLAS, scripts override=BDKORLAS/class=BDENSHTV/race=BDSHKORL; no equipped gear; sole inventory item is SCS token DW#RND03 (strref 9999999, zero effects).
- weidu_external/backup/stratagems/6100/BDKORLAS.CRE and .../ArtisansKitpack/20000/BDKORLAS.CRE both contain 0 items -> DW#RND03 was added by SCS component #6100 (Potions for NPCs) and she had no items even before all CRE-touching mods on this install.
- No .bcs/.spl/.eff in override references dw#rnd03 -> the token is inert at runtime; her scroll/potion AI blocks in BDSHKORL.baf (SCRL6H :87-104, POTN21 :106-123, SCRL3G :166-178, SCRL1Z :219-234) are dead code on this install because HasItem() always fails.
- Surrender trigger: BDSHKORL.baf:37-51 - AreaCheck(BD0130) + Global(BD_Fin_Talk,LOCALS,0) + HPPercentLT(Myself,71) + See([PC]) -> bd_plot=25, ChangeEnemyAlly(NEUTRAL), StartDialogNoSet(Player1).
- Surrender chain in BDKORLAS.dlg: state 4 (first talk) -> state 5 sets BD_Korlasz_Fight(BD0130)=1 + Enemy(); state 7 (bd_plot=25) -> state 8 -> accept sets bd_plot=27, BD_KORLASZ_SURRENDER=1, AddexperienceParty(1000), journal 259573 QUEST_DONE; refuse -> Enemy() fight to death.
- On surrender BDSHKORL.baf:53-63 gives AddXPWorthOnce (her 2500 XP) + DropInventory + escape via rope; BDSHSURR.baf (attached via ARE actor script slots on nearly every dungeon hostile) kills all undead with full XP-worth and makes humans drop loot, go neutral, escape with XP-worth-once -> surrender pays ~= killing everything + 1000 XP per party member.
- BDSHKFIN.baf (ARE-actor slot on the 12 bodyguards near Korlasz: BDKORME3-9, BDSHIS09/10, 2x BDSKGR02) keeps them neutral until Korlasz turns hostile/dies or they are attacked, then group-Enemy()+Help(); attacking them sets BD_Korlasz_Fight=1.
- Endgame rematch: BD0116.baf:1-21 spawns her (equipment destroyed) in Korlasz's Cell if alive; TrapBDKorlasz region sets BD_KORLAS_FREED -> BDKORLAS.baf force-buffs Stoneskin+Minor Globe+Mirror Image, cutscene BDCUTKOR, dialog states 24-27 -> Enemy().
- Named lieutenants verified from BD0130.ARE/BD0120.ARE actor lists: BDKORME9 cleric 6 (plate/shield/morningstar, full priest book), BDSHIS08 gnome illusionist F/M 5/5, BDKORME8 'wizard slayer' F5, BDSHIS10 elven archer ranger 5 x2, BDSHIS06 blackguard, BDSHIS07 shadowdancer, BDSHIS09 assassin x4, BDKORME1/2 machine mercs with stat-gated parley dialogs (STR>13/WIS>13), BDSHKFAM dust-mephit familiar, BDUNSLGU (4000 XP), BDSHADGR/BDMUMM01 (3000 XP each); BD0120: Porios, Ammon, BDSHIS04 Iron Throne Commander.
- SCS 35.21 installed (WeiDU.log:284-359) incl. #6000/#6030/#6040/#6100/#7140 (Improved Undercity assassins)/#7230 (Tougher chapter-five end battle)/#8040; SCS left BD* SoD creatures untouched but patched non-BD CREs in SoD areas (GHAST.CRE in BD0130 has dw#gpshm/dw2mp2ge).
- Undercity assassins live in EET BG0123.ARE (Rahvin F11/Haseo F11/Wudei C12/Gorf ogre9/Shaldrissa M13/Carston F9 + skeleton warriors); Iron Throne party in BG0615.ARE (Zhalimar F11 HP110, Gardush F10, Alai FM8/7, Aasim FC8/7, Diyab CT9/9, Naaman M9/9, Thaldorn T6).
- SCS slot pattern: override=dw#gpsht (generic shout/aggro; dw#gpshm for monsters), class/race=394-byte fight-specific dialog-starter (RAHVIN.bcs/ZHALIMAR.bcs), default=combat brain: generic dw1mel*/dw1ran*/dw2* for non-casters, generated dw#mgNNN/dw#prNNN for casters (585 mage + 311 priest script families in override).
- SCS prebuffs happen inside the caster brain: HaveSpell()-guarded ReallyForceSpellRES of dwsw* '(cast previously)' instant spells + RemoveSpell (dw#mg13.baf:419-545: dwsw212/305/114/408), gated by INI(DMWW_mage_prep_difficulty) with Difficulty() fallback; all combat casts are HaveSpell-guarded so the brain adapts to the CRE's actual memorized spellbook.
- SCS difficulty is read from Baldur.lua 'Game Options' via the EE INI() trigger; live values: DMWW_mage_difficulty=4, mage_prep=5, genai=4, priest=3, spawn=7; 0 means follow the game slider; the install currently runs 'Difficulty Level'=5 = HARDEST/Insane (DIFFLEV.IDS 1-5), LoB off, 'Suppress Extra Difficulty Damage'=0.
- Insane/scripted-fight scaling: placed ARE actors and CreateCreature spawns are not duplicated or stat-boosted by the slider; SoD scales composition only via explicit Difficulty() script branches (BD0130.baf:258-372 chest guards 12/9/8/3; BDSARC03.baf spirit ambush 10/8/6/4); Korlasz's AI scales down on Easy, not up on Insane; BD0130.baf:476-488 zeroes the rest-ambush header once the fight ends.

## Inferred (not directly verified)
- Vanilla (un-modded) SoD Korlasz probably ships the scrolls/potion her script references (SCRL6H/SCRL1Z/SCRL3G/POTN21) - the bespoke script blocks strongly imply it - but the EET-imported CRE on this install never had them; could not verify against a pristine SoD source.
- DW#RND03 was meant to become potions/loot via SCS's random-treasure machinery; on creatures it appears to be an unconverted leftover token (inert), so on this install killing Korlasz drops effectively nothing.
- BDSPY.spl applies opcode 268 (removed by BDUNSPY op321); its exact function was not identified - inferred to be a pre-dialog protection/marker used by SoD talk-first bosses.
- dw#mgNNN/dw#prNNN numbering is deterministic per install but not stable across SCS versions/component selections (SSL-generated), so hardcoding dw#mg13 is safe only for a tail-mod on this specific install; distributable mods must detect at install time.
- AddexperienceParty(1000) grants 1000 XP divided among the party (~167/char at 6) —
  unit-corrected 2026-07-12 (user-verified in-game; the per-member reading was wrong).
- The C0PR#* op326 effects on many CREs come from Artisan's Kitpack / AK_MULTICLASS_PROFS_FIX global patches (C0 prefix matches, and ArtisansKitpack backups contain BDKORLAS.CRE); they are class-conditional apply-lists with no impact on her as a mage boss.
- SCS deliberately excludes BD* (SoD) content from its AI components - inferred from consistent evidence (all BD mages keep BD scripts, non-BD CREs in the same areas are patched), not from reading SCS source (the stratagems mod folder was deleted from the game dir).

## Design notes
- Rebuilt single fight can reuse the existing scaffolding wholesale: BDSHKFIN for the synced bodyguard group (preserves the parley->fight->surrender flow), BDSHSURR on everything else so the surrender payoff still cascades, and the existing BD_Korlasz_Fight / BD_KORLASZ_SURRENDER / bd_plot 25-27 globals so zero downstream content breaks.
- Keep the HPPercentLT(71) surrender parley but consider moving it lower (e.g. 40-50%) and/or keeping lieutenants active during the parley window; as shipped she can never kill anyone past phase 1 because she stops fighting at 71% HP.
- Give Korlasz her intended consumables back (Minor Globe scroll SCRL1Z, Prot. Elemental Energy SCRL6H, Vocalize SCRL3G, Potion of Clarity POTN21) - this alone revives four dead AI blocks and visibly upgrades the fight with zero new AI code, and works with or without SCS.
- For an SCS-grade Korlasz: her current spellbook already contains dw#mg13's full prebuff set (Shield/Mirror Image/Haste/Stoneskin); assigning dw#mg13 as default script (guarded by FILE_EXISTS_IN_GAME ~dw#mg13.bcs~) gives instant prebuffs + sharper targeting, with vanilla BDSHKORL as the no-SCS fallback. Alternatively keep BDSHKORL and just re-time the surrender threshold - it is already a competent brain.
- Curated party suggestion from verified assets: Korlasz + BDKORME9 (cleric), BDSHIS08 (illusionist), BDKORME8 (wizard-slayer), 2x BDSHIS10 (archers), BDSHKFAM (familiar), plus 2-4 elite undead (BDSKGR03/BDWIGHT2/BDUNSLGU) as difficulty-gated adds - all have real gear and distinct roles, unlike the 109-mob horde.
- Scale composition the SoD-native way: explicit Difficulty(HARDEST)/HARD/... CreateCreature branches (mirror BD0130.baf:258-372); do not rely on the slider to buff a static fight - the engine only doubles enemy damage on Insane.
- XP accounting for the chapter rebuild: current outcomes are kill=2500+loot(nothing) vs surrender=2500+1000xN+XP-worth of all remaining followers; any trash cut automatically shrinks the surrender payout too, so re-weight via the AddexperienceParty amount and/or quest XP, not by re-adding mobs.
- Non-caster lieutenants can take SCS generic brains (dw1melge/dw1range/dw1melth etc.) + dw#ptn* potions to become SCS-smart with zero new scripts; guard with FILE_EXISTS_IN_GAME ~dw#gpsht.bcs~ or MOD_IS_INSTALLED ~stratagems/setup-stratagems.tp2~ 6000, falling back to BDENSHTV+BDSHTAUN (SoD native) otherwise.
- The machine-room pair (BDKORME1/2) already implement a stat-gated non-combat resolution - keep them as-is; they are a model for making the remaining fights 'meaningful' without adding numbers.
