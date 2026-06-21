# 08 — Companion Power Audit

Status: **synthesized** from per-companion CRE/2DA/ITM/SPL assessments of the live modded
install (EET + AK + SR + SCS + CDTweaks, as actually installed). Read-only.
Date: 2026-06-21. Scope: all 56 joinable companions across BG1 → SoD → BG2 → ToB.

## Purpose

Establish a single power baseline for the `chriz-sod-rebalance` remix so that buffs and nerfs
target the genuine outliers rather than perceived ones. Each companion was scored on four axes
(Offense / Defense / Utility / Scaling, 1–10) and given a verdict. Tiers below collapse those
verdicts into an S→D ladder.

---

## 1. Tiered power ranking

Axes are `Off / Def / Util / Scl` (1–10). **Scope** = the EET content window the live CREs
actually cover, which heavily conditions the Scaling axis:
`Full` = BG1→ToB · `BG1` / `BG1-SoD` / `SoD` = departs at that boundary ·
`SoA-ToB` = BG2 recruit · `ToB-end` = endgame only · *(ally/temp)* noted inline.

### S tier — Overpowered (above the SCS/Insane curve)

| Companion | Class / Kit | Off/Def/Util/Scl | Scope | Note |
|---|---|---|---|---|
| **Sarevok** | Fighter, TRUECLASS | 9/10/3/8 | ToB-end | Joins wearing undroppable boss invuln package (INVULNER + CHWRAITH) — 100% damage/spell/MR immunity + Deathbringer 200-dmg proc. Literally unkillable. |
| **Edwin** | Mage / Red Wizard (AK) | 10/7/9/10 | Full | Even after slot-fixes: net +2 slots/lvl, +5 caster level, enemy save-penalty, free SCS sequencers. Strongest arcane unit obtainable. |
| **Hexxat** | Thief / Invisible Blade (AK), vampire | 8/9/8/8 | SoA-ToB | Vampire STR20/DEX20 + dagger Mastery dual-wield + amulet near-total immunity to the entire SCS soft-CC arsenal. |
| **Pai'Na** | Druid / Hive Mother (AK) | 7/8/8/8 | SoA-ToB | Full druid book + Widow's Kiss +1 slot/lvl + arcane innates + L15/18 blanket disabler immunity. (Verify GA_ innates bake.) |
| **Baeloth** | Sorcerer, TRUECLASS, drow | 8/6/7/5 | BG1-SoD | Spontaneous 6/6/4 with a 19-spell known list (bigger than a player sorcerer) + flat MR 50 at low level. Tier king for BG1/SoD. |

### A tier — Strong (high value, defensible for Insane)

