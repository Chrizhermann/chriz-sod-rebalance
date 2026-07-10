# 18 — "Lich-lite" undead-caster candidate census (dwarven dig-site miniboss)

> Research data gathered by subagent 2026-07-10 from the dev install (read-only). DATA ONLY —
> decisions live in `docs/design/`.

**Source install:** `C:\Games\Baldur's Gate II Enhanced Edition modded - dev eet install\`
(full BG2:EE + EET, so BG1/SoD/BG2 creatures all present). All CREs/ITMs copied into a
scratch dir and parsed with a purpose-built Python CRE/ITM parser + a chitin.key→BIF
extractor (no game files modified). Offsets per the `bg-modding` skill's `ie-creatures.md`
and repo `docs/research/06-creature-danger.md` (CRE header, effect blocks, item equip-effect
table). IDS decodes from the install's loose `override/{GENERAL,RACE,CLASS,ANIMATE}.IDS`.

**Brief:** the remixed dig site wants a *scary undead-caster miniboss* for party level ~8-12
(BG1-era power curve). A true lich is too much. This doc scopes (1) what existing undead
casters sit between "skeleton mage" and "true lich," (2) the exact recipe + opcode strip-list
to clone-and-weaken a lich if none fit, (3) the SoD-native tier anchors for "scary but fair."
Locked constraint (from the tasking): **NO no-save/no-roll cheese** — the banned exemplars are
`BDSHSOUL` (shadowed souls), `BDBONBAT` (bone bats), `BDUNSLGU` (Unsleeping Guardian).

---

## Headline finding

There is a **real gap** and essentially **no ready-made undead arcane caster** in the target
band. Verified:

- The only existing undead that is a *functional* arcane caster below lich tier is the SoD
  **Skeletal Mage `BDSKGR07`** — L5 mage, **900 XP**, 5 spells (L1–L3).
- The next functional arcane caster up is the **lich** — L11+ mage, **22 000 XP**, full L1–9
  book. Nothing lives in between.
- BG2 **Spectre `SPECTR01`** and **Wraith `WRAITH01`** *carry* an L1–6 wizard spellbook in
  their CRE, **but ship with a melee brain (`GENSHT01`)** and never cast it — they function as
  level-drain melee, not casters. (Both share the *identical* 15-spell list — a vestigial
  block their AI ignores.) They are therefore **donor chassis**, not drop-in casters.
- **Mummies are not casters.** Every mummy/greater-mummy here (`MUMMY`, `MUMMY01`, `FSMUMM/2/3`,
  SoD `BDMUMM01`, `BDMUMMY`) is `class=GHOUL_REVEANT` with an **empty spellbook** — heavy
  resistances + `IMMUNE1`, melee only. The "greater mummy caster" does not exist in this install.

⇒ For a level-8-12 caster miniboss (~3 000-6 000 XP target) you either **up-rank `BDSKGR07`**,
**give a caster brain to a Spectre/Wraith chassis** (spellbook + level-drain already present),
or **strip-clone a lich** (§2). The closest *mechanical* template for "mid caster-miniboss with
weapon-immunity + MR that already works" is the **Rakshasa `RAKSHA01`** (a fiend, not undead).

---

## 1. Candidate census (weak → strong)

Fields: resref · in-game name · kill-XP (CRE `0x14`) · HP (`0x26`) · AC (`0x46`) · THAC0
(`0x52`) · class level (`0x234`) · CLASS.IDS class · animation (`0x28`) → ANIMATE.IDS look ·
spellbook (known-spell list, `0x2a0`) · weapon gate · other. **Weapon gate** = does it carry
`IMMUNE1`/`LICH`/`BDLICH` (op120 → needs a magical weapon to hit)? "**mundane-OK**" = no such
item, any weapon hits.

| # | resref | name | XP | HP | AC | THAC0 | lvl | class | anim → look | spellbook | weapon gate | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| — | **BDWIGHT2** | Imbued Wight | 1200 | 40 | 4 | 14 | 5 | WIGHT | `0xEC20` wight (yellow) | **SPWI112** only (1× L1 Magic Missile) | IMMUNE1 (+1) | barely a caster; 1 spell |
| 1 | **BDSKGR07** | **Skeletal Mage** | **900** | 20 | 7 | 19 | 5 | MAGE | `0xE060` **LICH_WHITE** | SPWI125,112 (L1) · 213,212 (L2) · **305** (L3 nuke) | **mundane-OK** (RING95 only) | **the clean low anchor.** Script `BDSKGR07`. Fragile (HP20) |
| 2 | **BDWRAI01/02** | Wraith (SoD) | 2000 | 48 | 4 | 9 | 6 | WRAITH | `0x7703` SHADOW | — (none) | IMMUNE1 (+1) | melee level-drain; THAC0 9, 2 APR |
| 3 | **WRAITH01** | Wraith (BG2) | 2000 | 43 | 4 | 9 | 6 | WRAITH | `0x7703` SHADOW | 15-spell L1–6 book **but AI=`GENSHT01` (melee)** — never cast | IMMUNE1 (+1) | **donor chassis**: book+level-drain present, needs caster brain |
| 4 | **BDSHADGR / BDSHADOW** | Greater Shadow | 3000 | 72 | 5 | 11 | 9 | SHADOW | `0xEA20` SHADOW_LARGE | — | IMMUNE1 (+1) | melee; strong for its XP |
| 5 | **SPECTR01** | Specter (BG2) | 3000 | 59 | 2 | 13 | 10 | SPECTRE | `0x6200` MAGE_MALE_HUMAN | same 15-spell L1–6 book, **AI=`GENSHT01` (melee)** | IMMUNE1 (+1) | **donor chassis** (as WRAITH01, higher level); level-drain |
| 6 | **BDMUMMY** | Fanegonorom (mummy-lord) | 5000 | 72 | 1 | 11 | 9 | GHOUL_REVEANT | `0xE080` MUMMY | — (not a caster) | IMMUNE1 (+1) | heavy resist (cold/acid/mcold 100, phys 50) |
| 7 | *(ref)* **RAKSHA01** | Rakshasa *(fiend, not undead)* | 3000 | 56 | -4 | 9 | 9 | RAKSHASA | `0x7F10` rakshasa | SPWI112,118,211,303,**304**,308 (L1–3, **casts** via `mage8d`) | IMMUNE1 + **MR** (RAKRING) | **the "it already works" template**: mid caster-miniboss, +1-gate, MR, Fireball |
| 8 | **BDDLICH / LICH01** | Lich | **22000** | 90 | 0 | 9 | 11 | MAGE (→18 via item) | `0x7F0D` **LICH** | **full L1–9** (SPWI913 ADHW, 910/911, 902/903, 717, 523…) | LICH+LICH02 (see §2) | **"too much" baseline.** Brain `mage18d` / `BDLICH`+`dw2mp2ge` |
| 9 | **BDCOLDH** | **Coldhearth Lich** (SoD boss) | 22000¹ | 72 | 0 | 15 | 18 | MAGE | `0x6204` MAGE_MALE_GNOME | full L1–9 incl **SPWI908 Time Stop** | BDLICH+LICH02 (see §2) | phylactery-respawn + force-wall arena (brain `BDLICH01`) |
| 10 | **DW#LICH1-9** | Lich (SCS) | 22000 | **156** | 0 | 0 | 25 | MAGE | `0x7F0D` LICH | full L1–9 + SCS customs (SPWI89x/92x, `dw#qalac`) | LICH+LICH02 | SCS-hardened; brain `dw#mg133-141` |
| 11 | **SENLICH / AMLICH01** | Odamaron / Vongoethe (named) | 22000-25000 | 120-137 | -2/-4 | 7/9 | 20/30 | MAGE | `0x7F0D` LICH | full L1–9 | LICH+LICH02 | named story liches; even more |
| 12 | **SHADEL** | Shade Lord | 25000 | 85 | -2 | 9 | 20 | SHADOW | `0xE050` **LICH_BLACK** | **SPIN117 only** (innate; a summoner/darkness boss, not an arcane caster) | IMMUNE1 (+1) | anim useful, kit not |
| 13 | **DEMILICH** | Demilich | **55000** | 50 | -6 | 9 | 27 | DEMILICH | `0x7F0E` DEMILICH | SPIN788/789 (imprison/wail innates) | LICH02 + op101 death/slay immunity | off the charts |

