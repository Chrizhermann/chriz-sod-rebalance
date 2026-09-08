# Issue 16 — road-north filler audit

Static snapshot: **2026-09-07**, designated dev EET installation at
`C:\Games\Baldur's Gate II Enhanced Edition modded - dev eet install`.
Research only: no cuts, game changes, or new design decisions.

**All 132 exact component 230/240 cut-list entries are disabled as intended.**
That does not settle whether the cuts were safe or whether the chapter is fully
reviewed. Two findings need attention before another broad thinning pass:

1. The cut “stray wight” is **Ymori**, an actor still required by an existing quest
   activation and dialogue branch. The dependency is confirmed; the result of
   `Activate()` against his zero appearance schedule needs an engine test.
2. The retained Shadow Aspect can still **summon banned Shadowed Souls** on Insane.
   This is a missed route under the approved global removal policy.

Ambient spawn activation, most temple restructuring, and the substantial spider
cave remain **OPEN** work rather than failed implementations of the July cut lists.

## Evidence and counting rules

Decision sources: [chapter 9](../design/chapters/03-roadnorth.md),
[locked wishlist](../01-remix-wishlist.md), and the shipped
`comp230_lists.tpa` / `comp240_lists.tpa`. The July
[road census](13-roadnorth-census.md) is historical baseline data, not the current
installed state.

The shared effective-resource census supplies [areas](issue16/areas.csv),
[actors](issue16/actors.csv), [creatures](issue16/creatures.csv),
[creature items](issue16/cre_items.csv), [cut-key checks](issue16/cutlist_checks.csv),
[spawn points](issue16/spawn_points.csv), [regions](issue16/regions.csv), and
[rest headers](issue16/rest.csv). An independent check also passed all 132 road keys.
Fresh attached CRE scripts/dialogues and the relevant area/container scripts were
decompiled with dev WeiDU 246 from task-owned temporary working directories.

“Scheduled” means at least one of the low 24 hour bits is set. “Living hostile”
below additionally requires CRE allegiance >=200 and no CRE dead-state bit. These
are static placement counts, not simultaneous fight sizes: some neutral actors
turn hostile, some actors begin invisible, and scripts/difficulty can change the
encounter. None of these ten areas has an embedded actor CRE in this snapshot.

| Map | ARE rows / schedule-zero rows | Scheduled living hostile CREs | Classification and retained content |
|---|---:|---:|---|
| BD7100 — Troll Claw Woods | 172 / 63 | 40 | **Approved cut verified; explicit keeps.** 21 trolls, 10 ogres, 7 elite spiders, 2 boars remain. Camp/recruit/quest cast stays. Ambient activation is OPEN. |
| BD7110 — troll lair | 16 / 0 | 16 | **Explicit keep.** Fifteen trolls plus the Shamaness; no spawn points. The old “16 + boss” description overcounted by one. |
| BD7200 — Forest of Wyrms | 59 / 28 | 19 | **Approved cut verified; explicit keeps.** Thirteen wyverns, five phase/astral spiders, and the hill giant remain. Ambient activation is OPEN. |
| BD0114 — spider cave off BD7200 | 40 / 0 | 40 | **Unreviewed density; quest content present.** No 230/240 cut list covers it. Details below. |
| BD7210 — Morentherene | 1 / 0 | 0 initially | **Explicit kept set-piece.** The neutral sleeping dragon becomes hostile; native reinforcements and component 250's difficulty buffs remain. |
| BD7220 — bugbear cave | 37 / 0 | 36 on disk | **Removed by routing, not actor deletion.** No incoming travel region in the 76-area census; the two former entrances now connect BD7210 and BD7230 directly. Do not count these preserved files as surviving reachable filler. |
| BD7230 — Cyric temple | 55 / 6 | 18 | **Six ambushers correctly cut; broader reshape OPEN.** Forty-nine scheduled rows include nine corpses and one target dummy, not 49 fighters. Shadowed Soul exception below. |
| BD2000 — Boareskyr Bridge | 151 / 8 | 26 initially | **Eight cuts applied; Ymori quest risk.** Siege pickets and the neutral-to-hostile battle are explicit keeps. Barrel replacement belongs to #14. |
| BD2010 — goblin warren | 39 / 27 | 8 | **Approved cut verified; core explicitly kept.** Chief, witch doctor, three warriors, three elites: 885 nominal kill XP. The ninth EA255 row is a dead dog, not an extra fight. |
| BD2100 — Bridgefort | 41 / 0 | 1 initially | **Quest/recruit hub kept.** The initial invisible wraith and Junia's dialogue-created wights are quest encounters, not evidence of an overlooked ambient pack. |