| Companion | Class / Kit | Off/Def/Util/Scl | Scope | Note |
|---|---|---|---|---|
| **Jan Jansen** | Mage/Thief / Arcane Trickster (AK) | 7/6/10/8 | SoA-ToB | Detect Illusion 76 + full arcane + Pilfer Magic; best toolbox of its trio. |
| **Keldorn** | Paladin / Inquisitor | 7/8/9/7 | SoA-ToB | 2× Dispel + True Sight + Hold/Charm immunity = the canonical SCS-mage counter. |
| **Anomen** | Fighter/Cleric, no kit | 6/8/8/8 | SoA-ToB | Premier support-tank: 124 HP, plate+shield, full priest + warrior HLAs. |
| **Evandra** | Sorcerer (converted), no kit | 6/8/8/8 | SoA-ToB | Spontaneous self-protect + protection-stripping suite; low blast ceiling. |
| **Aerie** | Cleric/Mage, no kit | 7/5/9/8 | Full | Dual full caster — highest utility in the game; glass body holds it back. |
| **Ajantis** | Paladin / Divine Champion (AK) | 7/9/6/7 | Full | Save-proof off-tank/striker + L1-4 divine casting + Smite. |
| **Dorn** | Paladin / Blackguard (AK enhanced) | 8/7/6/8 | Full | STR19 warrior + Life Drain + Poison Weapon + fear aura. Leans OP. |
| **Imoen** | Mage/Thief / Trickster (AK) | 6/7/9/7 | Full | Elite arcane+thief toolbox + stacking Trickster passives. |
| **Quayle** | Cleric/Mage, Illusionist | 6/6/9/8 | BG1(+) | Dual book protection-stripper/buff engine; ugly physicals don't matter. |
| **Wings (Lara)** | Ranger / Feralan (AK) | 8/7/7/6 | SoA-ToB | GM short bow + +4 bow + 204 HP; fixed 2.5M XP is the over-power vector. |
| **Sirene** | Paladin / Knight of the Mystic Fire (AK) | 6/8/7/7 | SoA-ToB | Tanky paladin + arcane (Stoneskin/PFMW) + Shatter Spell anti-mage. (Metadata "Martyr" is wrong.) |
| **Mazzy** | Paladin / Divine Champion (AK) | 7/8/6/7 | SoA-ToB | Stacking saves + Divine Wrath + Rapid Shot archery; STR15 brake. |
| **Yeslick** | Fighter/Cleric / Alaghor (mod) | 6/8/7/7 | Full | Dwarf+CON17 near-CC-immunity + full F/C + fixed Dispel innate. |
| **Korgan** | Fighter / Berserker (AK) | 8/8/2/8 | SoA-ToB | GM dual-axe + Enrage CC-immunity. Benchmark "strong but appropriate". |
| **Sha'Teel** | Fighter / Wizard Slayer (AK) | 7/6/7/7 | BG1 | AK redesign into a real anti-caster; CON9 fragility is the tax. |
| **Minsc** | Ranger / Rashemi Berserker (AK) | 6/8/5/7 | Full | Rage = 10rd broad disabler immunity; capped at Master (no GM). |
| **Aura** | Bard / Artificer (AK) | 6/6/9/7 | Full | Infusion + Craft Automaton + snares; loaded kit on a weak chassis. |
| **Bristlelick** | Fighter / Gnoll Bruiser (mod) | 8/6/6/4 | BG1 | STR19 + ench-3 halberd deletes BG1; short tenure caps it. |
| **Coran** | Fighter/Thief, no kit | 8/5/6/4 | BG1 | DEX20 + Longbow spec = premier BG1 archer; BG1-only. |
| **Caelar Argent** | Fighter (ally form) | 8/8/3/3 | SoD *(ally)* | Scripted guest powerhouse for one battle — intentionally above curve. |
| **Corwin** | Ranger / Feralan (AK) | 8/5/5/5 | SoD | Stacked missile bonuses (kit CLAB + baked op167/286 + +2 bow/arrows). |
| **Khalid** | Fighter / Vanguard (AK) | 6/8/5/4 | BG1-SoD | Premier BG1/SoD anchor; gone at SoA start. |
| **M'Khiin** | Shaman, no kit | 5/6/7/5 | SoD | Generous 6/6/4 slots + free spirit summons; strongest SoD support. |
| **Kagain** | Fighter / Dwarven Defender (AK) | 5/9/4/7 | BG1 | Elite dedicated tank (stun+displacement immunity); offense-light. |
| **Garrick** | Bard / Troubadour (AK) | 3/3/8/3 | BG1 | Song of Healing + movement-impair immunity = strong support; squishy. |

### B tier — Balanced (sits on the intended curve)

| Companion | Class / Kit | Off/Def/Util/Scl | Scope | Note |
|---|---|---|---|---|
| **Neera** | Mage / Wild Mage | 8/7/7/9 | Full | Full mage power; Wild Mage kit is fair-to-slightly-risky, not an outlier. |
| **Nalia** | Mage/Thief, no kit | 7/6/9/7 | SoA-ToB | Best versatility (learns any scroll) at average raw power; squishy. |
| **Branwen** | Cleric / Priest of Tempus (mod) | 5/6/8/8 | Full | Full divine toolkit; mild flavor kit; pure backline support. |
| **Viconia** | Cleric/Thief (converted) | 6/8/7/6 | Full | DEX19 + Drow MR + full SR cleric + stealth backstab niche. |
| **Haer'Dalis** | Bard / Blade | 7/6/7/5 | SoA-ToB | Spin burst + tiefling resists; +2 weapon cap & L6 spell ceiling brake. |
| **Jaheira** | Fighter/Druid, no kit | 6/7/6/6 | Full | Textbook durable multiclass; 2-pip cap and split XP keep it baseline. |
| **Tiax** | Cleric/Thief, no kit | 4/5/8/6 | BG1 | Classic Swiss-army support; weak offense; mid baseline. |
| **Safana** | Bard / Abettor of Mask (AK) | 4/5/8/6 | SoA-ToB | Thief-song support + anti-mage spells; deliberately weak offense. |
| **Valygar** | Ranger / Stalker | 6/6/6/5 | SoA-ToB | Solid B-tier scout/frontliner; underrated Stalker innate package. |
| **Voghiln** | Bard / Skald | 6/4/7/5 | SoD | Always-on party buff + arcane utility; fragile. |
| **Glint** | Cleric/Thief, no kit | 3/5/8/4 | SoD | Pure utility/support; trap 70 + divine; weak combat. Appropriately costed. |
| **Dynaheir** | Mage / Invoker | 7/2/6/4 | BG1 | Glass-cannon specialist; well-costed (4 HP at L1). |
| **Xzar** | Mage / Necromancer | 6/3/6/2 | BG1 | Fine early controller; limited by availability, not kit. |

