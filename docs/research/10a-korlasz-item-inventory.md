# 10a — Korlasz Dungeon Item Inventory (for re-homing)
**Status:** research complete (verified against the live install, 2026-07-05; produced by the prologue-pass verification workflow). Feeds `docs/design/chapters/01-prologue.md`.

# Korlasz Dungeon Complex — Complete Item Inventory (VERIFIED from live install)

## 0. Complex definition (VERIFIED via .are travel regions)

Parsed travel regions/entrances of every candidate area (live `override\*.are`, region struct type 2):

- **BD0120** ⇄ **BD0130** are the ONLY interconnected pair (two links each way: `TranBD0130`/`Tranbd0130rope`). BD0120 has **no walk-out exit** — leaving is scripted (`BDCUT00Z` → BD0103).
- **BD0113** (wyrmling chamber) exits ONLY to **BD5100** → belongs to the Boareskyr chapter, NOT this complex.
- **BD0114** (spider nest) exits ONLY to **BD7200**; **BD0115** (wolf cave) only to **BD7000** → wilderness-chapter sub-areas, NOT this complex.
- BD0116 (Korlasz-surrender scene room) links only to BD0102 (palace); no travel link to the dungeon.

**Scope of re-homing is therefore exactly BD0120 + BD0130.** (BD0113/BD0114 appendix at the end.)

## 1. Container inventory

BD0120: 18 containers / 56 item records. BD0130: 35 containers / 78 item records. Loose gold in containers totals **4,161 gp** (MISC07 stacks: 221+206+147 / 3,000+267+171+112+37).

### UNIQUE / QUEST items in containers (full detail)

