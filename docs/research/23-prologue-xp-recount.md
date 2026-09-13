# Prologue XP recount and Ymori staging evidence

**Research date:** 2026-09-08. **Scope:** effective dev EET resources, read only;
research baseline `dbe9e1c`, before the pending issue #16 follow-up is installed.
This document records evidence and candidate accounting scenarios against the
then-installed **24,000 XP per character** baseline.

**Subsequent user decision, 2026-09-08:** use a flat **22,000 XP per character on
every difficulty**. The user explicitly rejected difficulty-scaled quest rewards.
Fresh component 175 uses the chosen amount; tail component 176 updates older
installations. The scenarios below remain research evidence, not an automatic
formula for the reward. Other approved chapter compensation remains unchanged.

## 1. What the old calculation got wrong

The historical [prologue ledger](../design/chapters/01-prologue.md)
counts **147,980 party XP** as guaranteed removed content. It includes BD0113
(5,600) and BD0114 (47,515), although these are still reachable from BD5100 and
BD7200 respectively. Removing just that classification error gives:

`147,980 − 5,600 − 47,515 = 94,865 party XP = 15,810.83 per character at six.`

That is a correction to the old arithmetic, **not a final replacement award**.
The old ledger also:

- sums difficulty-exclusive ARE actors together and calls the result Normal;
- omits initially neutral guards whose defeat or surrender can award creature XP;
- calls Ammon's 3,000 XP guaranteed, although it requires endorsing her letter;
- misses optional coffin, region and creature-script encounters and quest awards;
- estimates replacement combat instead of using its actual CRE XP values;
- omits the original prison rematch when comparing a surrender route.

The old optional **8,000 XP from phase spiders** is also in retained BD0114
(`BD0114.baf:9–14`), not in the skipped dungeon. Neither retained cave nor those
spiders belongs in compensation for the dungeon skip.

## 2. Units and scope of the recount