### C tier — Below-average (buff candidates; see §2)

| Companion | Class / Kit | Off/Def/Util/Scl | Scope | Note |
|---|---|---|---|---|
| **Cernd** | Druid / Shapeshifter (AK Overhaul) | 6/6/7/6 | SoA-ToB | Rescued kit but structural single-class cast-or-shift drag; late join. |
| **Fade** | Fighter/Thief (converted) | 6/5/8/6 | SoA-ToB | High utility but STR14/CON10 glass; backstab unreliable vs SCS detection. |
| **Xan** | Fighter/Mage / Eldritch Knight (AK) | 5/7/6/4 | Full | Frail gish; EK -1 slot/lvl double-dips on multiclass lag. |
| **Kivan** | Ranger, no kit | 6/6/5/4 | BG1 | The only un-kitted ranger; scattered 2-pip profs; outclassed by peers. |
| **Faldorn** | Druid, no kit | 5/4/6/6 | BG1-SoD | Spellbook saves her; bare-bones stats; plain true-class. |
| **Rasaad** | Monk / Sun Soul | 5/6/3/6 | Full | DEX16 kills the monk's AC identity; fire-typed nukes matchup-dependent. |
| **Skie** | Thief / Swashbuckler (AK) | 4/6/4/5 | BG1-SoD | Built as 1-APR shortbow user; fights its own duelist kit. |
| **Eldoth** | Bard, no kit | 4/4/6/5 | BG1 | DEX12 cripples his archer build; ~4 spells on join. |
| **Yoshimo** | Thief / Bounty Hunter | 5/4/6/2 | SoA *(temp)* | Serviceable early rogue; guaranteed departure caps scaling (by design). |
| **Alora** | Thief, no kit | 3/5/6/3 | BG1 | Malformed skill build (0 stealth/detect illusion); combat-irrelevant. |
| **Montaron** | Fighter/Thief, no kit | 4/4/4/2 | BG1 | Broken skill allocation (0 locks/traps); all-mundane gear. |
| **Wilson** | Fighter / Grizzly Bear | 6/4/1/3 | SoA-ToB | Gear-locked +2 claws + frozen AC2 + no Free Action; can't scale. |

### D tier — Underpowered (clear buff candidate)

| Companion | Class / Kit | Off/Def/Util/Scl | Scope | Note |
|---|---|---|---|---|
| **Sarah** | Ranger / Feralan (AK) | 4/4/3/2 | SoA-ToB | Live kit ≠ intended "Archer"; fires NORMAL arrows; **ToB CRE level byte stuck at 7** despite 1.2M XP — mechanically frozen. Worst on every axis. |

---

## 2. Weakest — "would-never-take" (buff candidates)

Ordered roughly weakest-first. Each entry gives the conservative, SCS-style buff direction
already identified in the per-companion analysis. The recurring theme: **broken stat/skill/level
data and missing-kit gaps**, not under-tuned class design.

### Sarah — Ranger/Feralan *(the clearest buff target)*
1. **BUG FIX (essential):** set `K#SARAH1` (ToB) level byte to match its 1.2M XP (~L12) and
   resync HP/THAC0 — she is otherwise a frozen L7 char sitting on unused XP.
2. Refocus proficiencies into one build: Long Bow 3-4 (Mastery/High-Mastery for AK APR) + 2
   Two-Weapon; drop the wasted Two-Handed style.
3. Replace NORMAL arrows with +1/+2 ammo and add one magical melee weapon (she currently cannot
   hurt weapon-immune SCS foes — ammo enchant, not launcher, governs bypass).
