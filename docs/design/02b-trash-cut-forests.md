# 02b — DESIGN: Wilderness / Forest Trash-Cut Proposal

Status: **design proposal — markdown only, no game changes.** Implementation (WeiDU tail-mod that
`COPY_EXISTING` each `BD7*.are` and removes/edits actor entries) comes after sign-off.
Source data: `docs/research/02b-encounters-forests.md` + `docs/research/sod_encounters_full.csv`.
Date: 2026-06-21.

## Framing & method
- **Goal:** ~70% reduction of *placed trash* across the forest region, biased toward low-XP filler
  (beetles, redundant displacer/spider/wolf packs) and over-sized identical packs, while keeping
  each area's flavor and intended path challenge.
- **Counts are placed-actor baselines.** SoD's base packs are **difficulty-independent** — the same
  on Story…Insane. The exception is SoD's per-difficulty *variant* placement (`_HARD/_INSANE`
  suffixes), concentrated in **BD7220** (and scattered `_HARD` subsets). On **Insane (Difficulty 5 /
  Legacy of Bhaal)** those variants stack on top, so the user sees **≈ baseline in flat-pack areas
  and noticeably more (toward 2×) in variant-tagged areas** — i.e. cutting the variant-tagged mobs
  is *doubly* effective for this user. Each area below flags where Insane scaling bites.
- **Preserve untouched (per directive):** Morentherene green dragon **BD7210**, Neothelid cult
  temple **BD7230**, shadow tomb **BD7310**.
- **Three "make-meaningful" upgrades** (fewer-but-elite, named leader, real tactics) instead of pure
  deletion: Hill-Giant warband **BD7300**, Troll Shamaness **BD7110**, Bloodbark Vampire **BD7410**
  (+ Greater Basilisk **BD7400**).
- Removal lists give **resref × count to delete** and **what to keep**. Quest/neutral NPCs and
  scripted one-off set-pieces (Tsolak wolves, Neera wolfpack, dragon adds, aerial servants) are
  **never** in the cut — they're story.

---

## BD7300 — Dead Man's Pass  (biggest trash field)
**Current placed enemies: 139** (Insane: ~same; no difficulty-suffixed packs here). Rest felt 39/44%.

| Pack | resref | now | **delete** | **keep** | rationale |
|---|---|---:|---:|---:|---|
| Beetles | `BDBEETMH` / `BDBEETBH` | 23 | **23** | 0 | pure filler (120-175 XP), two infestations add nothing |
| Displacer beasts | `BDDISPBE` (+`BDDISPBP`) | 19 | 14 | 5 (4+1 lord) | keep one pack; recurs in 7100/7200 |
| Orogs | `BDOROG01/02/03/04/05/SG` | 21 | 12 | 9 warband | chief+shaman+priest+2 elite+4 grunt |
| Hill giants | `BDGIANHI` (+`BDGIANHL`) | 11 | 6 | 5 | → **set-piece upgrade** (leader + 4) |
| Dire wolves | `WOLFDI` | 11 | 7 | 4 | one pack |
| Ogres | `BDOGRE01-06` | 12 | 9 | 3 | chieftain+berserker+shaman pocket |
| Spiders | `SPIDPH/SPIDSW01/SPIDGI/BDSPIDGA` | 12 | 8 | 4 | phase-spider nest (3 phase+1 sword) |
| Hobgoblins | `BDHOBG01-04` | 10 | 7 | 3 | small pocket (cap+2 archer) |
| Boars | `BDBOAR02` | 7 | 7 | 0 | filler |
| Worgs | `BDWORG` | 4 | 4 | 0 | filler (fold into wolves) |
| Ettins | `PETTIN` | 2 | 0 | 2 | elite pocket |
| Shambling mounds | `BDSHAMB` | 2 | 0 | 2 | corrupted-grove flavor (6000 XP) |
| Dark treants | `BDTREANT` | 2 | 0 | 2 | corrupted-grove flavor |
| Cave bear / hamadryad / nymph | `BD328OSO/BDHAMADR/BDNYMP01` | 3 | 0 | 3 | unique flavor |