All creature and quest numbers below are **party XP** unless explicitly marked
per character. `AddExperienceParty` and `AddXPWorth` distribute XP among living
party members; the Imoen and Liia actions instead name Player1 through Player6
individually. The [IESDP action reference](https://gibberlings3.github.io/iesdp/scripting/actions/bgeeactions.htm)
documents these action units. `AddXPWorthOnce(Myself,TRUE)` is counted once per
creature, not again as a separate kill award; its `ClearStat` variant is marked
untested in IESDP, so the surrender figures remain static source evidence.

The difficulty labels here are the **literal engine identifiers**, not UI labels:
installed `DIFFLEV.IDS` contains `1 EASIEST`, `2 EASY`, `3 NORMAL`, `4 HARD`,
`5 HARDEST`, matching the [primary identifier reference](https://gibberlings3.github.io/iesdp/files/ids/bgee/difflev.htm).
In particular, `NORMAL=3` must not be casually described as the UI's Normal
setting. This audit did not use the native UI to check its labels or SCS settings.

The comparison asks what a defined, six-living-member playthrough of the skipped
BD0120/BD0130 content could award, then subtracts the replacement jailbreak.
It is a counterfactual resource ledger: component 140 makes the dungeon
inaccessible and sets surrender globals in the actual remix. It is not a live
measurement of visiting those areas with component 140 active.

## 3. Placed encounters, with difficulty gates applied

Fresh reads of BD0120's 25 and BD0130's 118 ARE actors matched the corresponding
143 rows in [actors.csv](issue16/actors.csv) for area, index, CRE, XP, allegiance,
state, schedule and difficulty-script slot. All are scheduled. The raw initial
hostile totals are 4,150 and 55,215, but those include mutually incompatible
difficulty placements.

The actor-specific gate scripts each contain a single `DestroySelf()` block:

| Attached script | Removal condition | Retained at DIFFLEV |
|---|---|---|
| BDLNORM | `DifficultyLT(EASY)` | 2–5 |
| BDLCORE | `DifficultyLT(NORMAL)` | 3–5 |
| BDLHARD | `DifficultyLT(HARD)` | 4–5 |
| BDLINSA | `DifficultyLT(HARDEST)` | 5 |
| BDHEASY | `DifficultyGT(EASIEST)` | 1 only |

The historical BD0130 total includes a 65-XP BDHEASY skeleton together with its
higher-difficulty replacements. Even DIFFLEV 5 therefore has **55,150**, not
55,215, initially hostile XP.

| DIFFLEV | BD0120 initially hostile: count / XP | BD0120 Porios group: count / XP | BD0130 initially hostile: count / XP | BD0130 initially neutral mercenaries: count / XP | Combined placed XP |
|---|---:|---:|---:|---:|---:|
| 1 EASIEST | 6 / 2,220 | 6 / 1,875 | 29 / 11,440 | 8 / 1,900 | **17,435** |
| 2 EASY | 6 / 2,220 | 6 / 1,875 | 30 / 12,025 | 8 / 1,900 | **18,020** |
| 3 NORMAL | 9 / 3,170 | 7 / 2,375 | 52 / 26,125 | 8 / 1,900 | **33,570** |
| 4 HARD | 11 / 3,800 | 8 / 2,775 | 67 / 39,725 | 8 / 1,900 | **48,200** |
| 5 HARDEST | 12 / 4,150 | 9 / 3,075 | 80 / 55,150 | 8 / 1,900 | **64,275** |

These rows exclude Korlasz herself, Ammon, the Fist helpers, decorative animals
and corpses. The eight neutral beetles are handled separately below. BDKORME8/9
are already initially hostile and are not counted again in the neutral column.

This is a **clear-all-eligible-encounters basis**, not an unavoidable award.
`BDSHSURR.baf:9–49` awards creature worth when eligible humans flee or undead die
on surrender. It requires active actors in the active area; its first block
destroys inactive actors without awarding XP. `BDKORME1.baf:48–53` separately
awards the two 400-XP escaping mercenaries. `BDSHKFIN.baf` turns Korlasz's
remaining guards hostile when her fight starts. These explain why initial
allegiance alone is insufficient and why an actual route can yield less.

## 4. Boss, exit and optional awards

Korlasz's dungeon CRE (`BDSHKORL`) is worth **2,500**. Surrender retains that
worth through `BDSHKORL.baf:54–63` and adds **1,000 party XP** through BDKORLAS
dialogue states 10/11. The four installed action copies include alternative
interjection branches; they are not four cumulative rewards.

Imoen's BD0130 exit conversation, state 32, awards **5,000 to each of Player1–6**
(`BDIMOEN.d:303–308`). Its root accepts Korlasz dead or surrendered. The preceding
book-return response is optional; the 5,000 each is not conditional on choosing it.

Optional additions below use each encounter once and require the relevant
interaction. Peaceful and hostile resolutions of the same NPC are alternatives.

| Optional content | DIFFLEV 1–2 | DIFFLEV 3 | DIFFLEV 4 | DIFFLEV 5 | Effective source |
|---|---:|---:|---:|---:|---|
| Ammon: sign endorsement after helping with moss | 3,000 | 3,000 | 3,000 | 3,000 | BDAMMON state 31; refusing the signature in state 33 pays no XP |
| Fanegonorom: peaceful quest completion | 3,000 | 3,000 | 3,000 | 3,000 | BDMUMMY state 8; count one live reward, not the orphaned legacy branch too |
| Fanegonorom: fight instead, including allies | 5,000 | 5,500 | 7,000 | 8,950 | BDMUMMY CRE 5,000; BD0120.baf:7463–7535 adds 0 / 500 / 2,000 / 3,950 |
| Restless spirit: return the staff | 3,000 | 3,000 | 3,000 | 3,000 | BDSHSARS container + BDSPIRIT.baf:23–35 |
| Restless spirit: fight instead, including three bonebats | 5,925 | 5,925 | 5,925 | 5,925 | BDSPIRIT CRE 3,000; BDSPIRIT.baf:1–10 adds 3 × 975 |
| Shadow coffin | 1,680 | 6,100 | 8,520 | 13,520 | BDSARC03.baf:1–86, one guarded difficulty branch |
| Sarevok's hidden chest wave | 2,825 | 6,050 | 7,150 | 10,025 | BDSHSECR sets the item flag; BD0130.baf:258–372 guards one wave |
| One opening of the skeleton coffin | 400 | 400 | 400 | 400 | BDSARC04.baf:1–10; no explicit one-shot guard, so this is a one-opening convention |
| Eight neutral beetles, if fought | 700 | 700 | 700 | 700 | 3 × BDBEETBR 175 + 5 × BDBEETFM 35; BDBEETFI can turn them hostile |
| Shatter the jelly globes | 540 | 540 | 540 | 540 | BDSHSLIM.baf:20–35 creates BDSHJELL + JELLOC, 270 each |
| Approach the lava mephit trigger while visible | 1,260 | 1,260 | 1,260 | 1,260 | BDSHMMSP.baf:1–14 creates 3 × MEPMAG01, 420 each |

The last two are **region-script spawns**. The shadow coffin and spirit are
container-script roots. Thus the historical statement that the chest is the
only scripted dungeon encounter is incorrect even though counting arbitrary
`CreateCreature` occurrences in the large EET area script is also misleading.

The optional totals are **16,405 / 24,050 / 27,570 / 35,445** for peaceful
mummy/spirit resolutions, or **21,330 / 29,475 / 34,495 / 44,320** for fighting
both, ordered as DIFFLEV 1–2 / 3 / 4 / 5. They include Ammon, the other listed
optional encounters and one skeleton-coffin opening. They exclude the Korlasz
surrender bonus and original jail fight, which are added explicitly below.

## 5. Replacement jailbreak and original prison encounter

Current component 170 CRE XP fields are:

| Creature | XP |
|---|---:|
| CSRKORL | 4,500 |
| CSRHASS | 1,400 |
| CSRVHAS | 1,400 |
| CSRPORI | 975 |
| CSRSILL | 975 |
| CSRGRIT | 175 |

BD0116's first two blocks create the core crew, then Sillune and Grit only with
`DifficultyGT(EASY)`. Therefore clearing the replacement awards **8,275 at
DIFFLEV 1–2**, or **9,425 at 3–5**. The HARDEST block adds defenses and a potion,
not more XP-bearing actors. Fist enforcers are not counted as player enemies.
The source is [comp170.tpa](../../chriz-sod-remix/lib/comp170.tpa) and its current
installed CREs; Grit is 175, not a guessed familiar allowance.

For a surrender-route comparison, the original prison fight matters too. The
**pre-170 WeiDU backup** of BD0116.BCS begins with `!Dead("BDKORLAS")` and creates
`BDKORLAS.CRE`, whose XP field is **2,500**. Its escape/fight chain already
existed before the remix; see the [original SCS/crew research](10d-korlasz-scs-pattern.md).
Thus surrendering in the dungeon and then killing her in the original prison
adds **2,500 party XP** to that comparison. A dungeon kill route has no living
Korlasz to fight again and does not get this addition. Skipping the original
prison rematch also removes the addition.

At the research baseline, component 175 awarded six separate
`AddXPObject(...,24000)` actions, confirmed in installed
CSRCELE state 2. Together with a full replacement fight, that is approximately
**25,379.17 per character at DIFFLEV 1–2**, or **25,570.83 at 3–5**. This total
must not be compared with removed content while forgetting replacement combat.

## 6. Supported candidate accounting scenarios

For six living characters, let `P` be the combined placed XP in section 3,
`J` the replacement fight, and `O` the selected optional total in section 4.

- **Core clear, dungeon kill:** `(P + 2,500 + 30,000 − J) / 6`.
- **Completion, dungeon surrender plus original jail fight:**
  `(P + 2,500 + 30,000 + O + 1,000 + 2,500 − J) / 6`.

These are candidate **Liia award amounts**, after deducting replacement combat.
The completion columns take all listed optional encounters once, including
beetles and globes, then choose peaceful or hostile mummy/spirit resolutions.

| Engine DIFFLEV | Core clear / dungeon kill | Completion / peaceful quest resolutions | Completion / optional mummy and spirit fights |
|---|---:|---:|---:|
| 1 EASIEST | 6,943.33 | 10,260.83 | 11,081.67 |
| 2 EASY | 7,040.83 | 10,358.33 | 11,179.17 |
| 3 NORMAL | 9,440.83 | 14,032.50 | 14,936.67 |
| 4 HARD | 11,879.17 | 17,057.50 | 18,211.67 |
| 5 HARDEST | 14,558.33 | 21,049.17 | 22,528.33 |

For completion without the original prison rematch, subtract **416.67 per
character**. For a dungeon kill instead of surrender, also subtract **166.67**.
Omitting Ammon's endorsement removes 500. Other omissions follow the optional
table divided by six. Decimal values are arithmetic equivalents, not claims
about the engine's per-award integer rounding.

The researched scenarios supported a discussion around roughly **9,400–14,900 at
DIFFLEV 3**, **11,900–18,200 at 4**, or **14,600–22,500 at 5**. They do not select
a new fixed award by themselves. A completion-biased amount, a core-encounter amount and a
difficulty-scaled amount encode different design choices. The baseline 24,000
is above these defined scenarios, but this is not proof of a universal maximum:
rest farming, repeated coffin openings, combat spell summons, lock/trap/scroll
XP, XP modifiers, killing noncombatants and later mod-added content are outside
this ledger. Routes may also skip eligible encounters or resolve them before
their area scripts run. No live XP payout test was performed.

## 7. Ymori: a narrow schedule restoration preserves native staging

This is separate from the prologue ledger. The issue #16 baseline cut key is
`BDYMORI@4089@408` in component 230's BD2000 list. Fresh effective bytes show:

| Field | Effective dev baseline | Pre-230 backup |
|---|---|---|
| BD2000 actor index 1 | Wight / BDYMORI at 4089,408 | Same |
| Actor flags at +0x28 | 0x00000001 | Same |
| Appearance DWORD at +0x40 | **0x00000000** | **0x00FFFFFF** |
| Other bytes in its 0x110-byte actor record | Identical | Identical |
| BDYMORI CRE state DWORD at 0x20 | **0x00080000** | CRE itself was not changed by this ARE cut |

The only differing actor bytes are +0x40, +0x41 and +0x42. The original all-day
mask is **0x00FFFFFF**, not a guessed 0xFFFFFFFF. Crucially, CRE state bit 19 is
the native **deactivated** flag in BG2/BGEE, as documented in the
[primary CRE V1 specification](https://gibberlings3.github.io/iesdp/file_formats/ie_formats/cre_v1.htm).
This is distinct from ordinary invisibility. The [Deactivate/Activate actions](https://gibberlings3.github.io/iesdp/scripting/actions/bgeeactions.htm#125)
describe an actor retained in the area but unavailable until activated.

The current BD2000 container named `Ymoribody` runs `BD2000YM`. That script stages
the body using `BD_SDD222`, advances its local variable after the interaction,
then at `BD2000YM.baf:34–52` calls **`Activate("BDYmori")`**, adds journal 250531
and creates six zombies. BDJUNIA state 30 tests `Dead("bdymori")`; states 32–34
consume the discovery in her confrontation, and the `BDYMORI` item supports an
additional accusation. The creature carries that quest head, Kendra's Chain
(BDAMUL10) and Herdrin's Short Sword +2 (BDSW1H09).

These bytes and scripts support restoring only this actor's original schedule,
removing its cut-list entry, and preserving the CRE state, inventory and
container script. That retains the intended dormant actor for the existing
`Activate` moment. A new first-pass `Deactivate`, early spawn or dialogue rewrite
is not needed to reconstruct the original staging. A zero-schedule saved actor
may require a save-specific repair; an override edit alone is not evidence of
repairing an already visited BD2000.

This establishes a concrete quest dependency and original staging, not a live
proof of the full sidequest. Junia has alternative accusation routes, so it
would be too strong to call every resolution completely hardlocked. The small
restoration is supported without claiming every quest branch was played.

## 8. Evidence and reproducibility

The read-only game source was
`C:\Games\Baldur's Gate II Enhanced Edition modded - dev eet install`.
ARE actors were parsed using the existing bounded `audit_filler.area` and
`audit_filler.creature` parsers, which use the documented ARE actor schedule and
CRE XP/state fields. All 143 dungeon actor rows matched the tracked census.
Attached area, actor, region and container script roots were inspected; three
non-BD trap scripts were freshly decompiled and contain trap spells, not direct
creature creation. Ordinary combat spell trees were not recursively enumerated.

Raw assets remain ignored. Local evidence is under
`research/data/issue16-xp-20260908/`: `decompiled/` contains 13 fresh dialogues,
`extra/decompiled/` the mummy/spirit dialogues and helper scripts,
`traps/decompiled/` the three trap helpers, `native-jail/` the pre-170 area script,
and `recount/recount.json` contains 106 resource SHA-256 hashes, grouped counts,
calculations and the Ymori byte comparison. Existing fresh BAF line references
above use `research/data/issue16-audit/census-v3/baf/`. Newly decompiled dialogue
line references use this recount's `decompiled/` or `extra/decompiled/` directory.
WeiDU ran only with a task output directory as its working directory.

WeiDU.log SHA-256 before and after the read-only recount was identical:
`77f307c7e69a0f930e59f102adbcbbf5a520c9cde3c5f54212e78348de182e5f`.
This detects install-log drift during the recount, not every possible concurrent
manual resource edit. The following hashes identify the principal inputs:

| Resource | SHA-256 |
|---|---|
| BD0120.ARE | `873e95240c86cdf567bbc6f12de0dd50e3a2a7378139b70b0d125b935d129bc6` |
| BD0130.ARE | `6dde32fbf9ca565660222cea85685c98f94fca066370659219f42d0f7dbdd56e` |
| BD0120.BCS | `e710d3534d8187f1d3b79c8666e1b3c4e761700f3ee9477ac5c81f51f43fb4f1` |
| BD0130.BCS | `08b788f2afd4a4ea1b906e01db838948f06200c925f94ab4281a766dac5f9dd5` |
| BD0116.BCS, effective | `9329c955067a8cbc9a2c33c5d6df7de55022e18e4fa737f190d2af88041f5f4a` |
| BD0116.BCS, pre-170 backup | `2e5a4b15910bf24525a7b2fe1240b3e2f26f1c162a5180a9ee91ddfd394733ec` |
| BDKORLAS.CRE | `506f9dcca77333572fbedc32fdc5d5d3fcb21203d46e55049c742e4a455b39ed` |
| BD2000.ARE, effective | `7c3fb9b43af617ce68f92b75a801a0187761098c6501a4e0a645096b355db7be` |
| BD2000.ARE, pre-230 backup | `504c28af9b9c68d4c4d8f1bc3ae4295d549be56075d7df13cf7e624e51861c21` |
| BDYMORI.CRE | `4b6a488aa5f63cce7a25aa5f43905cc8d627709e17a6d15d5b17fa6c2c87f4e3` |

No installer, game resource, save or component 175 amount was changed during this
read-only research. The later approved implementation is recorded at the top.
