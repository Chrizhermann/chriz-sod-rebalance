# 10b — Korlasz-Dungeon Skip: Minimal State Vector
**Status:** research complete (verified against the live install, 2026-07-05; produced by the prologue-pass verification workflow). Feeds `docs/design/chapters/01-prologue.md`.

## 1a. EET IMPORT FLOW — everything between campaign entry and palace arrival (VERIFIED)

**Step 1 — BDSODTRN.baf** (cutscene, runs in final BG1 area; `research/data/sod_baf/BDSODTRN.baf:1-46`):
`EndOfBG1=1`, `SOD_fromimport=1`, `PartyCured=1`; `CopyGroundPilesTo("BD0120",[949.1686])` (line 15 — ground-pile copy target is the BD0120 entry chamber); `bdresurr` P2–P6, `bddispel` all, `AdvanceTime(TEN_DAYS)`, `bdrejuve` all; movies ENDMOVIE + SODCIN01; `MoveToCampaign("SoD")` (line 42). No explicit teleport — landing position comes from SODSTRTA.2DA (see §4; INFERRED).

**Step 2 — BD0120.bcs arrival blocks** (import-relevant; `research/data/sod_baf/BD0120.baf`):
- `K#NewGame` EET block (:26-39) — **skipped for imports** (requires `ENDOFBG1=0`).
- `K#StoryMode` (:41-50) — story-mode only, OHSMODE3 on Imoen2.
- BPRNG1 Slave Ring destroy (:575-586, both flows).
- **BD0120_START** (:600-627, both flows): destroy MISC55 (Duke Eltan's Body) from all players; resurrect P2-P6; rejuve all; **`GiveItemCreate("BDKEYR",Player1)` Key Ring (:625, given nowhere else in the corpus)**; `BDAI_RESET_TIMERS=1`.
- Viconia SoD portrait (import only, :629-638): `BD_VICONIA_PORTRAIT=1` + `BDVICPOR` spell.
- **IMOEN2 strip** (import only, :651-663): `BD_Imoen_Items=1`; `ActionOverride("Imoen_import_eq",TakeCreatureItems("IMOEN2",ALL))` — Imoen_import_eq is a **container in BD0120.are at (92,1098)** (VERIFIED by ARE parse); then IMOEN2 `LeaveParty()` + `DestroySelf()`.
- Party capability flags at bd_plot=0 (:665-843): `bd_party_has_lockpicking/traps/warrior/priest/wizard` ("BD0120" scope) — consumed by BDINTRO's Safana auto-join and the fresh companion pool.
- `cd_fall_of_sarevok` journal cleanup (:7541-7578, both flows, unconditional once): EraseJournalEntry of ~30 BG1 "Rise of Sarevok" strrefs (231475, 226812, 227091…227514).
- Intro launcher (:5502-5511): `GlobalLT("bd_plot","global",2)` → `StartCutSceneEx("bdintro",TRUE)`. This is the **single choke point** both flows pass through.

**Step 3 — BDINTRO.baf import branch** (`research/data/sod_baf/BDINTRO.baf`):
- Per-companion re-wiring, `SOD_fromimport=1` + `InMyArea`: dynaheir→DYNAHJ/bddynahe (:224), minsc→MINSCJ/bdminsc (:234), rasaad (:244), viconia→VICONIJ/bdviconi (:254), safana (:264), edwin (:274), jaheira (:284), khalid (:294), dorn (:304), neera (:314), baeloth (:324). BG1-only NPCs get J-dialog + empty override script: Ajantis (:334), Alora, Branwen, Coran, Eldoth, Faldorn, Garrick, Kagain, Kivan, Montaron, Quayle, Shar-Teel, Skie, Tiax, Xan, Xzar, Yeslick (:498). Mod hooks on same flag: C0Aura (:1-10), L#BRIST (:12-21).
- **Safana auto-join** (:508-539): requires `BD_Imoen_Items=1` **and** (no lockpicking **or** no traps flag); `BeenInParty("safana")` → MoveGlobal+resurrect+rejuve+rewire+JoinPartyOverride, else CreateCreature("safana7")+join.
- **Final True() block** (:541-582) — runs in BOTH flows: `bd_plot=2`, `bd_npc_camp_chapter=0`, **`chapter=7`**, `DREAM=7`, `BD_TURNOFF_GEARSCRIPT("BD0120")=1`, `sprite_is_dead{safana,dynaheir,minsc,rasaad}=0`, rejuve all, party JumpToPoint staging, `ChangeAIScript("bdplayer",OVERRIDE)` on Player1, `CreateCreature("bdshimoe",[881.1652])` (escort Imoen), breakable-cutscene rig (cutskip area script).
- Walk-in scene (:584-688) ends `ActionOverride("IMOEN2",StartDialogNoSet(Player1))` → BDIMOEN state at bd_plot=2.

**Step 4 — dungeon beats** (dialog-driven; decompiles in scratchpad `dlg/`):
- BDIMOEN state 6: bd_plot 2→10, `BDSH_Imoen_Floor=1`, journal **256379 QUEST** (also addable by BDFF1000 states 14/15, evil variant 256380).
- BDKORDEF.dlg: bd_plot=20. BDSHKORL.baf:37-51 (Korlasz AI, HP<71%): bd_plot=25 + neutral + dialog. BDKORLAS.dlg: 25/26 during talk; surrender = **bd_plot=27 + `BD_KORLASZ_SURRENDER=1` + journal 259573 QUEST_DONE**; fight = `BD_Korlasz_Fight("BD0130")=1`. On surrender BDSHKORL.baf:53-63: DropInventory + **AddXPWorthOnce (=2500 XP; BDKORLAS.CRE 0x14 VERIFIED)** + EscapeAreaObject rope.
- BD0130.baf:142-156: **bd_plot=29** once Korlasz dead-or-surrendered; :215-250 journals 267326/266937 QUEST, 259572 QUEST (Korlasz dead only). Other BD0130 journals: 264295/264311-315, 270023-25 (side content).
- **BDIMOEN state 32** (BDIMOEN.d:303-314): `AddXPObject(Player1..6, 5000)` — **5,000×6 = 30,000 party XP**, `BDSH_Imoen_Floor=3`, `BDSH_Rope=1`, Imoen + BDFF1000/1/2 EscapeAreaObject("Tranbd0120rope"). Optional BDSHBHR papers hand-in (states 31/36: TakePartyItem).
- Farewell: BDIMOEN state 35: **bd_plot=40** + `bd_Imoen_farewell=1`; states 53/54 (BDIMOEN.d:496-509): journal **269028 QUEST_DONE** + `StartCutSceneEx("bdcut00z",FALSE)`. Alternative exit via BDFF1000 states 28/29.

**Step 5 — BDCUT00Z.baf** (:1-32): rejuve all; **`TakeObjectGoldGlobal("BD_TAKEN_GOLD","GLOBAL",Player1)`** (impounds ALL party gold into the global); `BD_EXTRA_GOLD=17`; **`BD_SAFEHOUSE_DONE=1`**; `LeaveAreaLUA("bd0103",…)` whole party → guest floor. Note: bdcut00z does NOT set bd_plot.

**Step 6 — BD0103.bcs with BD_PLOT<51** (`research/data/sod_baf/BD0103.baf`):
- :106-120 `PlayerChest00` (container at (105,473)) impounds every player's BACKPACK items.
- :122-129 if `BD_Imoen_Items=1` → `MoveContainerContents("BD0120*Imoen_import_eq","BD0103*Imoen_equipment")`, flag→2. (Imoen_equipment container at (704,855), VERIFIED.)
- :131-225 signature-item flags (import only) for dead/never-joined NPCs: BD_HAS_NEERAS_BAG/BELT/STAFF, BD_HAS_DORNS_SWORD, BD_HAS_RASAADS_BOOTS, BD_HAS_BAELOTHS_ROBE — each checks party, PlayerChest00, **and Imoen_equipment**.
- :227-~620 strips **every** companion: BG1-only NPCs LeaveParty; SoD NPCs (MINSC/DYNAHEIR/SAFANA/VICONIA/BAELOTH/EDWIN/JAHEIRA/KHALID/NEERA/RASAAD/DORN) are resurrected, LeaveParty, **DestroySelf** (e.g. SAFANA :489-501). Palace phase starts solo by design.
- **Palace-night block** :728-786, trigger = `GlobalLT("BD_PLOT","GLOBAL",51)` alone: TextScreen("DPALACE"), **`bd_npc_camp_chapter=1`, `BD_PLOT=51`**, GiveItemCreate bdscrl04 Treasury Note (flavor only — zero consumers in corpus/dlgs), journal 267494 QUEST, `AdvanceTime(FOURTEEN_DAYS)`, rest+sleep staging, then the **pre-placed BD0103.are actor 'IMOEN2' (cre BDIMOEN at (221,459))** StartDialogNoSet → bd_001_plot chain.
- :1064-1079 Imoen_equipment default stock (unconditional, once): 3×POTN08, POTN14, WAND12_(10), 40 arrows, BOW05, SCRL77/75/67.
- Departure chain from there is palace-internal: BDSCHAEL/BD0102 set 52, 54 (Imoen poisoned scene :707-726), BDSERV/BDCUT05 55, BD0102 56, BD0101/BDSCHAEL 57, BDSCHAEL 60-63, BD0021 reads 60-63 → sets 65 → BDCUT10 (bd_plot=100, bd_npc_camp_chapter=2, `IncrementChapter("chptxt8")` at BDCUT10.baf:33 → chapter 8).

## 1b. FRESH (non-import) FLOW (VERIFIED)
- **campaign.2da** SOD row, STARTARE column → **SODSTRTA.2DA**: START_AREA **BD0120**, START_XPOS 760, START_YPOS 1695, **START_XP 64000** (override copies dumped; VERIFIED).
- BD0120: `K#NewGame` EET block runs (ENDOFBG1=0): DREAM=7, ENDOFBG1=1, NEWGAME_SOD=1, RemoveWorldmapAreaFlag(BG0900), K#REMBHA on Player1, TakeItemListPartyNum("K#PLOT",99); K#BhaalSpawnAbility1-6 rolled by alignment (:52-479), granted as SPIN101-106 once bd_plot≠0 (:481-573).
- `bd_remove_2da_items`: `DestroyAllEquipment()` on Player1 (:588-598). `BD_Init_Gold`: `GiveGoldForce(30000)` if party gold <30000 (:640-649). Class/proficiency gear handouts (:845-3845; brac06 for weak-STR warriors :845-863, weapons, BD_Two_Weapons club :3840-45).
- **Companion pool spawn** at bd_plot 0→1 (:3856-~5500): NumInParty × alignment × thief/priest/warrior/wizard flags choose 1-5 spawns from evil pool {dorn7, baelot7, viconi7, EDWIN7_, safana7}, neutral {neera7, khalid7, JAHEIR7_, dorn7, safana7}, good {JAHEIR7_, khalid7, MINSC7_, dynahe7, safana7}; each sets `SPRITE_IS_DEAD<npc>=0` + `ChangeSpecifics(<npc>,NONE)`.
- BDINTRO fresh branch (`SOD_fromimport=0`): `JoinPartyOverride()` per spawned NPC (:31-129); **signature items**: khalid brac06 (:131), viconia ring22 (:143), jaheira ring22 (:155), safana ring05 (:167), dynaheir/neera/edwin RING08_ (:179-213); monk fist equip (:215-222); then same final True() block + Imoen escort + walk-in scene as import.

## 2. Dungeon-set state that ANYTHING later reads (persistence table)
| State | Set by | Later readers |
|---|---|---|
| bd_plot 0→1→2→10→20→25/26/27→29→35→40 | BD0120/BDINTRO/BDIMOEN/BDKORDEF/BDSHKORL/BDKORLAS/BD0130/BDFF1000 | BD0103 needs only **LT 51**; JAHEIRAJ.dlg banter GlobalGT 25; BDTUTOR.baf:143 GT 27 (dungeon-internal); BDSCLANE.baf:57 `GlobalLT(bd_plot,36)` is a Beamdog dead-code bug (bd_plot ≈300 there). **No reader anywhere needs 41-50; 50 is only BDDEBUG's convention.** |
| chapter=7 (BDINTRO:550) | BDINTRO both flows | chapter-checking content until IncrementChapter chptxt8 (BDCUT10.baf:33) |
| bd_npc_camp_chapter 0→1 | BDINTRO:549 → BD0103.baf:737 | camp/follower system per chapter |
| **BD_KORLASZ_SURRENDER=1** | BDKORLAS.dlg (with bd_plot=27 + journal 259573 QUEST_DONE) | BD7300.baf:174-181 (Dead Man's Pass: spawns Ephrik); banters in DYNAHJ, JAHEIRAJ, KHALIJ, SAFANJ, XANJ, XZARJ, MONTAJ, QUAYLJ, SHARTJ, ELDOTJ, FALDOJ, AJANTJ; BDROPE/BDSARC02/BDSHIMOE etc. dungeon-internal |
| Korlasz alive/dead (`Dead("BDKORLAS")`) | combat | **BD0116.baf:1-13 spawns her imprisoned in the palace-basement cell iff `!Dead("BDKORLAS")`** (never-created ⇒ !Dead ⇒ cell spawn = skip-consistent with "captured alive"); cell dialog adds journal 261626 + BD_SPAWN_KORLASZ=2; BD0116.baf:64-75 journal 261627 QUEST_DONE when dead; BDFIST1A/BDPORIOS/BDTUTOR read Dead() |
| XP | BDIMOEN state 32: 5000×6=30,000 party; Korlasz surrender AddXPWorthOnce=2,500 (CRE 0x14); dungeon kills/quests | XP economy only |
| **BD_TAKEN_GOLD** (all gold) | BDCUT00Z:20 | **BD4100.baf:553-580 (Dragonspear Castle Keep, First Floor)**: Gold_Chest gets TAKEN+EXTRA (AddGlobals) + note BDMISC42 if `BD_OPHYLIS_HAD_GOLD=1` (set in BDOPHYLL.dlg state 36), else flat 2000. Treasury Note bdscrl04 has **no consumers** — pure flavor |
| BD_EXTRA_GOLD=17 | BDCUT00Z:21 | only BD4100 AddGlobals |
| **BD_SAFEHOUSE_DONE=1** | BDCUT00Z:22 | every companion override script (BDMINSC.baf:461-470 etc., 16 NPCs incl. MKHIIN/CORWIN/GLINT/VOGHIL) — gates the join-XP-floor snapping system |
| BD_Imoen_Items 0→1→2 | BD0120:658 → BD0103:127 | BDINTRO Safana auto-join requires =1; BD0103 container move requires =1 |
| Imoen items | Imoen_import_eq container (BD0120.are) → MoveContainerContents → Imoen_equipment (BD0103.are) | player retrieval; signature-item flags :131-225 scan it |
| Journals | 256379/80 QUEST open; 259573 or 259572 resolve; 269028 QUEST_DONE close; +side (266937, 267326, 259570/71 mummy, 264295…) | journal UI only |
| sprite_is_dead\*/=0, ChangeSpecifics NONE | BDINTRO:553-556, BD0120 pool blocks | camp-NPC availability checks (Dead() object matching) |
| DREAM=7 | BDINTRO:551 / K#NewGame | dream sequencing (no exact-7 baf reader; marks BG1 dreams done) |
| cd_fall_of_sarevok=1 + ~30 EraseJournalEntry | BD0120:7541-78 | BG1 journal cleanliness (EET/fixpack-patched block) |
| BDSH_Imoen_Floor / BDSH_Rope / bd_Imoen_farewell / BD_IMOEN_TRAPS | dungeon dialogs/scripts | dungeon-internal only (BD0120, BD0130, BDSHFFIS, BDSHIMOE + C0Aura mod comment BD0120.baf:1-24) |

## 3. MINIMAL replacement-intro state vector (derived)
Beamdog's own skip (**BDDEBUG.baf:151-160**, `bd_debug_move_to_bg`) is the verified floor: `bd_npc_camp_chapter=1; bd_plot=50; StartCutSceneEx("bdcut00z",FALSE)` — everything else self-assembles from BD0103's LT-51 blocks. A production-quality replacement cutscene must add, in order:
1. **Companion wiring** (import): the BDINTRO import-branch SetDialogue/ChangeAIScript per NPC — keep BDINTRO blocks 1-539 intact and replace only the staging block (:541-582) + walk-in blocks (:584-688). This preserves mod hooks (C0Aura, L#BRIST) for free.
2. **Globals**: `chapter=7`, `DREAM=7`, `bd_plot=50` (any <51 works; 50 matches BDDEBUG and satisfies the GT-25/GT-27 banter reads), `bd_npc_camp_chapter` may stay 0 (BD0103:737 sets 1), sprite_is_dead resets, `ChangeAIScript("bdplayer",OVERRIDE)` on Player1.
3. **From BD0120 blocks that would still run if we keep landing there** (recommended, see §4): BDKEYR, MISC55 destroy, resurrections, Viconia portrait, IMOEN2 strip, cd_fall_of_sarevok cleanup, K# new-game machinery — all free if the party spends 2-3 script passes in BD0120 before teleport-out.
4. **Korlasz default**: set `BD_KORLASZ_SURRENDER=1` + journal 259573 QUEST_DONE (canonical "captured alive"; BD0116 cell spawn is automatically consistent because she was never created ⇒ !Dead). Add 256379 QUEST then 269028 QUEST_DONE for a tidy journal.
5. **XP compensation**: 30,000 party XP (Imoen state-32) + 2,500 (Korlasz) + whatever kill-XP budget design assigns.
6. **Exit**: `StartCutSceneEx("bdcut00z",FALSE)` — do NOT reimplement it; it owns BD_TAKEN_GOLD/BD_EXTRA_GOLD/BD_SAFEHOUSE_DONE and the bd0103 move.
7. **Ground piles**: BDSODTRN:15 copies BG1 ground piles to BD0120 [949.1686]; if the player never walks BD0120, imported ground loot is stranded → either patch BDSODTRN's target to BD0103 or accept the loss (piles are droppings the player left on the floor in the BG1 finale area).

**If imported IMOEN2 is NOT stripped (stays in party through the palace):** three palace CREs share DV `IMOEN2` (BDIMOEN.CRE, BDIMDEAD.CRE, BDSHIMOE.CRE — all dlg BDIMOEN; imported IMOEN2.CRE has dlg IMOEN2J; all VERIFIED by CRE parse). Concrete breakage at bd_plot 40-63:
- BD0103.baf:773-785 night scene: `ActionOverride("IMOEN2",StartDialogNoSet(Player1))` resolves ambiguously between the party member (wrong dialog — IMOEN2J has none of the bd_001_plot states) and the placed BDIMOEN actor → scene hangs or fires an EET banter instead.
- BD0103.baf:693 and :713: `ActionOverride("IMOEN2",DestroySelf())` at plot 52/54 → can destroy a joined party member (INFERRED: engine-dangerous, party-slot corruption risk).
- BD0103.baf:819-822: `ApplyDamage("IMOEN2",20,PIERCING)` + bdgassa1 poison — the assassination scene can hit the party Imoen.
- BD0103.baf:801-803 (BDCUT02 intro): creates a second bdimoen and equips "IMOEN2" the NOCIRCLE ring → two Imoens on the guest floor.
- BD0103.baf:106-120 impounds her backpack anyway; the BD_Imoen_Items chain never fires so Imoen_equipment only gets the default stock; BDINTRO Safana auto-join condition never true.
Conclusion: the strip (BD0120:651-663 semantics — items to a container, LeaveParty, DestroySelf) is load-bearing and must happen before BD_PLOT reaches 51; keeping her would require re-authoring every `"IMOEN2"` reference in BD0103/BDCUT02/BDIMOEN palace states.

## 4. Fresh-start engine mechanics if BD0120 is skipped
- Start area is data-driven and per-campaign: campaign.2da SOD row → SODSTRTA.2DA (START_AREA BD0120, 760.1695, START_XP 64000). Only the SOD row references SODSTRTA, so editing it is surgically scoped. It would (INFERRED) also relocate import landings, since BDSODTRN's MoveToCampaign has no explicit destination.
- **However**: the entire new-game bootstrap lives in BD0120.bcs/BDINTRO.bcs — EET's K# blocks (Bhaalspawn abilities SPIN101-106, K#PLOT strip, K#REMBHA), DestroyAllEquipment, 30,000 gold, gear handouts, companion pool + JoinPartyOverride + signature items, BDKEYR, journal cleanup. A START_AREA change silently skips all of it and every mod that patched those scripts.
- **Recommendation (design)**: keep START_AREA=BD0120 and do an **instant teleport-out**: the choke point is BD0120.baf:5502-5511 (`GlobalLT(bd_plot,2)` → StartCutSceneEx("bdintro")). Let 2-3 area-script passes run (new-game blocks all execute at bd_plot=0 before this trigger), keep BDINTRO's wiring/join blocks, and replace only its staging+walk-in blocks with the §3 vector ending in bdcut00z. Fresh-flow companions join then are immediately stripped/destroyed by BD0103 (:489-501 pattern) exactly as vanilla does — and their BeenInParty/sprite flags are preserved for the camp system. Player never gains control inside the dungeon; zero state is lost; both flows share one implementation.

Key file paths: `C:\src\private\chriz-sod-rebalance\research\data\sod_baf\{BDSODTRN,BD0120,BDINTRO,BDCUT00Z,BD0103,BD0130,BDSHKORL,BDDEBUG,BD0116,BD4100,BD7300,BDCUT10,BDMINSC}.baf`; decompiled dialogs in scratchpad `dlg\{BDIMOEN,BDKORLAS,BDKORDEF,BDFF1000,BDOPHYLL,BDMUMMY,BDSCHAEL,BDSERV}.d`; live 2DAs `C:\Games\Baldur's Gate II Enhanced Edition modded\override\{CAMPAIGN,SODSTRTA}.2DA`.

## Verified facts
- BDSODTRN.baf (EET transition cutscene) sets EndOfBG1=1, SOD_fromimport=1, PartyCured=1, copies ground piles to BD0120 [949.1686], resurrects/dispels/rejuvenates the party, advances time 10 days, plays ENDMOVIE+SODCIN01, then MoveToCampaign("SoD") with no explicit destination (BDSODTRN.baf:1-46).
- campaign.2da SOD row column STARTARE points to SODSTRTA.2DA, which declares START_AREA=BD0120 at (760,1695) and START_XP=64000 (both files read from live override).
- BD0120.baf:651-663 (import only): sets BD_Imoen_Items=1, has container-object 'Imoen_import_eq' TakeCreatureItems("IMOEN2",ALL), then IMOEN2 LeaveParty+DestroySelf; Imoen_import_eq is a container in BD0120.are at (92,1098) (binary ARE parse).
- BD0103.baf:122-129 moves the stripped gear: MoveContainerContents("BD0120*Imoen_import_eq","BD0103*Imoen_equipment") when BD_Imoen_Items=1 and BD_PLOT<51; BD0103.are has containers PlayerChest00 (105,473) and Imoen_equipment (704,855) and a pre-placed actor 'IMOEN2' using BDIMOEN.CRE at (221,459).
- BDIMOEN.dlg state 32 awards AddXPObject 5000 to Player1..Player6 (30,000 party XP), sets BDSH_Imoen_Floor=3 and BDSH_Rope=1, and has Imoen+3 Flaming Fist escorts EscapeAreaObject via 'Tranbd0120rope' (decompiled BDIMOEN.d:303-314, state header BEGIN 32).
- Dungeon exit cutscene BDCUT00Z.baf: TakeObjectGoldGlobal("BD_TAKEN_GOLD","GLOBAL",Player1) impounds all party gold, sets BD_EXTRA_GOLD=17 and BD_SAFEHOUSE_DONE=1, moves party to bd0103; it does NOT set bd_plot (BDCUT00Z.baf:20-30).
- The impounded gold is returned at BD4100 ('Dragonspear Castle Keep, First Floor' per sod_areas_dataset.csv): Gold_Chest receives BD_TAKEN_GOLD+BD_EXTRA_GOLD (AddGlobals) plus note BDMISC42 when BD_OPHYLIS_HAD_GOLD=1 (set in BDOPHYLL.dlg state 36), else a flat 2000 gold (BD4100.baf:553-580). The Treasury Note bdscrl04 given at BD0103.baf:739 has zero consumers in the corpus.
- Beamdog's own dungeon-skip exists: BDDEBUG.baf:151-160 sets bd_npc_camp_chapter=1, bd_plot=50, then StartCutSceneEx("bdcut00z",FALSE) — nothing else.
- BD0103.baf:728-786 palace-night block triggers on GlobalLT("BD_PLOT","GLOBAL",51) alone: TextScreen DPALACE, bd_npc_camp_chapter=1, BD_PLOT=51, treasury note, journal 267494 QUEST, AdvanceTime 14 days, sleep scene, then the placed IMOEN2 actor StartDialogNoSet.
- BD0103.baf strips the entire party before plot 51: BG1-only NPCs LeaveParty; SoD companions are resurrected, LeaveParty, then DestroySelf (e.g. SAFANA at BD0103.baf:489-501); the palace phase is designed to start solo.
- Korlasz state machine: BDSHKORL.baf:37-51 forces dialog at HP<71% setting bd_plot=25; BDKORLAS.dlg sets 26 then 27+BD_KORLASZ_SURRENDER=1+journal 259573 QUEST_DONE on surrender; BDSHKORL.baf:53-63 then DropInventory + AddXPWorthOnce + EscapeAreaObject; BDKORLAS.CRE XP value = 2500; BD0130.baf:142-156 sets bd_plot=29 once she is dead or surrendered.
- BD0116.baf:1-13 spawns Korlasz imprisoned in the palace-basement cell whenever !Dead("BDKORLAS") — a never-created Korlasz satisfies this, so a skip with her alive is automatically consistent with the 'captured alive' outcome.
- Post-prologue readers of dungeon state: BD7300.baf:174-181 spawns Ephrik if BD_KORLASZ_SURRENDER=1; 12 companion J-dialogs (DYNAHJ, JAHEIRAJ, KHALIJ, SAFANJ, XANJ, XZARJ, MONTAJ, QUAYLJ, SHARTJ, ELDOTJ, FALDOJ, AJANTJ) reference bdkorlas; JAHEIRAJ reads GlobalGT(bd_plot,25); BD_SAFEHOUSE_DONE=1 gates the join-XP-floor system in all 16 companion override scripts (e.g. BDMINSC.baf:461-470). No reader anywhere requires bd_plot values 41-50.
- bd_plot setter map for 0-63: BD0120 (79x value 1, fresh pool spawn), BDINTRO 2, BDIMOEN.dlg 10/35/40, BDKORDEF.dlg 20, BDSHKORL.baf+BDKORLAS.dlg 25/26/27, BD0130.baf 29, BDFF1000.dlg 35/40, BDDEBUG 50, BD0103.baf:738 51, BDSCHAEL.dlg 52/54/57/60/61/62/63, BD0102 52/56, BDSERV+BDCUT05 55, BD0101 57, BD0021 65, BDCUT10 100 (+IncrementChapter chptxt8 at BDCUT10.baf:33).
- BDINTRO.baf final True() block (541-582) runs in BOTH flows: bd_plot=2, bd_npc_camp_chapter=0, chapter=7, DREAM=7, BD_TURNOFF_GEARSCRIPT=1, sprite_is_dead resets, bdplayer AI on Player1, creates escort Imoen 'bdshimoe'; import branch rewires 11 SoD companions' dialog+AI and 17 BG1-only NPCs' J-dialogs; Safana auto-joins imports lacking thief skills (BDINTRO.baf:508-539, requires BD_Imoen_Items=1).
- CRE parse: BDIMOEN.CRE, BDIMDEAD.CRE, BDSHIMOE.CRE all have death variable IMOEN2 and dialog BDIMOEN; imported IMOEN2.CRE has DV IMOEN2 but dialog IMOEN2J — three palace creatures collide with the party member on DV if she is not destroyed.
- If imported IMOEN2 stays in party: BD0103.baf:693 and :713 DestroySelf her at plot 52/54, :819-822 ApplyDamage 20 piercing + poison spell targets her, :773-785 StartDialogNoSet resolves against the wrong dialog (IMOEN2J lacks the bd_001_plot states), and :801-803 creates a duplicate Imoen.
- BD0120-resident bootstrap that a skip must preserve: BD0120_START block (destroy MISC55, resurrect, give BDKEYR key ring — granted nowhere else, BDAI_RESET_TIMERS), Viconia portrait (import), EET K#NewGame block (fresh only: NEWGAME_SOD, Bhaalspawn abilities SPIN101-106, K#PLOT strip), DestroyAllEquipment + 30,000 gold + gear handouts (fresh), cd_fall_of_sarevok one-shot erase of ~30 BG1 'Rise of Sarevok' journal entries (BD0120.baf:7541-7578, both flows).
- Dungeon journal chain: 256379/256380 QUEST opened by BDIMOEN state 6 / BDFF1000 states 14-15; resolved by 259573 QUEST_DONE (surrender) or 259572 (dead, BD0130.baf:246); closed by 269028 QUEST_DONE in BDIMOEN states 53/54 which also launch bdcut00z; BDFF1000 states 28/29 are the alternate launcher.
- Both flows funnel through one choke point: BD0120.baf:5502-5511, IF GlobalLT(bd_plot,2) THEN StartCutSceneEx("bdintro",TRUE).

## Inferred (not directly verified)
- MoveToCampaign("SoD") lands the party at the SODSTRTA.2DA coordinates — inferred from BDSODTRN containing no explicit teleport action plus the observed BD0120 (760,1695) arrival; editing SODSTRTA would therefore redirect BOTH import and fresh flows.
- DestroySelf on a joined party member (BD0103.baf:693/713 if IMOEN2 kept) is savegame-dangerous (permanent party-slot removal); severity inferred from engine behavior, not tested on this install.
- With BD_KORLASZ_SURRENDER left at 0 and Korlasz never created, companion banters that branch on surrender-vs-dead read the 'not dead' path; setting the surrender flag to 1 in the skip gives the most coherent downstream text (Ephrik spawn at BD7300, cell dialog) — inferred from trigger shapes, individual banter lines not exhaustively read.
- BDSCLANE.baf:57 GlobalLT("bd_plot","global",36) is a Beamdog typo (bd_plot is ~300 during that battle; likely meant bd_battle) — inferred dead code, harmless to the skip.
- The camp/follower system tolerates companions who never existed (fresh-start skip without pool spawn) because its checks are Dead()/BeenInParty-shaped and a never-created NPC reads as alive-but-absent; flagged as the main residual risk if SODSTRTA redirection were chosen instead of instant-exit.
- bd_plot=5 reader in BDIMOEN.dlg has no setter anywhere in the corpus (dead dialog state).
- DREAM=7 marks the BG1 dream track complete so SoD resting does not replay BG1 dreams; no exact-7 reader exists in the .baf corpus, consistent with threshold-style checks elsewhere (see docs/research/09-sod-dreams.md).

## Design notes
- Adopt Beamdog's own skip recipe as the spine: bd_plot=50 + bd_npc_camp_chapter=1 + StartCutSceneEx("bdcut00z",FALSE) (BDDEBUG.baf:151-160). Never reimplement bdcut00z — it owns the gold impound, BD_EXTRA_GOLD, BD_SAFEHOUSE_DONE and the bd0103 move.
- Implement as an 'instant exit': keep START_AREA=BD0120, let 2-3 area-script passes run (all EET K# new-game blocks, gear, gold, keyring, Imoen strip, journal cleanup execute at bd_plot=0), keep BDINTRO blocks 1-539 (companion wiring + Safana auto-join + mod hooks), and WeiDU-patch only BDINTRO's staging block (541-582) and the two walk-in blocks (584-688) to set chapter=7/DREAM=7/bd_plot=50/sprite flags and launch bdcut00z. One implementation covers both flows; never edit WeiDU.log entries.
- Do NOT change SODSTRTA.2DA START_AREA: it silently skips every mod- and EET-patched BD0120/BDINTRO block (Bhaalspawn abilities, K#PLOT strip, 30k gold, gear, companion pool, BDKEYR) that would then need duplication.
- Set BD_KORLASZ_SURRENDER=1 in the replacement and add journal 256379 QUEST + 259573 QUEST_DONE + 269028 QUEST_DONE; leave Korlasz uncreated so BD0116's cell spawn plays the 'captured alive' epilogue for free.
- Never let imported IMOEN2 survive past the intro: the strip (items→Imoen_import_eq container, LeaveParty, DestroySelf) is load-bearing; three palace CREs share her death variable and BD0103 destroys/damages/poisons 'IMOEN2' by DV during plot 51-54.
- XP compensation budget for the skipped dungeon: 30,000 party XP (Imoen state-32 award) + 2,500 (Korlasz surrender) + kill/quest XP per docs/research/03-xp-economy.md; fresh starts already get START_XP 64000 engine-side.
- If import ground-pile fidelity matters, patch BDSODTRN's CopyGroundPilesTo target from BD0120 [949.1686] to a BD0103 spot; otherwise document the loss (only affects loot deliberately left on the floor of the BG1 finale area).
- bd_plot=50 is the safest skip value: <51 satisfies every BD0103 trigger, >27 satisfies BDTUTOR/JAHEIRAJ banter reads, and no content reads 41-50.