The exact cut checks are BD7100 **63/63**, BD2000 **8/8**, BD2010 **27/27**,
BD7200 **28/28**, and BD7230 **6/6**. There are no unmatched, duplicate, or still
scheduled keys in those lists.

## RN-1 — Ymori was cut as filler but remains in Tender of the Dead

**Classification: confirmed quest dependency of an applied cut; runtime consequence
unresolved.** Component 230 targets `BDYMORI@4089@408`, ARE actor index 1, and writes
its appearance schedule to zero. The source list calls this a 175-XP wight. The
CRE's actual death variable is `BDYMORI`.

The effective chain is still present:

- BD2000 container index 0, `Ymoribody`, has `BD2000YM` as its script at entry +0x48.
- `BD2000YM.BCS` creates `BDBODY04` when `BD_SDD222>3`; opening/clicking the body
  advances `BD_SDD222_YM` to 2. Its next block disables the body container,
  **activates `BDYmori`**, creates **six `ZOMBIE`**, and advances the local state to 3.
- Junia dialogue state 30, entered at `BD_SDD222=5` / `BD_SDD222_PERP=1`, gates both
  “found Ymori” confrontation replies on `Dead("bdymori")`. These lead through
  states 32–34 to exposing Junia. State 33 also tests possession of `BDYMORI`.
- The alternative direct accusation at Junia state 28 remains. This is therefore
  **not a demonstrated whole-quest hardlock**. State 28 or 34 creates three
  `BDWIGHTJ` at the altar; those are alternative branches, not six wights in one run.

The removed actor also carries these identifiable quest belongings in the current
CRE. Numeric flags are preserved here; their presence in a CRE is not proof of a
completed runtime drop:

| Item | Effective name | Instance flags | Charges |
|---|---|---:|---|
| BDAMUL10 | Kendra's Chain | 0x00000002 | 0 / 0 / 0 |
| BDSW1H09 | Herdrin's Short Sword +2 | 0x00000002 | 0 / 0 / 0 |
| BDYMORI | Ymori's Head | 0x00000003 | 0 / 0 / 0 |

The remaining CRE inventory is `RING95`, `IMMUNE1`, `WIGHT`, and `RNDTRE08`.
Kendra's/Herdrin's returns and Tharantis/Junia dialogue must be considered before
calling this actor expendable. None of these dependencies was retired by 230.

**Recommended next check:** stage the body-interaction branch on a fresh BD2000,
then verify whether the scheduled-out actor can actually be activated, killed,
and looted and whether Junia's confrontation remains available. Do not infer the
answer merely from the presence of `Activate()` or from the installed cut count.
If suppression is confirmed, the narrow repair is to preserve this existing quest
actor and its belongings, while reconciling its **175 XP** already included in the
230 removed-XP basis. Retiring the whole quest would require a separate design
decision; it is not part of the approved trash cut. No repair or ledger change is
made by this audit.

## RN-2 — Shadow Aspect retains a banned summon route

**Classification: missed approved global policy, not a failed 240 cut key.** The
wishlist's July 8 direction removes `BDSHSOUL` from every SoD area. BD7230 still
contains scheduled actor index 24, `BDASHIRU` / Shadow Aspect. Its CRE is alive,
EA255, has default script `BDASHIRU`, and no actor script override replaces it.