| resref | name | where (area/container @x,y) | class | elsewhere in game* | re-home priority |
|---|---|---|---|---|---|
| BDSHSARE | Page from Sarevok's Notes | BD0130/Table_sarevok @2729,2536 (secret library) | QUEST (cross-chapter) | **nowhere else** | **P1 — must** (sets `BD_SAREVOK_SECRET=1` in BD0130.baf:374-381; resolved in **BD7230.bcs** masks-room, journal QUEST_DONE 266956) |
| BDSHBHR | Bhaal Research | BD0130/Table_korlasz @1698,659 (bedroom) | QUEST (story premise) | nowhere else | **P1 — must** (the papers Duke Jannath sent Imoen for; handed to Imoen post-boss, `TakePartyItem` BDIMOEN.d states 31/36) |
| BDSW2H03 | Sword of Ruin +2 | BD0130/Chest_secret01 @2588,2759 (lock 90, trapped) | UNIQUE weapon | **nowhere else** | **P1 — must** |
| BDHELM10 | Helm of Unwavering Purpose | BD0130/Chest_secret02 @2603,2687 (lock 90, trapped) | UNIQUE armor | **nowhere else** | **P1 — must** |
| BDMISC13 | Cobalt Moss | BD0120/Sarcophagus4 @468,997 (trapped) | QUEST (Ammon sidequest) | nowhere else | **P1 — must if Ammon quest ported** (BDAMMON.d:137-162: turn-in → he gives his `wand10` + `AddexperienceParty(3000)`, BDAMMON.d:268-269) |
| BDSHKORJ | Korlasz's Journal | BD0130/Table_korlasz @1698,659 | UNIQUE lore | nowhere else; no script/dlg refs | P2 |
| BDSHKORO | Orders from Korlasz | BD0120/Jackpot chest @1911,1370 | UNIQUE lore | nowhere else; no script/dlg refs | P2 |
| BDSHPAM1 / BDSHPAM2 | Crusader Pamphlet ×2 | BD0130/Table_library @2826,1008 / Table_machine_room @515,1148 | lore + flag | nowhere else | P2-P3 (sets `BD_PAMPHLET_RESPONSE=1`, BD0130.baf:383-391; read only by **BDFF1001.dlg** — the dungeon's own Fist escort → dies with dungeon) |
| BDSHSTF1 | Wooden Staff | BD0130/Body_cave pile @3242,1262 | QUEST (Restless Spirit) | nowhere else | P2 — port quest wholesale or cut (see §4.6) |
| BDSHSTF2 | Ornate Headpiece | BD0130/Chest_war_room01 @1005,273 (lock 75, trapped) | QUEST (Restless Spirit) | nowhere else | P2 (pair with BDSHSTF1) |
| BDBOOK02 | Kanaglym: The Abandoned City | BD0130/Bookcase_secret02 @2704,2410 | lore (foreshadows BD4100 keep-era content) | nowhere else | P2 |
| BDBOOK04 | The Nine Hells | BD0130/Bookcase_secret01 @2529,2547 | lore | 1 other area | P3 |
| BDTORCB | Burned-Out Torch | BD0130/Torch container @2176,2510 (trapped) | PUZZLE (brazier/secret-door) | nowhere else | dies with dungeon (see §4.7) |
| BAG02I | Gem Bag | BD0120/Jackpot chest @1911,1370 | QoL container | 0 in override scan (biffed BG2 resource; gem bags exist in BG2 stores) | P2 — early gem bag is real QoL |
| CDIA525 | Shroud of Flame (scroll) | BD0130/Bookcase_secret02 — **script-injected by IWDification** (BD0130.baf:1734-1740, `cd_iwdification_add`) | mod-added scroll | sold in 4 stores | P3 (purchasable; note mod-compat) |

*"elsewhere" = scan of ALL override .are container items (1,061 areas), ALL 9,598 .cre inventories, ALL .sto sale stocks. Caveat: pristine-biffed base-BG2 resources aren't in override, so BG2-only copies of generic base items may be undercounted; irrelevant for all BD-prefixed resrefs (SoD content is fully loose in override).

### Notable-but-replaceable container items (exist elsewhere / purchasable)

| resref | name | where | elsewhere | priority |
|---|---|---|---|---|
| WAND05 | Wand of Fire (5 ch.) | BD0130/Sarcophagus_brazier_room @2965,1905 | 2 areas, 16 stores | P3 |
| WAND11 | Wand of the Heavens (5 ch.) | BD0130/Sarcophagus_myrkul_room @734,1514 | 3 areas, 11 stores | P3 |
| MISC07 ×3000 | Gold | BD0130/Chest_korlasz @1733,628 (lock 95, trapped) + SCRL6O (Secret Word), SCRL2D (Summon Shadow), AMUL12 (Laeral's Tear) | gold/scrolls common | P3 (the 3,000 gp is the dungeon's cash jackpot — fold into re-homed reward) |
| AMUL11 | Pearl Necklace | BD0120/Sarcophagus2 | 18 areas | GENERIC |
| SCRL75, SCRL04, SCRL08, SCRL58, SCRL5F, SCRL6L, SCRL10/11/14 (cursed), SCRL1J | spell/cursed scrolls | various shelves | all in 2-35 stores | GENERIC |
| POTN02/03/05/08/10/11/14/17/21/24/25/32/52 | potions | various | ubiquitous | GENERIC |
| RNDGEM01/02, RNDSCR04/05, RNDMAG03/06, RNDTRE06/07, RNDTRI01-03, RNDARO01, RNDPTN01, DW#RND03 | random-treasure placeholders (engine rnd tables; DW# = SCS) | various | system-wide | GENERIC |
| BOOK32/37/43, MISC50 (Skull), MISC56_ (Broken Weapon), MISC58 (Broken Armor), MISC61 (Wine), MISC25 ×10 (Zircon), MISC43 (Emerald) | mundane/flavor | various | common | GENERIC |
| Weapon_rack01-05, Armor_storage (BD0120 @747-881; BD0130 @1521/1734) | ~40 mundane weapons/armor (SW1H01…, CHAN01…, PLAT01, BOW03…, HELM01/10, BDHELM08, BDHELMJ3, SHLD*) | racks/chest | all common | GENERIC (drop with dungeon) |
| PLAT04 | Full Plate Mail | BD0130/Chest_secret02 | 2 areas, 16 stores, 137 CREs | P3 (strong for tier; optional) |
| CHAN05 | Splint Mail +1 | BD0130/Corpse_brazier_room1 | 4 areas, 21 stores | GENERIC |
| SHLD17A | Buckler +1 | BD0130/Corpse_bane_room1 | 1 area, 5 stores | GENERIC |
| BLUN07 | Morning Star +1 | BD0130/Body_cave | 29 stores | GENERIC |
| **Imoen_import_eq** | (empty, invisible container @92,1098 BD0120) | — | — | **P1 mechanic** (§4.3) |

## 2. Carried loot (placed actors; droppable = not flagged `undroppable`; CRE item flags at CRE V1.0 items-offset 0x2BC struct +0x10)

Named/lieutenant carriers:

| carrier (CRE) | where | droppable items of note | class/priority |
|---|---|---|---|
| **BDSHKORL** "Korlasz" (the actual boss CRE on BD0130; dlg BDKORLAS, deathvar BDKORLAS — note: `bdkorlas.cre` is the separate neutral surrender-clone placed in BD0116) | BD0130 | **BDSHKEY Korlasz's Key** (opens Korlasz_bedroom door, lock 100), CLCK01 **Cloak of Protection +1** (biffed base item), CLCK12 Knave's Robe, BDBRAC13 Bracers AC 6, STAF02 Quarterstaff +1, DART02 ×80, SCRL6H/SCRL1Z/SCRL3G (consumed by her AI: BDSHKORL.baf:101/175/231 DestroyItem on cast), POTN21, DW#RND03 (SCS random) | P1 as a bundle if she's rebuilt as boss: this IS the boss-kill reward. **On surrender no item transfers** (BDKORLAS.d:112-140 sets `BD_KORLASZ_SURRENDER=1`, +1000 party XP, journal; no GiveItem/Drop) — surrendering forfeits her loot AND BDSHKEY (bedroom then needs 100 lockpicking) |
| **BDPORIOS** "Porios" | BD0120 | **BDKEY05 Tomb Key** (required by Plot_door BD0120, lock 96; also gated in BDPDOOR1.baf:18-51), **BDCLCK06 Cloak of Minor Arcana** (unique, nowhere else), DAGG05 ×20 | P1 for BDKEY05-equivalent gating only if a door survives; BDCLCK06 P2 unique. Surrender: `GiveItem("BDKEY05",Player1)` BDPORIOS.d:207/213 — cloak stays on him and is lost unless he's killed |
| **BDAMMON** "Ammon" (neutral alchemist) | BD0120 | WAND10 Wand of Monster Summoning (3 ch.) — also his quest reward (he hands over the carried wand), DART04 ×20, DART02 ×40, POTN10, DW#HASPT (SCS) | P1 with the Cobalt Moss quest (wand + 3,000 party XP) |
| BDKORDE4-9, BDKORDEO (surrender-variant followers), BDSHIS01-10, BDSHME01-03, BDKORME1-9 (elites) | both | generic magical consumables/ammo: AROW05 ×10 Arrow of Biting, AROW02, DART03 Stunning ×10-20, DART04 Wounding, **DART11 Dart of Acid +1 ×20** (only 6 CREs/2 stores game-wide), POTN08/10/14/24/52, RNDTRE06/randoms; mundane armor mostly `undroppable` on the KORDE (neutral) variants; SW1H48 Ninjatō, SW1H43 Katana, HELM13 | GENERIC/P3 — nothing unique; total is a modest consumables economy that vanishes with the trash cut |
| BDFF1000-1002 (allied Fist escort) | BD0120 | POTN08 ×5, POTN20, POTN52 ×3, WAND11 (3 ch.), HAMM02, CHAN05, SHLD04A | allies, leave via rope with Imoen (BDIMOEN.d:311-314) — not player loot |
| Undead trash (BDSKGR00-07, BDSHAD04, BDWIGHT1-3, BDWRAI02, BDMUMM01, GHAST, BDBONBAT, BDSHZOM1, BDSHSOUL, BDUNSLGU, BDGHASTG) | BD0130 | only system items (RING94/95, IMMUNE1, attack .itms, HELMNOAN — all `unstealable|undroppable`) + generic droppable weapons/ammo (SW2H01, AX1H01, BOW03, AROW08/09 few) + RNDTRE08 randoms | GENERIC — zero unique loss from cutting them |

## 3. Script-granted items (all VERIFIED, file:line)

1. **BD0120.baf:600-627 first-entry block (`BD0120_START`)** — campaign-start bootstrap: destroys MISC55 "Duke Eltan's Body" from all 6 party slots, full-heal/resurrect (`bdresurr`/`bdrejuve`), and `GiveItemCreate("BDKEYR",Player1)` — the SoD **Key Ring** (exists nowhere else). **P1: this block must move to the new campaign entry point.**
2. **BD0120.baf:641-649** — `GiveGoldForce(30000)` when `SOD_fromimport=0` (new-campaign chars only).
3. **BD0120.baf:845-3841 "gear script"** (~90 blocks, all gated `Global("SOD_fromimport","global",0)` + `BD_TURNOFF_GEARSCRIPT`) — grants new-campaign Player1 a proficiency-matched signature BG1 loadout: one weapon (Kondar/Albruin/Varscona/Burning Earth/Whistling Sword/Mauletar/Spider's Bane/Rashad's Talon/Ashideena/Suryris's Blade/Thresher/Krotan's Skullcrusher/Aule's Staff/Arla's Dragonbane/The Guide/Army Scythe/Dead Shot/Protector of the Dryads…), class armor (Archmagi robes/Ankheg Plate/Fallorain's/Practical Defense/Magma Bulwark/Karajah's/Shadow Armor), **Helm of Balduran** (:3201), **Cloak of Balduran** (:3338), Golden Girdle, Worn Whispers, Evermemory, Sandthief's Ring, potions, +1 fallbacks. **Dormant on this EET install** — `BDSODTRN.baf:8` sets `SOD_fromimport=1` — but P1 for fresh-start compatibility: relocate with the new start.
4. **Imoen import-equipment flow (P1 mechanic)**: BD0120.baf:651-663 — on import with IMOEN2 in party: `ActionOverride("Imoen_import_eq",TakeCreatureItems("IMOEN2",ALL))` then Imoen leaves+DestroySelf; **BD0103.baf:128** later runs `MoveContainerContents("BD0120*Imoen_import_eq","BD0103*Imoen_equipment")` — her BG1 gear becomes retrievable in the palace guest floor. If BD0120 is bypassed, this pair must be re-wired or imported-Imoen gear is silently lost.
5. **Dungeon-exit gold impound**: BDCUT00Z.baf:20 `TakeObjectGoldGlobal("BD_TAKEN_GOLD","GLOBAL",Player1)` — ALL party gold impounded at exit; returned only in **BD4100** (Dragonspear Castle Keep 1F) Gold_Chest with Note BDMISC42, `AddGlobals("BD_TAKEN_GOLD","BD_EXTRA_GOLD")`, or flat 2,000 gp if Ophyllis subplot failed (BD4100.baf:553-580). Any dungeon-removal must keep or consciously redesign this economic reset.
6. **Restless Spirit sidequest (self-contained)**: opening Sarcophagus_spirits_room spawns BDSPIRIT (BDSHSARS.baf:1-14); placing BDSHSTF1+BDSHSTF2 inside destroys both and `CreateItem` **MISC28 Waterstar ×10, MISC32 Shandon ×8, MISC39 Water Opal ×5** (BDSHSARS.baf:16-31); journal wiring BD0130.baf:393-474 (`BD_SDD016`, entries 264311-15/270023-25).
7. **Brazier/torch puzzle**: BDSHTORC.baf:37/57 `CreateItem("BDTORCB")`; BDSHBRZ.baf:50-100 swaps BDTORCB↔BDTORCY/R/P (lit torch colors) — opens the secret library (Secret_door, flags 0xA2). Items BDTORC* are dungeon-internal; die with the dungeon unless the puzzle is ported.
8. **BDCUT02.baf:20** gives BDMISC56 "Parchment" to BDGASS2 — palace assassination, not dungeon.

## 4. Special mechanics / cross-references summary

- **Cross-chapter thread (highest-value find)**: BDSHSARE → `BD_SAREVOK_SECRET` → **BD7230** masks-puzzle quest completion. Removing the dungeon without re-homing this item strands a chapter-10 quest resolution.
- **BD_SAREVOK_SWORD rumor thread**: set/read only in BDPORIOS.dlg + BDIMOEN.dlg (sentry shouts about a sword "already gone"; Imoen comments) — pure dungeon-internal flavor, safe to drop.
- **Post-boss XP**: Imoen's wrap-up dialog gives **5,000 XP × 6** (BDIMOEN.d:303-308) — attached to dungeon completion, not to any item (BDSHBHR handover is inside the same conversation but only TakePartyItem). Budget this into the chapter-pass XP re-weighting.
- **Korlasz surrender vs kill**: surrender = +1,000 party XP, journal, and forfeits her entire droppable kit incl. BDSHKEY (BDKORLAS.d; no item actions anywhere in the dlg).
- Rest-ambush skeletons (BDSKGR02/00/04 table, day/night 6, diff 80) carry only generic weapons/ammo — no loot argument against the planned rest softening.

## 5. Appendix — out-of-complex areas (do NOT need re-homing in the prologue pass)

- BD0113 (→BD5100): Niche: BDBOOKNJ "Journal of Ithtaerus", OHRGEM01 "Shadow Gem".
- BD0114 (→BD7200): BDSW1H22 "Severance +2" (Spidercove), BDLEAT02 "Goblin Hide Armor +2" (Goblincorpse), BDEGG01 Spider Egg ×5, POTN32, randoms.

## Tooling
Parsers written for this task (reusable): scratchpad `ieparse.py` (ARE V1.0 containers/actors/regions/doors, CRE V1.0 inventory+slots+flags, TLK, ITM, chitin.key/biff name resolution), `xref.py` (whole-override item cross-reference; JSON at scratchpad `xref.json`). Decompiled dialogs (WeiDU v24600, scratchpad): BDKORLAS.d, BDPORIOS.d, BDAMMON.d, BDIMOEN.d.

## Verified facts
- Complex = BD0120 ⇄ BD0130 only: BD0120 travel regions go solely to BD0130 (TranBD0130, Tranbd0130rope) and vice versa; exit to palace is scripted (BDCUT00Z), verified from live .are region structs.
- BD0113 exits only to BD5100; BD0114 only to BD7200; BD0115 only to BD7000 — none are part of the Korlasz complex.
- The BD0130 boss CRE is BDSHKORL (dialog BDKORLAS, deathvar BDKORLAS); bdkorlas.cre is a separate neutral clone placed in BD0116 for the surrender scene.
- Complex-exclusive items (zero other copies in any override .are container, .cre inventory, or .sto stock): BDSHSARE, BDSHBHR, BDSW2H03 Sword of Ruin +2, BDHELM10 Helm of Unwavering Purpose, BDMISC13 Cobalt Moss, BDSHKORJ, BDSHKORO, BDSHPAM1/2, BDSHSTF1/2, BDBOOK02, BDTORCB, BDCLCK06, BDKEY05, BDSHKEY, BDKEYR.
- BDSHSARE sets BD_SAREVOK_SECRET=1 (BD0130.baf:374-381) which is consumed in BD7230.bcs (masks puzzle, journal QUEST_DONE 266956) — a cross-chapter dependency.
- Ammon sidequest: TakePartyItem bdmisc13 → GiveItem wand10 + AddexperienceParty(3000) (BDAMMON.d:137-162, 268-269).
- Imoen post-boss dialog grants 5000 XP to each of 6 party slots (BDIMOEN.d:303-308); BDSHBHR handover is TakePartyItem only, no XP delta and sets no global.
- Korlasz surrender path (BDKORLAS.d:112-140): BD_KORLASZ_SURRENDER=1, AddexperienceParty(1000), journal 259573; contains NO item transfer — her droppable loot (BDSHKEY, CLCK01 Cloak of Protection +1, CLCK12, BDBRAC13, STAF02, scrolls, POTN21, DART02×80) is forfeited on surrender.
- Porios gives BDKEY05 Tomb Key via dialog on surrender (BDPORIOS.d:207,213); BDKEY05 opens Plot_door in BD0120 (door key field, lock 96) and is checked in BDPDOOR1.baf; BDSHKEY opens Korlasz_bedroom door in BD0130 (lock 100).
- BD0120.baf:600-627 first-entry block gives BDKEYR Key Ring to Player1, destroys MISC55 Duke Eltan's Body from all slots, and full-heals/resurrects the party.
- BD0120.baf gear script (~lines 845-3841) and GiveGoldForce(30000) (:641-649) are gated on SOD_fromimport=0 (new-campaign only); BDSODTRN.baf:8 sets SOD_fromimport=1, so both are dormant on this EET install.
- Imoen import flow: BD0120.baf:651-663 strips IMOEN2's items into container Imoen_import_eq (BD0120 @92,1098, empty in .are) and removes her; BD0103.baf:128 MoveContainerContents to BD0103*Imoen_equipment.
- Gold impound: BDCUT00Z.baf:20 TakeObjectGoldGlobal(BD_TAKEN_GOLD) at dungeon exit; returned in BD4100 (Dragonspear Castle Keep 1F) Gold_Chest with BDMISC42 Note plus BD_EXTRA_GOLD, or flat 2000 gp (BD4100.baf:553-580).
- IWDification (cd_iwdification_add, BD0130.baf:1734-1740) injects CDIA525 Shroud of Flame scroll into Bookcase_secret02; the scroll is also sold in 4 stores.
- Restless Spirit quest: BDSHSARS.baf spawns BDSPIRIT on sarcophagus open; placing BDSHSTF1+BDSHSTF2 inside creates MISC28×10, MISC32×8, MISC39×5 gems and destroys the staff pieces.
- Torch/brazier puzzle items BDTORCB/BDTORCY/BDTORCR/BDTORCP are created/swapped by BDSHTORC.baf and BDSHBRZ.baf; puzzle opens the BD0130 secret library.
- BDSHPAM1/2 set BD_PAMPHLET_RESPONSE=1 (BD0130.baf:383-391), read only by BDFF1001.dlg (the dungeon's own Flaming Fist escort).
- Container gold in the complex totals 4,161 gp; the largest stack is 3,000 gp in Chest_korlasz (lock 95, trapped) together with SCRL6O, SCRL2D, AMUL12.
- BAG02I (Jackpot chest, BD0120) resolves via chitin.key/biff to 'Gem Bag'; CLCK01 on Korlasz resolves to 'Cloak of Protection +1'; MAGE01 (undroppable, on assassin-types) is Sandthief's Ring used as an equipped power.
- Korlasz's AI consumes her droppable scrolls when casting (BDSHKORL.baf:101/175/231 DestroyItem SCRL6H/SCRL3G/SCRL1Z).
- Undead trash on BD0130 carries only undroppable system items (RING95, IMMUNE1, attack items) plus generic droppable weapons/ammo — no unique loot is lost by cutting them.
- SCS mass-distribution items present: DW#HASPT on 1,203 CREs and DW#RND03 random-treasure on 138 CREs, including dungeon NPCs — generic.
- BDIMOEN.d:311-314: after the wrap-up, Imoen and BDFF1000-1002 EscapeAreaObject via the rope transition (Tranbd0120rope).

## Inferred (not directly verified)
- Re-home priorities (P1 must / P2 nice / P3 optional) are my classification, derived from uniqueness (zero other copies), quest wiring, and store availability — not from any in-game data field.
- The 'exists elsewhere' scan covers the override directory only (1,061 .are, 9,598 .cre, all .sto). Pristine-biffed base-BG2 resources are not scanned, so game-wide counts for generic base items (e.g. gem bags, common scrolls) are undercounts; this cannot affect BD-prefixed SoD resrefs since all SoD content is loose in override.
- BDSHKORO 'Orders from Korlasz' and BDSHKORJ 'Korlasz's Journal' appear to be pure lore: no .baf, .bcs, or .dlg in the install references them (searched all sod_baf + override DLG/BCS). Small chance a strref-level reference exists that a resref search cannot see.
- The 5,000 XP × 6 Imoen wrap-up is effectively the dungeon-completion reward and should be counted in the XP-economy budget when the crawl is removed.
- If Korlasz surrenders, the Korlasz_bedroom door can only be opened with 100 lockpicking (or Knock) since BDSHKEY is never transferred — I infer this is an intentional loot/mercy tradeoff, but it may just be an oversight in Beamdog's design.
- BDBOOK02 ('Kanaglym: The Abandoned City') foreshadowing of later SoD content is my reading of the title vs BD4100-era content; the book has no script hooks.
- DW#HASPT's display name resolving to 'Mirror' is almost certainly a strref quirk of the SCS-generated item; its exact function was not investigated (irrelevant: mass-distributed, generic).

## Design notes
- Minimum-loss re-home bundle if the crawl is cut entirely: BDSHSARE, BDSHBHR, BDSW2H03, BDHELM10, BDSHKORJ, BDSHKORO, BDCLCK06, BAG02I, the 3,000 gp jackpot, and Korlasz's droppable kit — all fit naturally into (a) a boss-kill drop if Korlasz is kept as a single set-piece, plus (b) one 'family vault' reward container, plus (c) Imoen/palace dialogue for BDSHBHR.
- The BD0120_START bootstrap block (Key Ring grant, MISC55 cleanup, party heal/resurrect) and the SOD_fromimport=0 branches (30k gold + gear script) must be moved to whatever area becomes the new campaign entry — they are start-of-SoD infrastructure, not dungeon content.
- The Imoen_import_eq → BD0103 Imoen_equipment pipeline must be re-wired if BD0120 is bypassed, or imported-Imoen gear is silently destroyed with her CRE.
- Decide explicitly whether to keep the BDCUT00Z full-gold impound: it is SoD's economy reset; if kept, the BD4100 Gold_Chest return needs no change (it reads the global, not the area).
- If Korlasz remains as the rebuilt boss fight: her surrender branch currently forfeits all loot — consider adding an item transfer (at least BDSHKEY-equivalent) so the mercy path isn't strictly punished, in line with the mod's 'meaningful fights' goal.
- The Restless Spirit quest (spirit + 2 staff pieces + gem payoff) and the brazier/torch secret-library puzzle are the two self-contained 'good content' nuggets of BD0130 — candidates for porting wholesale into whatever remains of the tomb rather than item-by-item re-homing.
- IWDification targets BD0130's Bookcase_secret02 by script; if the area stays reachable but emptied, its block still works. If the area becomes unreachable, no breakage occurs (scroll sold in 4 stores), but note it in the compat doc.
- Cutting all BD0130 undead trash loses zero unique items — only generic ammo/potion economy; supports the planned ~70% trash cut with no loot-table compensation needed beyond the uniques above.