¹ `BDCOLDH` CRE kill-XP field is 0; the 22 000 is awarded by script `AddExperienceParty(22000)`
(`BD1200.baf:10-18`, per `docs/research/12-coastway-census.md`).

**Explicitly NOT casters (verified empty spellbook — exclude from the search):** all mummies
(`MUMMY`, `MUMMY01`, `FSMUMM/2/3`, `BDMUMM01`, `BDMUMMY`), revenants (`GRREVEN`, `REVEN01`),
ghasts (`BDGHAST`, `BDGHASTG`), most wights (`BDWIGHT/1/3`, `BDWIGHTJ`), all shadows
(`BDSHAD02/04`, `BDSHSOUL`, `BDSHADGR`), bone bats (`BDBONBAT`), armored skeletons
(`BDSKGR01/02/03/08`). These are melee undead — HP/resist/level-drain, no spells.

### Read of the tiers

- **Below the band (too weak):** `BDWIGHT2` (1 spell), `BDSKGR07` (900 XP, HP20).
- **In the band but melee-only (need a brain or a re-skin):** `SPECTR01`/`WRAITH01` (best donors —
  spellbook + level-drain already baked), `BDSHADGR`, `BDMUMMY`.
- **The template that already behaves like the goal:** `RAKSHA01` — a level-9 caster-miniboss with
  Fireball, a +1-to-hit gate, and MR, that the AI actually pilots. Not undead, but the exact
  *mechanical* shape wanted. Cloning its stat line onto an undead chassis/anim is one viable path.