In the effective `BDASHIRU.BCS`, the block beginning at decompiled line 57 checks
`!STATE_INVISIBLE`, `Difficulty(HARDEST)`, an expired/not-running local `bd_summons`
timer, and a seen enemy. It sets the timer to `TEN_ROUNDS`, applies Shadow Door and
Darkness, and creates **two `BDSHAD04` plus two `BDSHSOUL`**. There is no once flag;
another eligible timer window can run the block again. Earlier invisibility logic
and combat state affect whether it actually fires, so this audit establishes a
live static route, not a measured frequency of summons.

Each effective Shadowed Soul has **1,100 nominal kill XP** and carries only
`IMMUNE1`, `RING95`, and `S1-12M2`, each with instance flags `0xA`; no named quest
belonging was found on that template. The existing fixed 240 ledger covers placed
cuts and BD7220, not these combat-dependent repeated summons. Their variable
quantity must not be silently treated as a fixed two-creature XP deduction.

The narrow policy follow-up can remove the two banned creation actions while
preserving the Shadow Aspect encounter and unrelated shadow summons. Any new
replacement creature or broader fight redesign remains a separate decision.

This also corrects the historical road census's “arc is CLEAN” statement: its
placed/rest/spawn-table screen did not cover this attached creature script.

## RN-3 — ambient activation is still present, by the old pass's scope

**Classification: OPEN keep/cut treatment.** The chapter document explicitly says
ambient respawns were left out of the quick-win pass. Initial `enabled=0` does not
mean the spawn table has been removed.

| Map | Points and creature tables | Effective activation path |
|---|---|---|
| BD7100 | 9: Spiders01/02 → BDSPIDGI/BDSPIDHU; Wolves01 → BDWOLF/BDWOLFDI; Hobgoblins01/02 → BDHOBG02/BDHOBG05; Trolls01/02 → TROLL01; Boars01/02 → BDBOAR02/BDBOAR01 | `BD_SPWN_ACTIVE` 0→1 deactivates all; state 1 with no ENEMY allegiance in area→2 starts ONE_DAY; expiry→3 activates all. |
| BD7200 | 4: Wolves → BDWOLF/BDWOLFDI; Boars → BDBOAR02/BDBOAR01; Wyverns → BDWYVR01/BDWYVR02; Spiders → BDSPIDGI/BDSPIDHU | Same 0→1→2→3 chain after the area has no ENEMY allegiance. |
| BD2000 | 4: Wolves01 → BDWOLF/BDWOLFDI; Beetles01 → BDBEETBH/BDBEETMH; Spiders01 → BDSPIDGI/BDSPIDHU; Bears01 → BDBEARBL/BEARBR | Same chain, with state 1 additionally requiring `BD_SPWN_OVERRIDE=0`; the area releases this siege override at plot >=295. |

All 17 points have nonempty tables, a 24-hour schedule, initial enabled 0, day/night
fields 20/20, and EE frequency field 7200. The configured maximum is six except
BD7200 Wyverns (four) and BD2000 Bears01 (one). Some table weights are zero; retain
the raw values in [spawn_points.csv](issue16/spawn_points.csv) rather than guessing
their runtime consequences.

These scripts **arm once**: no reset from state 3 was found in their effective area
scripts. Repeated generation after activation is an engine spawn-system question,
not proof of a repeating script loop. A timed clear/leave/revisit test is still
needed to establish actual packs and frequency. The activation paths can restore
small spiders, hobgoblins, or beetles despite the placed-actor cuts, but no further
removal was previously approved. Their XP is variable, not another known fixed
placed-kill chunk.