4. If recruited mid-SoA, nudge join XP toward party curve (~150-300K) instead of 89K.

### Wilson — Fighter/Grizzly Bear
1. Scale claw enchant with level (+3 late SoA, +4 ToB) — he is hard-locked out of all gear and
   stalls vs PfMW/high-AC.
2. Grant innate **Free Action** (thematically a bear shrugs off web/hold) — his single biggest gap.
3. Level-gated natural-AC bonus so his tankiness rises instead of being frozen at AC 2.
4. Optionally unlock one accessory slot (drop one op181) for minimal gear participation.

### Alora — Thief, no kit
1. Reallocate skills so she actually has Hide/Move-Silently (shift ~30-40 pts from the redundant
   PickPkt/OpenLock surplus) — her x3 backstab is currently dead weight.
2. Add a ranged pip (Sling/Short Bow) + a sling so she contributes chip damage on Insane.
3. Optional single Detect Illusion investment. Keep DEX19 + Rabbit's Foot identity.

### Montaron — Fighter/Thief, no kit
1. Root-cause: re-spread T-level points to give functional Open Locks + Find/Remove Traps (he has
   zero of both) — pull from over-stacked Pick Pockets/Move Silently.
2. Optional Two-Weapon Style pip + a +1 short sword (or move his wasted Sling spec onto Throwing
   Axe). Keep lean scout HP/STR/CON.

### Eldoth — Bard, no kit
1. Assign a kit consistent with the modpack pattern — **Skald** (party War Chant) or Blade.
2. Fix DEX 12→16 (his AC and archer ranged THAC0 both depend on it).
3. Flesh out the starting L5 bard book (Blur, Mirror Image, Invisibility, Glitterdust/Web, Slow).

### Kivan — Ranger, no kit
1. **Assign a thematic kit** — Stalker (vengeance-hunter: stealth + mage spells + backstab) or
   Archer; smallest change, biggest balance return, matches the install's NPC-kit philosophy.