- **Above the band (the "too much"):** every lich (22 000 XP+, full L1–9, item-granted blanket
  immunities), Shade Lord, Demilich.

---

## 2. Build-our-own: the mini-lich recipe (data only)

### 2a. What makes a lich "too much" — and where it lives

A lich's danger is **not** in the CRE resistance bytes. Verified on `LICH01`, `BDCOLDH`,
`DW#LICH1`, and even `RAKSHA01`/`DEMILICH`: **the CRE header magic-resistance region is 0**
(no byte in `0x59`–`0x63` or the `0x64`–`0xB2` window carries MR/weapon-immunity). The lich
package is delivered three ways:

1. **A carried "immunity" item** (`LICH.ITM` / SoD `BDLICH.ITM`) whose 47–71 *equipped* effects
   ARE the lich — this is the strip target.
2. **The spellbook** (`0x2a0` known-spells) — full L1–9 incl. Time Stop / ADHW / PfMW.
3. **The AI brain** (`mage18d` / `dw#mg13x` / `BDLICH01`) — pre-casts PfMW, Spell Turning,
   Stoneskin, Mirror Image, spell-triggers, HLAs; plus phylactery respawn on Coldhearth.
4. Plus the **engine UNDEAD type** (`GENERAL.IDS UNDEAD=4` at CRE `0x271`) — innate immunity to
   sleep/charm/hold/poison/disease/level-drain/critical-hit/backstab, present on *any* undead
   regardless of items. (This part you generally KEEP — it is standard for all undead, not
   lich-specific.)

### 2b. `LICH.ITM` equipped-effect enumeration (the exact strip-list)

Parsed from loose `override/LICH.ITM` (71 equip effects, item enchant 0). Opcode = offset
`0x00` of each 48-byte V1 equip-effect (item equip table via header `0x6a`/`0x6e`/`0x70`):