Rest and travel encounters are separate systems. BD7100 and BD0114 retain rest
day/night fields 1/2; the other rest-enabled maps here use 1/1. BD7210's table is
empty and its NOREST gate depends on the dragon encounter; BD2100 has no configured
rest pack. The area scripts also retain URE travel-launch branches: BD7200 alone
can queue BD0064, BD0060, or BD0066 with individual global flags and the shared
eight-hour timer. Those arenas belong to the campaign travel audit, not an
additional placed-actor count for BD7200.

## RN-4 — temple/Ziatar recomposition remains a design task

**Classification: OPEN; six explicitly rejected ambushers correctly removed.** The
six `cultist_ambush1..6` placements have schedule zero. `BD7230AM` does not create
them: it requires the named actor to be alive and neutral, then makes it invisible
and jumps it into position after the Neothelid dies. No recreation of those named
actors was found in the reviewed area/region/attached scripts. Old saves with
baked actors are a separate runtime case.

The remaining temple is not simply “~40 parley cultists.” Its 49 scheduled rows are:

- **18 initial hostiles:** Neothelid; Darskhelin; Shadow Aspect; two umber hulks;
  three invisible stalkers; four enthralled cultists; three mutated crawlers;
  three worgs. Their nominal kill XP totals **60,510**.
- **21 living neutrals:** thirteen cultist/guard/enforcer/mage/mad-cultist rows;
  two named Neothelid scene actors; Ziatar, Akanna, Madele; Keherrem and two crusader
  prisoners. Their neutrality is not a promise of a peaceful route.
- **Nine dead cultist props and one bookshelf target.** They are not ten additional
  fights or guaranteed kill-XP sources.

Ziatar's current dialogue ends in combat: state 3 uses `Enemy()`, `Shout(ALERT)`,
and unlocks/opens Door07; state 5 also uses `Enemy()`. Her 3,000-XP CRE carries
**BDKEY11 (Jail Key)** and **BDKEY12 (Ritual Room Key)**. Generic `BDCULT` scripts
turn neutral cultists hostile when Ziatar ceases to be neutral or dies; their
non-ambush escape block is instead keyed to Darskhelin's death.

Akanna carries **BDMISC51 (Wardstone)**. Her dialogue is hostile if Darskhelin is
alive; after his death it can offer a reward and hand over the wardstone. If she
turns hostile while alive, the area script creates aerial servants once: one at
EASY, two above EASY. Keherrem's prison dialogue requires BDKEY11 and feeds the
missing-patrol/Kharm route. Madele and the Neothelid prey/escape actors have their
own dialogue or scene roles. They cannot safely be grouped with anonymous filler
without deciding which quest/scene survives.

Container rewards remain: Table_01 holds Ziatar's/Akanna's journals, Chest_01 the
parchment, and Chest_02 **Godsbane and Fractal Blade +3**. The Neothelid's death also
remains the **once-only 22,700 party-XP compensation carrier** for component 240.
A future “one big Ziatar fight” design must explicitly preserve or relocate the
keys, wardstone/prisoner route, chosen loot, and this ledger trigger. These are
recomposition constraints, not evidence that an already-approved Ziatar redesign
failed to install.

## RN-5 — the reachable spider cave was outside the chapter cut lists

**Classification: unreviewed density; OPEN.** BD7200's `Trans_bd0114` leads to
BD0114, with a return to BD7200. Its prologue-looking resource number obscures its
actual road-north location. It is neither the removed BD7220 cave nor skipped
content.

All **40 spiders / 47,515 nominal placed kill XP** remain: eleven small, eight giant,
eight sword, six phase, two astral, two wraith, two gargantuan, and the named
seven-legged spider. `BD0114.BCS` adds **two SPIDPHAS** once at difficulties above
NORMAL; those are another 8,000 nominal XP, not included in the placed total.

`BDSPID7L` is Neera's seven-legged-spider objective. The area checks her quest state,
announces the target, and asks for its leg after death. Region/area logic also
supports spider eggs and a rhinoceros-beetle interaction. A focused thinning
proposal should preserve those selected quest objects and interactions; this audit
does not authorize eliminating the cave or its whole spider roster. The root audit
also tracks the historical XP-rationale overlap that mistakenly classified this
reachable area as skipped, without changing the approved prologue award.