**Before → after: 139 → 42  (−97, −70%).** Keep = giant warband 5 + orog warband 9 + displacer 5 +
wolves 4 + spider nest 4 + ogre pocket 3 + hobgob pocket 3 + ettins 2 + shambling 2 + treants 2 +
bear/hamadryad/nymph 3.
Preserve: spectacles enemies (`bdearthe` 11000 XP, `BDRAEANN`), `bdephrik`, the Corwin parley
cutscene. Rest table can still drop a hill giant — see `research/01` for the rest-fix.

---

## BD7100 — Troll Claw Woods / Coalition camp hub
**Current placed enemies: 104** (Insane: ~same). Rest felt **49/57% — worst forest rest**, troll in table.
This map *becomes the army camp* in Ch.9, so it should read safer afterward; keep the **troll
identity** but not a 32-troll slog.

| Pack | resref | now | **delete** | **keep** | rationale |
|---|---|---:|---:|---:|---|
| Trolls | `TROLL01/TROLSP01/TROLLSM/TROLLGI` | 32 | 20 | 12 | namesake — keep most of any pack (6 reg + 3 spectral + 2 small + 1 giant) |
| Hobgoblins | `BDHOBG01-05` | 16 | 11 | 5 warband | captain+2 scout+1 archer+1 priest |
| Spiders | `SPIDGI/SPIDHU/SPIDSW/BDSPIDGA` | 15 | 11 | 4 | one mixed nest |
| Orcs | `ORC01_-07/03_/04_/05_` | 13 | 10 | 3 | trim to a scout party (orcs belong to 7000) |
| Ogres | `BDOGRE01-06` | 10 | 6 | 4 | chieftain+berserker+mage+1 |
| Beetles | `BDBEETMH/BDBEETBH` | 8 | 8 | 0 | filler |
| Displacer beasts | `BDDISPBE/BDDISPBP` | 6 | 6 | 0 | recurs in 7200/7300 |
| Boars | `BDBOAR02` | 2 | 2 | 0 | filler |
| Bears + dead dog | `BEARBR/BDDEADOG` | 3 | 0 | 3 | flavor/prop |

**Before → after: 104 → 31  (−73, −70%).**
Preserve: SDD225 "Irregulars" Kava/Farrl/Rend, Soralis+golem, the whole camp NPC population, all
9 (already script-deactivated) spawn points.

---

## BD7200 — Forest of Wyrms (overland, approach to the dragon)
**Current placed enemies: 47** (Insane: bugbears partly variant — slightly more). Rest felt 39/44%.
Keep the **wyvern identity** (Forest of *Wyrms*) as the lead-in to Morentherene.

| Pack | resref | now | **delete** | **keep** | rationale |
|---|---|---:|---:|---:|---|
| Wyverns | `BDWYVR01/02/03` | 13 | 6 | 7 | theme — 2 greater + 3 wyvern + 2 baby |
| Bugbears | `BDBUGB01/02/04/10/12/20` | 11 | 7 | 4 | warren is 7220; keep shaman+warleader+2 |
| Displacer beasts | `BDDISPBE/BDDISPBP` | 7 | 7 | 0 | redundant |
| Phase spiders | `SPIDPH/SPIDPHAS` | 5 | 3 | 2 | astral + 1 |
| Dire wolves | `WOLFDI` | 5 | 5 | 0 | filler |
| Small spiders | `BDSPIDER` | 5 | 5 | 0 | filler (65 XP) |
| Hill giant | `BDGIANHI` | 1 | 0 | 1 | mini-boss flavor |

**Before → after: 47 → 14  (−33, −70%).**

---

## BD7400 — Bloodbark Grove (undead/corruption; Neera + basilisk quests)
**Current placed enemies: 37** (+ scripted wolfpack 8). Rest felt 39/49%. Has the region's **only
active spawn point** (`Spawn 1`, max 6).

| Pack | resref | now | **delete** | **keep** | rationale |
|---|---|---:|---:|---:|---|
| Beetles | `BDBEETMH/BDBEETBH` | 13 | 13 | 0 | filler |
| Burning skeletons | `BDSKGR05/06/07` | 9 | 6 | 3 | keep skel-mage + 2 (token resistant squad) |
| Cold wights | `BDWIGHT3` | 4 | 3 | 1 | thin |
| Imbued wights | `BDWIGHT2` | 2 | 1 | 1 | thin |
| Bonebats | `BDBONBAT` | 2 | 2 | 0 | filler |
| Ghasts | `GHAST` | 2 | 1 | 1 | thin |
| Dark treants | `BDTREANT` | 2 | 0 | 2 | corruption flavor |
| Shambling mound / shadowed soul | `BDSHAMB/BDSHSOUL` | 2 | 0 | 2 | elite flavor |
| **Greater basilisk** | `BD302BAS` | 1 | 0 | 1 | → **set-piece upgrade** |

