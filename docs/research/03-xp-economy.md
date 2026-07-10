# 03 — SoD XP Economy

**Status:** research (read-only). Maps where SoD's XP comes from so trash-mob removal (Part 1b)
can be compensated by re-weighting big quest rewards (Part 1d) without breaking progression.

**Data sources:** `research/data/sod_baf/*.baf` (1232 decompiled scripts) for area/script awards;
**all 580 `override\BD*.dlg` decompiled with WeiDU** (into scratch, game dir untouched) for
dialogue awards (§1b); trash CRE files read directly from the live `override\`; CRE field offsets
verified against [IESDP CRE v1.0](https://gibberlings3.github.io/iesdp/file_formats/ie_formats/cre_v1.htm).
Spawn context cross-referenced with `sod_areas_dataset.csv`.

---

## 0. Two XP mechanics (verified) — the unit problem

The economy mixes two distribution rules. **Getting the unit right is essential** or quest XP
looks 6× bigger than it is.

| Mechanic | Engine rule | Per-character value |
|---|---|---|
| **Kill XP** (CRE field `0x14`) | **Divided** among living party members ("as equally as possible, remainder to first members") | `K / partysize` (≈ `K/6` full party; **solo gets full `K`**) |
| **`AddexperienceParty(X)`** | Full `X` to **each** member (quest XP "remains the same" regardless of party size) | `X` per char |
| **`AddXPObject(PlayerN,X)`** | Full `X` to that one object | `X` per char (SoD always loops Player1–6 with same `X`) |

Sources: [Fandom Experience Tables](https://baldursgate.fandom.com/wiki/Experience_Tables),
[Beamdog forums — XP distribution](https://forums.beamdog.com/discussion/32466/experience-points-how-does-the-game-distribute-them).

**All XP numbers below are per-character.** This is the right unit for progression (it drives
level). To convert a kill to party-total, multiply by ~6; to convert a quest award to
party-total, also multiply by ~6 (each of 6 gets the full amount). Net: in per-character terms,
**a quest `AddexperienceParty(X)` is worth `~6×` a kill whose CRE field reads `X`.** A troll
(CRE field 1400) is worth only ~233/char; the Coldhearth Lich quest (22000) is worth 22000/char
— roughly **95 trolls**.

**Verified CRE offsets (IESDP, not guessed):** kill-XP `0x14` (dword) · creature's own XP/power
`0x18` (dword) · current HP `0x24` (word) · max HP `0x26` (word). All SoD CREs are `V1.0`.

---

## 1. Scripted quest XP awards (from `.baf` — ranked, per character)

Only `AddexperienceParty` and `AddXPObject` are used. **No** `AddExperiencePartyEE`,
`AddExperiencePartyGlobal`, or `GiveExperience` calls exist in SoD scripts.

### Top scripted awards

| Rank | Award/char | Script | Quest / trigger context |
|---:|---:|---|---|
| 1 | **22,000** | `BD1200` | Kill **Coldhearth Lich** after destroying his phylactery (`BDMISC60`). Single biggest one-shot award. |
| 2 | **20,000** | `BD4000` | **Chapter 11 transition** — Dragonspear Castle assault (`IncrementChapter chptxt11`). |
| 2 | **20,000** | `BD4400` | **Chapter 12 transition** — descent into Avernus (`IncrementChapter chptxt12`). |
| 4 | **15,000** | `BD3000` | **Chapter 10 transition** — Coalition Camp established (`IncrementChapter SODTXT10`). |
| 5 | **12,000** | `BD5300` | Defeat **Kherriun + 6 Dark Magicians** (the Warrens). *(two mutually-exclusive branches, both 12k → 12k/run)* |
| 6 | **10,000** | `BD7100` | **Chapter 9 transition** — Troll Claw Woods cleared (`IncrementChapter SODTXT9`). |
| 6 | **10,000** | `BDBALDUR` | Cure Marek's poison (Marek & Lothander quest). *(two mutually-exclusive branches → 10k/run)* |
| 8 | **9,000** | `BDCOF01` | Stake **Tsolak the vampire**. *(two mutually-exclusive branches → 9k/run)* |
| 9 | **7,500** | `BDCUT10` | Cutscene award (Myself + Player2–6). |
| 10 | **6,000** | several | `BD2000` Boareskyr, `BDCROMMU`, `BDSDD315/316`, plus `BD5000` sub-quests (Slug, Julann/Rigah). |

**The 5 biggest guaranteed awards** (chapter/boss): BD1200 22k, BD4000 20k, BD4400 20k,
BD3000 15k, BD5300 12k. Four of the top six are **chapter-transition rewards** (BD7100/BD3000/
BD4000/BD4400 = **65,000/char guaranteed**) — these are already the game's "big quest reward"
model and the cleanest targets for re-weighting.

### Full per-script totals (per character, branch-adjusted)

| Script | Naive sum | Realistic/run | Note |
|---|---:|---:|---|
| BD4000 | 26,000 | 26,000 | 20k chapter + 6k |
| BD5300 | 24,000 | 12,000 | 2 exclusive 12k branches |
| BD1200 | 22,000 | 22,000 | Coldhearth Lich |
| BD5000 | 20,000 | 14,000 | Slug 6k + Julann/Rigah 6k (matarl* exclusive) + non-violent 2k |
| BD4400 | 20,000 | 20,000 | Avernus chapter |
| BDBALDUR | 20,000 | 10,000 | 2 exclusive 10k branches |
| BD4400(obj) / BD3000 | 20k/15k | 20k/15k | chapter transitions |
| BDCOF01 | 18,000 | 9,000 | 2 exclusive 9k branches |
| BDFOODS | 16,000 | 16,000 | 4× 4k rare-ingredient turn-ins (cook) — all obtainable |
| BD3000 | 15,000 | 15,000 | Coalition Camp chapter |
| BD7100 | 10,000 | 10,000 | chapter |
| BD2000 | 9,000 | 9,000 | Boareskyr |
| BDREDX / BDWATERS | 8,000 ea | 8,000 ea | |
| BDCUT10 | 7,500 | 7,500 | |
| (others ≤6,000) | — | ~30,000 | BDCROMMU, BDSDD315/316, BDEARTHE, BDVIDYAD, BD7300, BDCUT24, BDODSCRY, BDSPIRIT, BDPORTAL, BDSHTORC, BD0104/0111, BDSCRY07, BDDELEND |

- **Naive `.baf` total:** ~274,700/char.
- **Branch-adjusted realistic `.baf` total:** **~235,000/char** (−~37k for mutually-exclusive
  branches in BD5300/BDBALDUR/BDCOF01/BD5000).
- **This is only the area/creature-script layer.** The larger layer is dialogue (§1b).

---

## 1b. Dialogue quest XP awards (from `BD*.dlg` — now measured)

The earlier lower-bound caveat is **closed.** All 580 `override\BD*.dlg` were decompiled with
WeiDU (`weidu --game . --tlkin lang\en_US\dialog.tlk --nofrom *.dlg`, run in a scratch copy — game
dir untouched) and grepped for the same two actions. Again **only** `AddexperienceParty` /
`AddXPObject(Player1..6)` are used; no EE/Global/`GiveExperience` variants.

**83 dialogs award XP, across 327 occurrences.** Counting is dominated by **reply-branch and
outcome duplication** — the same reward is repeated across every player reply that reaches it, and
across mutually-exclusive quest endings. Four dedup levels:

| Counting method | Per-char total | Meaning |
|---|---:|---|
| Naive (every occurrence) | 1,076,250 | meaningless — reply-branch spam |
| Dedup by `(dialog, amount, journal)` | 593,000 | upper bound (counts exclusive *endings* separately) |
| Dedup by `(dialog, amount)` | 416,400 | better (collapses same-amount endings of one quest) |
| **+ manual cross-dialog/exclusivity fixes** | **~350,000** | **realistic obtainable, thorough run** (range ~330–375k) |

Manual fixes applied to the 416,400 figure: **−32,000** (BDCORWIJ's 32k is the *same* dragon
reward as BDHALAT's 32k — it fires through Corwin's dialog only when she's in the party) and
**−12,000** (BDHALAT's 12k "hostile" ending is mutually exclusive with its 32k "peaceful" ending);
several smaller faction-exclusive/optional side quests trim it further → **~350,000/char** central.

### Top dialogue awards (per char, exclusivity-aware)

| Award | Dialog(s) | Quest / context |
|---:|---|---|
| **32,000** | `BDHALAT` (or `BDCORWIJ` if Corwin present) | **Free Halatathlaer the dragon spirit** — placed in BD5100/BD5300, the Underground River arc (Ch.10), NOT the Forest of Wyrms (corrected 2026-07-10; see research/13). Biggest single dialogue reward. *Hostile ending = 12,000 instead.* |
| **18,000** | `BDDAEROS` | **Free the ghost of Daeros Dragonspear** (Dragonspear Castle basement). |
| **12,000** | `BDMURS` | Resolve the **ogre-tribe leadership** (Murs becomes chief; 3 exclusive endings, all 12k). |
| **12,000** | `BDMKHIIJ` | **Stand up for M'Khiin** (goblin companion personal quest). |
| **12,000** | `BDLADLE` / `BDPWATER` / `BDJAMVEN` | Tied cluster: camp **crate-moving job** / **water-folk** quest / **seed** quest. |

Other notable: `BDISABEL`+`BDTSMESS`+ script `BDCOF01` form the **Tsolak vampire-hunt** line
(~9k per step); a long tail of **~6,000** camp/side-quest turn-ins (`BDDOSIA`, `BDJULANN`,
`BDNAN`, `BDNEDERL`, `BDNEERA`, `BDOTILDA`, `BDSIMONE`, `BDMKHIIN`, `BDSHAPUR`, the `BDFOODS`
cook ingredients, etc.). Per-dialog totals concentrate in a handful of NPCs: BDHALAT/BDCORWIJ
(dragon), BDMURS (42k naive→12k real, ogres), BDDAEROS (Daeros), BDMKHIIJ/BDMKHIIN (M'Khiin).

> **Dialogue XP (~350k/char) is ~1.5× the scripted/area XP (~235k/char).** Most SoD quest XP lives
> in conversations, not area scripts — so any reweight must touch `.dlg`, not just `.baf`.

---

## 2. Common trash kill-XP (CRE field `0x14`, verified)

Read directly from live `override\`. Per-char = field ÷6 (full party).

| Creature (resref) | Kill-XP (field) | Per-char (÷6) | Max HP | Tier |
|---|---:|---:|---:|---|
| Hobgoblin (`HOBGOB`) | 35 | 6 | 8 | chaff |
| Skeleton (`BDSKGR00`) | 65 | 11 | 8 | chaff |
| Wolf (`BDWOLF`) | 65 | 11 | 24 | chaff |
| Bandit (`BDBANDIT`) | 65 | 11 | 10 | chaff |
| Orc (`ORC01_`) | 120 | 20 | 30 | low |
| Lemure (`BDLEMURE`) | 120 | 20 | 16 | low |
| Ghoul (`GHOUL`) | 175 | 29 | 16 | low |
| Bugbear (`BDBUGB01`) | 175 | 29 | 40 | low |
| Diseased/Dire Wolf (`BDWOLFDI`) | 175 | 29 | 40 | low |
| Skeleton, heavy (`BDSKGR04`) | 250 | 42 | 40 | mid |
| Skeleton warrior (`BDSKGR02`) | 400 | 67 | 60 | mid |
| Giant Spider (`BDSPIDGI`) | 420 | 70 | 40 | mid |
| Ghast (`GHAST`) | 650 | 108 | 32 | mid |
| Troll, small (`TROLLSM`) | 750 | 125 | 32 | high |
| Troll (`TROLL01`) | 1,400 | 233 | 54 | high |
| Imp (`BDIMP`) | 1,400 | 233 | 18 | high |

**Range:** chaff ~35–65 (≈6–11/char) → high ~1,400 (≈233/char). The common wilderness-spawn mix
(wolves, skeletons, spiders, bandits, ghouls, the odd troll) averages roughly **300–400/kill
party-total ≈ 50–65/char.** Trolls/imps/ghasts are the outliers that actually move the bar.

---

## 3. Where trash volume comes from (for the reweight estimate)

Per `sod_areas_dataset.csv`, the bulk of combat trash is **not** scripted `CreateCreature` (most
of those 2520 calls are NPCs/cutscene actors/coalition-camp & Flaming-Fist allies — `cutspy`,
`bdfist*`, `safana7`, companion `*7_` clones). Trash comes from:

1. **Random spawn / rest tables** — ~25 wilderness areas with `difficulty 80–200` (⇒ always
   `max` creatures: 3–6 per spawn) and felt encounter rates 22–80%. Volume scales with traversal
   time and respawns.
2. **A few large scripted set-pieces** — BD0120 skeleton crypt (206 spawns, incl. allies),
   BD3000 Coalition Camp siege (198), BD4000/BD4300 castle assault (85/59). These mix enemies and
   allies, so not every spawn is XP.

A precise count is **research/02's job** (encounter inventory, in progress) — it will firm up the
number below.

---

## 4. Reweight budget

### Total XP split (per character)

| Bucket | Per-char | Confidence |
|---|---:|---|
| Scripted/area quest XP (`.baf`) | ~235,000 | **measured** (branch-adjusted) |
| Dialogue quest XP (`BD*.dlg`) | ~350,000 | **measured** (exclusivity-corrected; range 330–375k) |
| **Quest XP subtotal** | **~585,000** | measured (range ~565–610k) |
| **Kill XP (all trash + set-pieces)** | **~80,000–130,000** | est. (see below) |
| **SoD total gain (thorough run)** | **~665,000–715,000** | est. |

**No XP-cap clipping in this install.** SoD's stock 500,000 cap is **removed** here:
`override\XPCAP.2DA` default = 2,950,000 with every class row `-1`, and `SODSTRTA.2DA`
`START_XP_CAP = -1`. So the full quest XP above is actually *absorbed*, not wasted — the economy
math is real, not capped.

**Kill-XP estimate (two methods):**
- *Bottom-up:* ~1,300–2,300 trash kills/run × ~55/char avg ≈ **70,000–130,000/char.**
- *Sanity:* even at the high end it is dwarfed by the now-measured ~585k quest XP.

**Headline finding (strengthened): SoD is overwhelmingly quest-XP-driven.** Quest XP is
**~82–88% of total**; kill XP only **~12–18%**. Dialogue alone (~350k) is ~1.5× all scripted
quest XP and ~3–4× *all* trash kills combined. Cutting trash barely dents progression.

### How much to re-inject if ~70% of trash is removed

- Removed kill XP ≈ 0.70 × ~100,000 ≈ **~70,000/char** (range ~50k–90k) = **only ~10% of total
  SoD XP.**
- **Two effects shrink the true gap:**
  1. Retained 30% trash still pays (~30k/char).
  2. Part 1c makes a few fights *meaningful* — buffed retained creatures return some kill-XP.
- **Net re-injection target: ~40,000–70,000/char.** Round figure for design: **~60,000/char** —
  a **~10% top-up** on the existing ~585k quest XP, trivially absorbed.

### Where to put it (design options — for `docs/design/`, not decided here)

- **A. Scale the big guaranteed awards (cleanest; matches existing model).** Combine the two
  layers: the 4 chapter transitions (`.baf` 10k/15k/20k/20k = 65k) + top scripted bosses
  (BD1200 22k, BD5300 12k) + the top dialogue rewards (BDHALAT/BDCORWIJ dragon 32k, BDDAEROS 18k).
  A flat **~+10% across these** (~13k+ here alone) plus a few targeted bumps reaches ~60k/char
  with almost no new content.
- **B. Per-area "cleared" bonus** — ~8–10 wilderness areas × ~6–7k/char ties XP to exploration
  rather than kill-count; easy to gate on an area global.
- **C. Buff the retained set-piece creatures' kill-XP** so fewer, harder fights carry the weight
  (synergizes with 1c).
- Recommended: **A as the backbone** (predictable, reversible, lore-fits the beats) +
  **C for the 2–3 redesigned fights.** Avoid B for trash-heavy areas being thinned (defeats the
  purpose). Because the budget is only ~10% of quest XP, a uniform proportional scale is the
  lowest-risk option — it preserves the existing reward *shape*.

### Implementation note

Awards live in **two** file types and a reweight must touch both:
- **`.baf`** (area/creature scripts) — `AddexperienceParty(N)` / `AddXPObject(PlayerN,N)`.
- **`.dlg`** (the larger layer, ~350k/char) — same actions inside transition `DO` blocks.

WeiDU patching: `.baf` via `COMPILE`/`REPLACE_TEXTUALLY` or `EXTEND_*`; `.dlg` via
`ADD_TRANS_ACTION` / `ALTER_TRANS` or decompile-edit-recompile. All reversible (backups). **Mind
mutually-exclusive branches**: scale the *award constant*, not per-occurrence, or the same reward
gets multiplied across reply branches. The dedup map in §1b (one reward per `(dialog, amount)`,
with the BDHALAT/BDCORWIJ merge) is the correct target list.

### Biggest uncertainties

1. **Trash kill count** — the dominant remaining unknown; needs research/02 encounter inventory to
   firm up the ~80–130k/char kill-XP figure.
2. **Quest exclusivity / completion rate** — the ~350k dialogue figure assumes a *thorough* run.
   Faction-exclusive and optional side quests mean an actual run lands somewhere in ~250–375k; the
   reweight % (≈10%) is robust to this because both numerator and denominator move together.
3. **Branch exclusivity precision** — top dialogue dups corrected manually; the long ~6k tail is
   `(dialog, amount)`-deduped, which may still slightly overcount multi-step quests.
4. *(Resolved)* XP cap — removed in this install (XPCAP.2DA = 2.95M, classes −1), so no clipping.