## Preserved loot, progression, and recruitment boundaries

- **Troll Claw/cave:** Glimmer of Hope +2 remains in its BD7100 named container;
  BD7110's Locket of Embracing and its existing loot remain. Camp cast, Soralis's
  golem, the Irregulars, chapter-entry XP, and companion relocation scripts are
  not trash candidates merely because they create creatures.
- **Forest/dragon:** BD7200's Stalker Gauntlets and BD7210's Sable Cloak remain in
  containers. Morentherene's native once-only reinforcements are two greater
  wyverns on NORMAL, three plus one young dragon on HARD, five plus two young
  dragons on HARDEST. These are part of the deliberately kept encounter.
- **Bugbear cave:** surviving BD7220 actors, Greater Shadow/spectacles logic, and
  cultist staging are unreachable through the audited area graph. The preserved
  resource file is not an instruction to delete its contents. The modified
  `TranBD7220` names still let the temple's escaping cultist use the direct route
  to BD7210.
- **Bridge/fort/warren:** Vichand's feather/scroll stash, the Troll-Tender's Journal,
  and BD2010's Circlet of Lost Souls remain. Keep Khalid/Neera/Voghiln and the
  Bridgefort dialogue/quest machinery. The bridge-resolution
  `CSR_RN_CHUNK` block still pays **23,200 party XP once** at plot >292. The larger
  siege and barrel finale are separate approved-keeps/#14 design work.

## Reproduction and limits

Ignored local evidence is at `research/data/issue16-audit/roadnorth/`: 39 raw resource
snapshots, selected fresh BAF/DLG decompiles, `details.json` (including item flags and
the 132 checks), and `source-manifest.json` (full paths, sizes, SHA-256, timestamp).
The final census BAFs are in `research/data/issue16-audit/census-v3/baf/` and
`census-v3/baf-created-cre/` (the earlier snapshot has the same effective bytes
for the road resources cited here).
These raw game resources stay outside Git; committed CSV metadata and this report
are the portable evidence index.

Key SHA-256 values pin the two actionable findings:

| Resource | SHA-256 |
|---|---|
| BD2000.ARE | `7c3fb9b43af617ce68f92b75a801a0187761098c6501a4e0a645096b355db7be` |
| BD2000YM.BCS | `ecd27b12997d8b1c984cc4b0cf2643f870bdb770ee0e459de075d670adc74a9e` |
| BDYMORI.CRE | `4b6a488aa5f63cce7a25aa5f43905cc8d627709e17a6d15d5b17fa6c2c87f4e3` |
| BDJUNIA.DLG | `30232bea864e3849a96328a15ab0349ac62f4d4455be7f3fd4f3df57891fb570` |
| BD7230.ARE | `89a513ce5818b5f348b7284a79cfb37a241dff7b455ea9948fb4ada2471ea626` |
| BDASHIRU.CRE | `99c4aad084704b02f4503f06dcddcc413d9a6b83ecddef6d2593eba79bbc3009` |
| BDASHIRU.BCS | `4a25a3bafee263ca9665e566dc9f3c8069325ec294e7568d048517aee2cfff1d` |

This is one modded EET installation, not a vanilla or standalone compatibility
claim. No runtime encounter, schedule/Activate test, elapsed-time respawn test, or
save-baked actor check was performed. Attached BCS/DLG literal creation and quest
paths were reviewed; this is not an exhaustive expansion of every summoned spell,
random-creature group, item effect, or third-party dynamic script switch. Quest
item names/flags describe the effective templates, not verified loot collection.

Before changing counts, first resolve the Ymori quest risk and the banned summon
route. Then take the temple, spider cave, and ambient activation findings to
keep/cut/consolidate triage with explicit XP and quest ownership.