| Opcode | params | grants | strip for a fair miniboss? |
|---|---|---|---|
| **120** Prot-Melee-Weapons | p1=0 p2=2 | immune to **nonmagical** weapons (needs +1 to hit) | **STRIP** for mundane-OK, or keep *only this* (via `IMMUNE1`) for a light +1 gate |
| **102** Prot-Spell-Level | p1=1,2,3,4 | immune to **ALL level-1–4 spells** | **STRIP** — biggest "your spells do nothing" lever (Coldhearth's `BDLICH.ITM` is L1–3) |
| **101** Prot-Opcode | p2=39,109,55,135,175,217,238 | immune to sleep(39)/hold(109)/slay(55)/polymorph(135)/hold-II(175)/unconscious(217)/**disintegrate(238)** | **REDUCE** — drop 55/238 so save-or-die still threatens; 39/109 are already free from UNDEAD type |
| **206** Imm-Spell-Resource ×~40 | res=SPWI502/503/505…, SPPR502-599, SPWI313/213/215… | immune to named death / level-drain / imprison / maze / breach-tier spells | **STRIP** most — these are anti-cheese for L5–9 play; a low miniboss doesn't need them |
| **296** Set-State | res=SPFLAYER, SPMINDAT (p2=109) | immune to mind-flayer psionic stun | optional keep |
| **328** Set-Ext-State | p2=127,131,135,140 | engine spell-state immunity flags (paired with above) | drops with the effects they gate |
| **28 / 29** Cold / Elec resist | p1=100 | +100% cold & elec | **REDUCE** to ~50 for undead flavour (Coldhearth `BDLICH.ITM` uses 90) |
| **83** Prot-Projectile | p2=186 | immune to one projectile | drop (minor) |
| **267** (feedback-string companion) | p1=strref p2=opcode | shows "Immune!" text next to an op101 immunity | cosmetic; drops with its immunity |

`BDLICH.ITM` (Coldhearth, 47 effects) is the same package **scoped down**: `op120` p1=0 p2=2,
`op102` **L1–3** only, `op100` Prot-Creature-Type p1=9 p2=7, cold/elec **90**, plus the same
op101/op206/op296 set. It is itself a decent "already-trimmed lich item" to start from.

`LICH02.ITM` = **enchant-4 touch weapon, ZERO equipped effects** — purely the melee attack (the
+4 enchant is what lets a lich's touch bypass PfMW/Stoneskin). Strip target = **replace with a
+1/+2 touch** so the miniboss can't ignore party defences.

`IMMUNE1.ITM` (3 effects) = the minimal weapon gate every SoD wight/wraith/shadow/mummy carries:
`op328` p2=178, **`op120` p1=0 p2=2**, `op282` set-spell-state p1=1 p2=25. Use this ALONE if you
want a "+1 to hit" miniboss with no other lich immunities.

`RING95.ITM` (76 effects) = the standard-undead **crowd-control** blanket (immune to
charm5/sleep39/confusion128/horror/hold109/stun45/poison25/feeblemind + Slay-Living family via
SPPR704). It has **no** op102 spell-level immunity and **no** op120 weapon immunity — so keeping
`RING95` gives "CC doesn't work on undead" (flavour) **without** making the miniboss a lich.

### 2c. CRE-side edits to weaken (chassis clone, per `ie-creatures.md` checklist)

- **Level `0x234`** 18-25 → **~8-10** (drives THAC0, HP, slot count).
- **Spellbook `0x2a0`/`0x2b0`** → cut every L5–9 known/memorized entry (Time Stop `SPWI908`,
  ADHW `SPWI913`, PfMW, Spell Turning, Improved Alacrity); keep L1–4 (or L1–3).
- **Race `0x272`** LICH(150) → SKELETON(115) / SHADOW(132) / SPECTRE(133): sheds the "lich"
  label, keeps `general=UNDEAD(4)` engine immunities. (Coldhearth already sits at
  `class=MAGE`, so class need not change.)
- **Animation `0x28`** off `0x7F0D` LICH — see §2d.
- **Scripts `0x248`–`0x268`** → replace `mage18d`/`dw#mg13x`/`BDLICH01` with a light mage
  script (or reuse `BDSKGR07`'s) — no PfMW/Time-Stop/HLA pre-buff, no phylactery loop.
- **Items** → remove `LICH`/`BDLICH` (defence) + `LICH02` (+4 touch); optionally add `IMMUNE1`
  (light +1 gate) and/or `RING95` (undead CC flavour).
- **Kill-XP `0x14`** → set directly (e.g. 3 000-6 000) rather than a script grant.
- **Coldhearth phylactery respawn** (`BD1200.baf:100-146`, phylactery item `BDMISC60`) → drop
  if cloning `BDCOLDH`.

### 2d. Alternative animations (an undead caster that is NOT the lich sprite `0x7F0D`)

From the install's `override/ANIMATE.IDS`:

| Anim ID | ANIMATE.IDS | Look / who uses it |
|---|---|---|
| **`0xE060`** | **LICH_WHITE** | pale robed skeletal caster — **this is the Skeletal-Mage `BDSKGR07` sprite**; best "skeletal necromancer" that isn't the green lich |
| **`0xE050`** | **LICH_BLACK** | dark-robed skeletal caster — the Shade Lord sprite; ominous, not the lich |
| `0x7703` | SHADOW | floating translucent wraith/spirit (incorporeal caster) — SoD wraiths/shadows |
| `0xEA20` / `0xEA10` | SHADOW_LARGE / SHADOW_SMALL | shadow forms |
| `0xEB20` | SKELETON_FIEND | armored skeletal caster |
| `0xEB00` / `0xEB10` | SKELETON_MONSTER / _WARRIOR | skeletal humanoid |
| `0xE080` | MUMMY | bandaged undead (mummy-lord caster look) |
| `0x2300` | DEATH_KNIGHT | armored undead knight — the Unsleeping-Guardian sprite (a "death-knight caster") |
| `0xE25E` | WIGHT_BARROW | barrow-wight |
| `0xE28A` | TROLL_SPECTRAL | spectral troll |
| `0x6200` / `0x6204` | MAGE_MALE_HUMAN / _GNOME | plain robed mage (least overtly undead — "necromancer"). Coldhearth uses gnome-mage `0x6204` |

Note: race (`0x272`) and animation (`0x28`) should move together for a coherent look
(`ie-creatures.md` checklist item 7).

### 2e. SCS lich script stack present here (FILE_EXISTS verified in `override/`)

- **`dw#mg13.bcs`** (SCS master-mage template) + **`dw#mg130.bcs … dw#mg141.bcs`** (difficulty-
  tiered mage brains). The 9 SCS lich CREs `dw#lich1-9.CRE` use **`dw#mg133-141`** as their
  class script — i.e. **SCS liches run the generic SCS mage brain, not a lich-specific one**.
- **`dw#qalac.SPL`** (SCS lich special spell, in every `dw#lich*` known list).
- Vanilla brains **`mage18d` / `mage8d` / `mage16d`** exist biffed (referenced by
  `LICH01`→`mage18d`, `RAKSHA01`→`mage8d`).
- SoD lich scripts: **`BDLICH.bcs`**, **`BDLICH01.bcs`** (Coldhearth combat + phylactery),
  **`BDLICHT.bcs`**, **`BDMISC02.bcs`** (Coldhearth override).

⇒ A "stripped SCS-pattern" mini-lich would **not** reuse `dw#mg13x` (that IS the full lich AI:
sequencers, PfMW, Spell Turning, Time Stop, HLAs). Give the chassis a light mage script (or
`BDSKGR07`'s) so it casts L1–4 without the lich survival kit.

---

## 3. SoD-native "scary but fair" anchor

From `docs/research/06-creature-danger.md` (verified CRE audit) and the `BD1200` garrison census
in `docs/research/12-coastway-census.md`:

- **Hardest SoD undead that are NOT the lich**, by kill-XP: `BDMUMMY` Fanegonorom **5000**
  (HP72, cold/acid/mcold-100 + IMMUNE1); `BDSKGR08` Skeleton Warrior **4000** (HP90, magic-90 +
  IMMUNE1); `BDUNSLGU` Unsleeping Guardian **4000** (**banned** — no-save cheese); `BDSHADGR`/
  `BDSHADOW` Greater Shadow **3000** (HP72); `BDWRAI01/02` Wraith **2000** (THAC0 9, level-drain).
- **The `BD1200` dig-site garrison** (headline stacks, from doc 12): `BDBONBAT`×17 (**banned**),
  `BDDEAD01`×10, `BDSHSOUL`×10 (**banned**), `BDSHZOM1`×9, `BDSKGR04`×9, `ZOMBIE`×6, `BDSKGR05`×5,
  `BDWIGHT1`×5, skeleton-guard families ×~20, `BDSHADGR`×2, `BDUNSLGU`×1 miniboss; boss `BDCOLDH`.
- So the dig site's existing **undead ceiling below the lich is a ~2000-5000 XP melee elite**
  (skeleton warrior / greater shadow / mummy-lord / wraith). A caster miniboss at **~3000-6000
  XP, caster-level ~8-10, spells L1-4, a +1-to-hit gate (IMMUNE1) and NO spell-level immunity**
  would seat naturally **above the garrison trash and below Coldhearth** — the "scary but fair"
  local band.
- The three **banned** exemplars (`BDSHSOUL`, `BDBONBAT`, `BDUNSLGU`) are exactly the
  no-save/no-roll designs the miniboss must avoid: it should threaten through **saving throws
  and to-hit rolls**, not auto-applied effects.

---

## Method / provenance notes

- Parsers + dumps in scratch (`parse_cre.py`, `parse_itm.py`, `extract_biff.py`, `keyscan.py`,
  `*_dump.txt`) — session-local, not committed. CRE effect-block offsets (V2 264-byte, opcode at
  block `+0x08`) per `docs/research/06-creature-danger.md`; item equip-effect table (V1 48-byte,
  opcode at `+0x00`, resource at `+0x14`) per `ie-creatures.md`.
- Names resolved from `lang/en_US/dialog.tlk`. Biffed CREs/ITMs pulled straight from
  `data/*.bif` via chitin.key locators (weidu `--biff-get` was unavailable — dialog-path config
  error — so extraction was done in Python).
- **Un-verified / flagged:** exact spell identities beyond level (spellbook entries cited by
  resref + level digit; only `SPWI112`=Magic Missile, `SPWI908`=Time Stop, `SPWI913`=ADHW named
  with confidence). Engine-UNDEAD innate immunity list is the standard IE set, not re-derived here.
```