**Before → after: 37 → 11  (−26, −70%).**
Preserve: scripted Neera SDD302 wolfpack (8). **Spawn-point recommendation (separate from placed
cut):** drop `Spawn 1` `max 6 → 2` so ambient undead atmosphere remains without flooding.

---

## BD7220 — Bugbear warren (+ spectacles Greater Shadow)
**Current placed enemies: 36** — **heavily difficulty-variant.** On **Insane the `_HARD/_INSANE`
bugbears stack → real live count is well above 36; on Core ~22-24.** Cutting the variant-tagged
mobs is the single highest-leverage Insane win in the region. Keep it a **bugbear stronghold**, just
smaller, anchored by the named chief.

| Pack | resref | now | **delete** | **keep** | rationale |
|---|---|---:|---:|---:|---|
| Stalkers | `BDBUGB04` | 8 | 6 | 2 | cut the `_HARD` stalkers first (Insane bloat) |
| Basic bugbears | `BDBUGB01/02/03` | 12 | 9 | 3 | trim |
| Veterans | `BDBUGB10/11` | 8 | 6 | 2 | trim |
| Shaman | `BDBUGB20` | 4 | 3 | 1 | cut `_INSANE` shamans |
| Warleader | `BDBUGB12` | 2 | 1 | 1 | keep one |
| Elder | `BDBUGB21` | 1 | 0 | 1 | keep |
| **Snorgash (chief)** | `BDSNORGA` | 1 | 0 | 1 | named leader |

**Before → after: 36 → 11  (−25, −69%; larger effective cut on Insane).**
Preserve: `BDSHADOW` Greater Shadow (SDD118 spectacles quest, NEUTRAL).

---

## BD7000 — Coast Way Forest (entry; orc raiding party)
**Current placed enemies: 22** (+ scripted SDD123 dire wolves 16). Rest felt 34%.
Keep one leaner orc war-party as the area's signature skirmish.

| Pack | resref | now | **delete** | **keep** | rationale |
|---|---|---:|---:|---:|---|
| Orc archers | `ORC02_` | 8 | 6 | 2 | trim |
| Orc warriors | `ORC01_` | 5 | 3 | 2 | trim |
| Orc raiders | `ORC06_` | 2 | 2 | 0 | filler |
| Orc bowmasters | `ORC07` | 2 | 2 | 0 | filler |
| Orc priest | `ORC03_` | 1 | 1 | 0 | trim caster bloat |
| Orc leader / shaman | `ORC04_` / `ORC05_` | 2 | 0 | 2 | keep the leadership |
| Wargs | `BDWORG` | 2 | 1 | 1 | mount flavor |

**Before → after: 22 → 7  (−15, −68%).**
Preserve: SDD123 Tsolak vampire fight + its 6/11/15 dire-wolf summon (difficulty-scaled).

---

## "Make-meaningful" upgrades (fewer but elite — describe, not just delete)

### BD7110 — Troll Shamaness lair  (16 → 7, redesigned)
Keep: **`BDTROLSH` Troll Shamaness** (named leader) + 2 `TROLLGI` giant-troll bodyguards + 3
`TROLL01` + 1 `TROLSP01` spectral. Delete 9 (the surplus regular/small/giant trolls).
**Upgrade design:** position the shamaness at the back with line-of-sight casting and a
**heal/regeneration-buff on her trolls** (she keeps them standing unless the party brings
fire/acid), giant trolls as the front wall, the spectral troll flanking from stealth. The fight
becomes a *tactical puzzle* (burst the shamaness / bring AoE fire) rather than a 16-body slog. Net
danger up, body count down.

### BD7300 — Hill-Giant warband  (the area's new climax)
Keep: **`BDGIANHL` Hill-Giant Leader** + 4 `BDGIANHI` + (adjacent) the kept orog warband as
"conscripts." **Upgrade design:** cluster them as one staged encounter on the pass — leader hangs
back hurling rocks (ranged), giants form a line, orogs screen. Give the leader a rallying/enrage on
first giant death. This replaces the diffuse 139-mob sprawl with one memorable set-piece + a few
elite pockets (ettins, shambling mounds, dark treants) scattered as "biome texture."