2. If kept kit-less, consolidate profs into Long Bow ***/**** + one melee line.
3. Optionally ensure he actually receives his L8 ranger priest spells under SR.

### Skie — Thief/Swashbuckler (AK)
1. Give real melee weapon specialization (2 pips finesse weapon + 1-2 style pips) so Fighter
   THAC0 + Insightful Strike fire — the single biggest lift.
2. Hand her a thematic finesse sidearm in SoD so she isn't a pure archer.
3. Strip the dead SPCL412 (Set Snare) and unusable stealth points. Leave DEX18/INT15/kit alone.

### Rasaad — Monk/Sun Soul
1. **DEX 16 → 18** — highest-impact, lore-appropriate fix; restores the monk AC/missile bonus
   that defines the class.
2. STR 16 → 17 (or small exceptional %), or a modest +THAC0 / +1 fist-enchant on his bracers.
3. Let Sun Soulray/Soulbeam deal half damage as untyped/magic so it lands vs fire-immune SCS foes.

### Xan — Fighter/Mage / Eldritch Knight (AK)
1. **Remove or halve the EK -1 slot/level penalty** — it double-dips with the multiclass lag and
   is the biggest drag on his arcane contribution.
2. CON 7 → 12-14 (a -1 HP/level frontliner is brutal on Insane), optionally STR 13 → 15.
3. Broaden his known book so it reliably reaches the L6 control/defense staples (Stoneskin,
   Improved Invis). Leave Edwin as the clear arcane king.

### Fade — Fighter/Thief (converted)
1. STR 14 → 16 (removes dead-stat penalty) and CON 10 → 13-14 (~+15-20 HP) to survive focus fire.
2. Optionally Short Sword Mastery (3 pips) for +½ APR.
3. Add a reliability tool that doesn't depend on stealth detection (1/day Improved Invisibility /
   Shadowstep) rather than buffing raw numbers. Keep the glass-cannon-rogue identity.

### Cernd — Druid/Shapeshifter (AK Overhaul)
1. Modest stat repair for the late underleveled join: CON 13→15 and/or DEX 9→13 (one-tome
   equivalent). Do NOT touch WIS 18.
2. Nudge SoA join XP band up toward the other SoA joiners' floor (~180-200K).
3. Fix shipped memorization to lead with Iron Skins + summons so he is combat-ready on recruit.
4. Verify Shapeshifter Overhaul claw THAC0/APR/enchant scale into ToB.

### Yoshimo — Thief/Bounty Hunter *(intentionally capped; no buff recommended)*
Below-average is by narrative design (guaranteed departure at Spellhold). Listed for completeness;
**no rebalance** — any investment is lost when he betrays the party.

---

## 3. Strongest — nerf candidates

The five S-tier units are the priority. Several A-tier kits carry one or two outlier levers worth
trimming if the remix wants tighter SCS parity. All directions are conservative and
flavor-preserving.

### Sarevok — Fighter (ToB-end) **[top priority]**
The joinable redeemed Sarevok permanently wears the **undroppable boss invulnerability package**
(INVULNER ring + CHWRAITH amulet; flags 0x68, usability 0) and the join dialog never strips them.
Result: 100% immunity to all damage types and all spell levels, 100% MR, immune to every major
disabler — unkillable on any difficulty — on top of GM 2H + Deathbringer 200-dmg/stun proc.
- **On join, strip INVULNER + CHWRAITH**, replace with reasonable endgame protection (~40-50%
  physical resist + Free Action, or a Ring of Protection +2 / normal amulet).
- Keep GM 2H, Sword of Chaos +2, 204 HP.
- Convert Deathbringer Assault's flat 200-dmg proc to a save-vs-death with modest proc chance
  (SCS instant-death treatment). *(Recommend a 30-sec EEex check that the items persist live first.)*

### Edwin — Mage/Red Wizard (AK)
Slot-fixes already applied (Fixpack #400 + amulet fix). Remaining outliers are the AK kit levers:
- **op191 caster-level +5 is the biggest outlier** — cap at +2, or scale +1 per 5 char-levels
  (max +3 in ToB).
- Cap the op346 enemy save-penalty at -2 and/or make it school-limited/short.
- Optionally drop CLAB C0REDW4 to +1 slot on odd spell levels (net ~+1.5/level).
- Leave INT/CON, spell selection, and the SCS sequencer innates intact — only magnitudes are over.

### Hexxat — Thief/Invisible Blade (AK), vampire
- **Trim OHHEXAM1's blanket immunities** to thematic vampire ones (charm, level-drain, sleep,
  disease, poison, fear) and **remove unconditional Hold/Paralysis (op175/109)** + any maze/psionic
  immunity — leave at least one hard-CC vector open. Or gate the strongest immunities behind
  "vampire form active" with the sunlight penalty live.
- Lower vampire stats STR20/DEX20 → STR19/DEX19 (removes the maxed +8 dmg / -4 AC outlier).
- Keep Domination but confirm SCS save scaling and hold to once/rest.
- Optional purist: cap dagger pips at Specialization (but Mastery is the kit identity — do amulet/
  stat trims first).

### Pai'Na — Druid/Hive Mother (AK)
*(Verify the empty CRE known-innate list actually bakes the GA_ innates first — if not, she may
land at merely "strong".)*
- **Biggest lever:** trim the L15/18 blanket disabler-immunity to a subset (keep poison/web/sleep;
  drop blanket charm/confusion/hold/stun/maze/paralyze — let her use Chaotic Commands/Free Action).
- Gate Cloudkill + Monster Summoning IV to ~1/day and unlock later (L11+/L13+); consider dropping
  Animate Skeleton Warrior (off-theme).
- Drop Widow's Kiss to +1 slot at levels 1-3 only (or remove) so she doesn't out-cast priests.
- Keep spider forms + Spiderskin + Poison Weapon as the signature identity.

### Baeloth — Sorcerer (BG1/SoD) *(per task — include)*
For the BG1/SoD tier he is the strongest arcane option by a clear margin.
- **Primary lever:** trim the known-spell list to a normal sorcerer progression for his level
  (~L7 = 5/4/3 known instead of 8/6/5). Edit known-spell entries in BAELOTH/BAELOT7, keep signature
  picks (Magic Missile, Mirror Image, a nuke).
- MR 50 is iconic drow flavor — prefer to keep, but if still hot, scale it (MR30 BG1 → MR50 SoD)
  so the anti-magic wall ramps with the tier. Leave slots/day and stats untouched.

### A-tier outliers worth a light trim (only if they play as over)

- **Dorn** (leans OP): STR 19 → 18/00; if Poison Weapon dominates, gate it behind save-vs-poison
  at -2 — but do that in the AK kit globally (affects all Blackguards).
- **Wings:** scale join XP to party / cap to encounter level (the fixed 2.5M is the real problem);
  drop Short Bow GM → Specialized; trim launcher +4 → +2/+3 and arrows +2 → +1 for the SoA CRE.
- **Corwin:** delete or halve the redundant baked op167/op286 missile bonuses (the kit CLAB already
  escalates missile THAC0/dmg); or drop Longbow GM → Mastery; or ship +1 arrows.
- **Minsc:** the Rage immunity list is over-broad — drop **maze (213) + level-drain (216)** while
  keeping stun/charm/fear/confusion/hold/feeblemind; optionally 10rd → 5-6rd. Power-neutral feel
  swap: allow true Grandmastery in 2H Sword + reassign the wasted Single-Weapon pips.
- **Ajantis:** drop the C0DC04 +1-all-saves HLA (paladin saves are already best-in-game); move one
  C0FIG passive off L1; optionally trim divine casting to L3.
- **Imoen:** push Trickster Evasion L7 → L9+ (Shadowdancer timing); audit Tricks illusion sub-spells
  so they don't grant SI:Divination / permanent true-invis; cap the cumulative thief-skill passive.
  Do NOT touch mage progression — the multiclass tax already balances her.
- **Kagain / Khalid:** the **Vanguard/DD defensive stack** (hard stun + displacement immunity +
  Defensive Stance 50% all-damage resist) is arguably over-tuned for an attrition remix. Pick at
  most one: cap Defensive Stance resist ~40%; make stun immunity a +4 save bonus instead of hard
  immunity. Both share the AK kit, so changes hit all kit users.
- **Yeslick:** only if it feels over — convert LK#Y2's "set STR to 18" to a +2/+3 bonus and/or
  shorten its up-to-20-min duration. Leave saves/casting (the F/C identity).
- **Bristlelick:** STR 19 → 18/91-00; halberd ench-3/+2/+2 → +1/+1; Provoke save penalty -5 → -2/-3.
- **Coran:** DEX 20 → 19 (elf max, near-invisible trim). Minimal action needed.

---

## 4. Methodology & caveats

**Difficulty assumption.** Every verdict is judged for **Insane + SCS + SR** on *this* modded
install — not vanilla, not a no-mods run. "Strong" means strong against smart-AI enemies with
doubled incoming damage, layered mage defenses, and heavy save-or-die/CC pressure. A companion's
value is weighted toward what counters that meta: CC-immunity, anti-magic (Dispel/Breach/Spell
Thrust/True Sight), self-protection, and reliable accuracy/penetration vs inflated AC/HP.

**Data source.** Scores derive from the **live CRE/2DA/ITM/SPL binaries** as actually installed
(post AK + CDTweaks + SCS + SR), i.e. the files the player fights with — not mod readmes or
vanilla references. Where a kit's behavior depends on CLAB application at level-up, that is noted.

**Scope conditions Scaling.** EET departs most BG1 companions at the SoD/BG2 transition and SoD
companions at the SoA transition. A low Scaling score frequently means "content window ends early,"
**not** a design flaw (e.g. Coran, Dynaheir, the SoD crew). Conversely, fixed-high-XP CREs (Wings)
or invuln gear (Sarevok) inflate raw power within a narrow window.

**Recurring finding.** The buff list is dominated by **broken data, not weak design**: malformed
thief-skill allocations (Alora, Montaron), a frozen level byte (Sarah), wrong/missing kits (Kivan,
Sarah), and double-dipping penalties (Xan EK). Fixing these is the project's highest-leverage work.

**Open verification items (do before building nerfs):**
- Confirm INVULNER + CHWRAITH persist on the live Sarevok party member (data says yes).
- Confirm Pai'Na's GA_ innates actually bake (empty CRE known-innate list, 12 reserved slots).
- Confirm Sirene's kit arcane spellbook populates in-game (CRE carries no known mage spells —
  same pattern as the already-fixed Aura/Safana bard-spell bug).

**Out of scope.** Cross-class party synergy, item/economy balance, and encounter tuning are covered
in the encounter (`02*`), XP (`03`), and creature-danger (`06`) research docs. This audit ranks
companions in isolation against the difficulty baseline.