### BD7410 — Bloodbark Vampire den  (14 → 5, redesigned)  & BD7400 Greater Basilisk
- **BD7410:** keep **`VAMFLM01` Fledgling Vampire** (8000 XP) + 2 `BDWOLFVA` vampiric wolves + 2
  `BDWOLFDR` dread wolves; delete the 5 plain `WOLF` + 2 surplus dread/vampiric. **Upgrade design:**
  the vampire fights *smart* — opens with domination/gaze, retreats to **gaseous form** at low HP
  and re-engages (level-drain on melee), wolves operate as a coordinated flanking pack. A real
  vampire encounter, not a wolf pile.
- **BD7400 Greater Basilisk (`BD302BAS`):** leave as the "Basilisk Sighting" set-piece but make the
  approach matter — petrification gaze with a telegraph, a petrified-victim prop or two for stakes.
  No count change (it's already a 1-creature set-piece); the win is that the *surrounding* beetle/
  skeleton trash is gone so the basilisk reads as the threat it should be.

---

## Region summary

| Area | role | before (placed) | after (placed) | cut % | note |
|---|---|---:|---:|---:|---|
| BD7300 Dead Man's Pass | overland | 139 | 42 | 70% | + giant-warband upgrade |
| BD7100 Troll Claw Woods | camp hub | 104 | 31 | 70% | worst rest pressure |
| BD7200 Forest of Wyrms | overland | 47 | 14 | 70% | |
| BD7400 Bloodbark Grove | overland | 37 | 11 | 70% | + basilisk; spawn max 6→2 |
| BD7220 Bugbear warren | sub | 36 | 11 | 69% | biggest Insane win |
| BD7000 Coast Way Forest | entry | 22 | 7 | 68% | |
| BD7110 Troll lair | sub | 16 | 7 | 56% | **upgrade** (deadlier) |
| BD7410 Vampire den | sub | 14 | 5 | 64% | **upgrade** (deadlier) |
| BD7230 Cult temple | dungeon | 18 | 18 | 0% | **preserve** |
| BD7310 Shadow tomb | sub | 10 | 10 | 0% | **preserve** |
| BD7210 Morentherene | sub | 0 | 0 | — | **preserve** |

- **Placed enemies region-wide: 443 → 156  (−287).**
- **Across the 8 trash/upgrade areas (excluding the 3 preserved set-piece dungeons): 415 → 128
  (−287, −69%).** ✓ target.
- **Total enemy incl. scripted one-offs: 476 → 189** (33 scripted/quest one-offs preserved).
- On **Insane** the felt reduction is larger in BD7220 (and any `_HARD`-tagged subset), since those
  variants stacked on top of the baselines being cut.
- **XP impact (feeds Part 1d):** ~287 removed mobs average roughly 300-1000 kill-XP; **order of
  ~150-200k XP removed across the region.** This must be recovered via main-quest reward reweighting
  (`research/03` / design 1d) so total progression is preserved — do **not** ship the cut without
  the XP reweight.

## Judgment calls to confirm with the user
1. **BD7100 trolls 32 → 12** — trolls are the area's namesake *and* it becomes your camp. Is 12 the
   right "menace level," or do you want more (15-18) on first traversal / fewer once camp is set?
2. **BD7300 — delete ALL ogres (12→3) and most hobgoblins (10→3)?** They recur elsewhere; confirm
   they can thin hard here, or keep an ogre band as a second pocket.
3. **BD7400 spawn-point `max 6 → 2`** — OK to also tune the one active ambient spawn point (vs only
   touching placed actors)? Atmosphere vs flood.
4. **BD7230 cult temple — 100% preserve, or trim the 3 worgs + 4 enthralled cultists** as the only
   "trash" inside an otherwise-set-piece dungeon? I lean 100% preserve.
5. **Upgrade appetite:** the 3 make-meaningful fights add *abilities/tactics* to named bosses
   (shamaness regen-heal, vampire gaseous-form/drain, giant leader enrage). Confirm you want them
   genuinely *harder per-creature*, not just fewer bodies.
6. **XP reweight dependency:** confirm the trash cut ships *together with* the 1d quest-XP reweight
   (~150-200k forest XP to relocate), not before it.
