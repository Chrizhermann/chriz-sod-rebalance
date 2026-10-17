# Drasus and Chosen of Cyric: questions for the Ashatiel brawl

Read-only reference audit, 2026-09-26. No proposed spell, item, level, AI package,
or difficulty tier in this note is a user-approved addition to Ashatiel's group.
The purpose is to identify the decisions worth discussing, not import either
reference encounter wholesale.

## Evidence and limits

- Effective resource source: `%USERPROFILE%\CEBG-Tests\Combined-20260908\game`.
- SCS source there is version 35.21. `WeiDU.log:239–245` records innate
  sequencers/contingencies, AI initialization, general AI, calls for help,
  smarter mages/priests and NPC potions. Line 276 records **7110, Improved
  Drasus party**. Thus the Drasus encounter component is actually installed.
- Current CREs, assigned BCSs, spell resources and English TLK were read. Scripts
  were decompiled only in a separate synthetic scratch game; no command used the
  source installation as its write/decompile target.
- Reproducible capture, effective resource SHA-256 values, creature spell/item
  inventory and decompiled scripts are under
  `%USERPROFILE%\CEBG-Tests\Ashatiel-20260926\drasus-reference\`.
  `capture.json`, `capture.py`, and `spell_probe.py` provide the evidence.
- No game was launched. Runtime fine-tuning settings and active save state were
  not read. A supported preparation branch is not proof that a current save
  selects it. The current installation also contains Spell Revisions, Artisan's
  Kitpack, Item Randomiser and other mods: these are effective installed actors,
  not unmodified SCS fixtures.
- Chosen of Cyric source evidence is in
  [the existing RR audit](24c-chosen-of-cyric-reference.md). Its older opening
  discussion is superseded by the [current brawl design](../design/wave1/09-ashatiel-party-brawl.md):
  player reset, enemies already hostile/prepared, attack early if approached,
  otherwise advance after preparation; no literal enemy dispel/rest is required.

## What SCS actually changes specifically for Drasus

`stratagems/tactical_bg1/drasus.tpa:3–9` is small: it adds two levels to Drasus,
Genthore, Kysus and Rezdan, enforces their class statistics, and adds a Magic
Shielding potion and a Frost Giant Strength potion to Drasus. It does not contain
a bespoke four-person spell rotation or an enormous encounter-specific buff list.

The sophistication mostly comes from other installed systems:

- `stratagems/genai/genai.tpa:109–121` repairs Genthore's loadout to throwing axes
  and a melee battle axe. The following area patch prevents NPC use of the mine
  travel regions so Rezdan does not leave the fight through an area exit.
- `stratagems/genai/kit_override/bg1/berserker.2da` assigns Drasus a berserker role.
- `stratagems/mage/override/bg1/kit.2da:2–3` assigns **Kysus Conjurer** and
  **Rezdan Enchanter**, giving two casters different emphases.
- `stratagems/help/help.tpa:324–335` assigns all four the same help group,
  `specifics=90`, and the group shout script. Their effective override slot is
  indeed `DW#GPSHT`.
- Generated combat scripts handle ordinary spell selection, movement, defenses,
  potions and attacks. Their resource names are install-specific.

The useful example is a coherent four-person party improved through roles,
usable equipment and competent AI, with a relatively modest encounter-specific
power increase.

## Effective roster and equipment

Names below are resolved from this installation's item/spell resources and TLK,
not guessed from vanilla resource numbers. HP and levels are base CRE values;
equipment, runtime effects and difficulty can modify combat statistics.

| Actor | Effective base | Relevant current gear and resources | Assigned combat AI |
|---|---|---|---|
| Drasus | Fighter/berserker, level 10, 80 HP | Morning Star +1, chain mail, medium shield; two Frost Giant Strength potion entries, one Magic Shielding potion entry; SCS random-potion tokens | `DW1MELBE` |
| Genthore | Fighter, level 9, 70 HP | Fallorain's Plate +1, large shield, two stacks of five throwing axes, battle axe; SCS random-potion tokens | `DW1RANGE` |
| Kysus | Conjurer, level 11, 68 HP | Traveler's Robe, throwing daggers/dagger, Fire Shield scroll; SCS random-potion tokens | `DW#MG553` |
| Rezdan | Enchanter, level 9, 56 HP | Mage Robe of Cold Resistance, darts, quarterstaff; SCS random-potion tokens | `DW#MG554` |

Do not turn the placeholder `DW#RND*` resources into a claimed fixed potion list;
the final spawned inventory depends on their random allocation machinery. A
scroll carried as loot is also not proof that the combat AI casts it.

The current Drasus CRE has Artisan's `C0BER#00` Enrage memorized three times,
plus `C0FIG01` Power Attack. The effective generic berserker script instead has
`HaveSpell(BERSERKER_RAGE)` / `Spell(Myself,BERSERKER_RAGE)` at lines 853–877,
while current `SPELL.IDS` resolves that symbol to 4321 (`SPCL321`). That is a
static spell-identity mismatch worth remembering when designing kit support.
This bounded audit did not establish any runtime bridging mechanism or test rage
in the engine; do not advertise his kit powers as working merely because the
CRE and generic script separately contain them. No unrelated fix was attempted.

## What their prebuffing can actually contain

These are the full relevant preparation branches present in the two effective
mage scripts, **not a promise of all buffs on every difficulty**.

| Mage | Long preparation branches | Additional short preparation branches |
|---|---|---|
| Kysus | Shield; Protection from Missiles; Stoneskin | Mirror Image; Shadow Door; Minor Globe of Invulnerability; Spell Deflection |
| Rezdan | Mage Armor; Stoneskin | Mirror Image; Minor Globe of Invulnerability |

Evidence: effective `DW#MG553.baf:380–643`, `DW#MG554.baf:418–533`.
The `dwsw*` preparation helpers' actual displayed names were checked against
their SPL resources, including the SR Stoneskin resource `dwsw408`.

There are several important qualifications:

1. **Prebuffing is separately configurable.** SCS distinguishes mage AI
   difficulty, prebattle-casting difficulty and other settings. Script checks use
   `DMWW_mage_difficulty`, `DMWW_mage_prep_difficulty`, engine difficulty and
   whether a creature was created out of sight. The source INI file alone does
   not prove what the player selected in an active game.
2. **Being out of view is not always sufficient to prepare.** Short buffs usually
   require enemy sight or an explicit `offscreenprep` flag. In these generated
   scripts Stoneskin still has an explicit `See(NearestEnemyOf(Myself))` check.
   An Ashatiel staging routine must deliberately prepare the chosen enemies;
   merely putting them red behind a tent does not guarantee completed buffs.
3. **Preparation normally costs spells.** Mirror Image, Shadow Door, Minor Globe,
   Spell Deflection, Shield, Protection from Missiles and Mage Armor preparation
   remove the corresponding memorized spell. The Stoneskin preparation block is
   an explicit exception here: it does not remove a memorized copy. It represents
   long-lasting advance preparation, leaving an ordinary Stoneskin for combat.
4. **There is no fixed offensive rotation.** Generated scripts are priority
   trees with target protections, spell availability, casting failure, range,
   cooldown and sometimes weighted-choice checks. Reading the spellbook does not
   tell us which spell will be cast first.

The SCS 35.21 readme describes the preparation ladder as: none at Basic;
several-hour defenses at Improved; longer defenses at Tactical; increasingly
shorter defenses at Hardcore/Insane, with in-sight/out-of-sight distinctions.
That is a useful separation of difficulty controls, not an agreed Ashatiel ladder.
Source: `stratagems/doc/readme-stratagems.html:846–876`.

## Combat resources, recasts and openings

Kysus carries three ordinary Mirror Images and one ordinary Stoneskin. At maximum
preparation, one Mirror Image is spent on opening preparation; the remaining
copies can support later defensive recovery. Rezdan carries one Mirror Image
and one Stoneskin, plus a defensive Minor Sequencer containing **Mirror Image +
Blur**. Kysus instead carries an offensive Minor Sequencer containing **two
Color Sprays**. The sequencer payloads were checked through their opcode-146
subspell references; these names are the effective SR installation's names.

The examples illustrate distinct emergency/offensive roles, not suggested
packages for Ashatiel:

- `DW#MG553.baf:2934–2969` and `DW#MG554.baf:2761–2794` recast Stoneskin when
  skins are almost gone, an enemy is close, a spell remains and casting/redefend
  timers allow it; Mirror Image also requires absent images and low skins.
  They use ordinary `Spell` actions, a one-round casting timer and a seven-second
  defense-recast timer. Their finite remaining spellbooks matter.
- Rezdan's sequencer (`DW#MG554.baf:2744–2759`) is a defensive reaction to
  low skins and missing Mirror Image, not automatic opening damage.
- Kysus's sequencer (`DW#MG553.baf:7004–7029`) requires a visible nearby target,
  no nearby ally and a target without the checked incapacitation/Minor Globe
  conditions. It therefore may not fire just because he owns it. It uses a
  sequencer helper plus two forced Color Sprays; this is explicitly scripted
  delivery, not ordinary sequential spellcasting.
- Both have Vocalize logic when silenced, but still require an available spell
  and an acceptable spell-failure state.
- Both have their own offensive spell emphasis: Kysus carries several summon
  spells, Slow, Greater Malison and Lightning Bolt; Rezdan carries Dire Charm,
  Hold Person, Ray of Enfeeblement and Chaos. This is role differentiation,
  not justification to give every caster every strong disable.
- Drasus's defensive potion AI requires actual inventory and spends `UseItem`
  actions under the same one-round timer (`DW1MELBE.baf:764–793`). His giant
  strength potion logic additionally checks strength and enemy proximity
  (`:1274–1305`). Items in a CRE do not all appear as simultaneous free prebuffs.

## Team engagement and the arena boundary

All four have the group-alert override. `DW#GPSHT.baf:36–94` shouts on seeing an
enemy and propagates hostility to members of the same group under the applicable
AI difficulty conditions. This is the mechanism that makes approaching one
opponent engage a party rather than permit four isolated pulls.

For the brawl, the useful question is narrower: **which actors may answer the
alert?** The agreed northern party must stay separate. Reusing a broad vanilla
Crusader help group would risk drawing unrelated siege actors into the sealed
arena. The brawl needs a deliberate group boundary and an early-approach trigger
that releases the whole agreed opposing party, plus the timed advance if the
player waits.

Likewise, enemy movement should use the arena rather than a global chase/escape
system. The Drasus source already treats blocking Rezdan's area exit as part of
keeping his encounter coherent. Ashatiel must keep room for repositioning and
hiding while making its wooden barricades genuinely block escape.

## What to borrow as questions from Chosen of Cyric

The [RR source audit](24c-chosen-of-cyric-reference.md) provides concrete examples:

| Pattern | Actual reference | Question for each Ashatiel member |
|---|---|---|
| Distinct roles | Assassin, barbarian, ranged attacker, arcane caster, hybrid, priest | What does this person contribute that another member does not? |
| Visible preparation | Individual potions, protection and buff actions in `rr#camb2.baf` | Which defenses are core to this role, and which would merely erase weaknesses? |
| Limited recoveries | Venduris uses real invisibility/healing potions and exits recovery when inventory is exhausted | How many recoveries, when, and what is the player's opportunity to stop them? |
| Ally support | Kerith checks disabled allies before Remove Paralysis; Selina can haste particular damage dealers | Which one or two teamwork relationships matter, and do they cost an action/spell? |
| Separate packages | Selina has separately guarded opening, emergency and offensive sequences | Is a package an opening move, an emergency tool or an ordinary cast; can it happen only once? |
| Explicit completion | Dedicated all-members-defeated check before exit cleanup | How does the encounter resolve if Ashatiel falls first or another enemy is charmed/disabled? |

RR is not a universal fairness template: its original opening gives the enemies
an advantage and strips the player's preparations; its ranged dispelling-arrow
assists include forced effects without an ammunition check. Neither belongs in
our design just because CoC uses it. Its high-level Chain Contingency, Improved
Haste, Protection from Magical Weapons, Greater Malison/Slow/Chaos sequence and
retreat-to-traps behavior should not become the assumed SoD baseline.

## Discussion checklist, with no packages selected

For each Ashatiel-group character, record these before implementing:

1. **Identity and job:** class/kit, level, principal weapon or spell role, and
   current behavior we want to preserve.
2. **Opening defenses:** what protects them from immediately folding, what
   weakness remains, and how long each defense lasts after the 30-second wait.
3. **Action budget:** which buffs are already active, which spells/consumables
   that preparation spends, what remains for battle, and whether allies supplied
   any protection. A long list of buffs is also a resource-allocation decision.
4. **Main pressure:** attacks, one distinctive spell family, ranged disruption,
   support or control. Avoid simultaneously maximizing every axis.
5. **Emergency behavior:** a finite heal, recast, potion or sequencer; thresholds,
   normal casting vulnerability, cooldown and maximum uses.
6. **Counterplay:** something the player can remove, interrupt, resist, outlast,
   position against or exploit by targeting a support member.
7. **Team interactions:** specific ally assistance and a bounded shared alert.
8. **Equipment versus rewards:** combat loadout, weapon enchantment/ammunition
   requirements, which consumables are used, and which surviving items drop.
9. **Difficulty:** tune selected resources, opening packages or timing instead
   of assuming every actor needs all of them. Keep coherent roles across tiers.
10. **Compatibility and tests:** resolve actual SR spell identities and kit
    abilities; inspect the final CRE/script pairing; test early approach, timed
    engagement, rest/reset, a defensive recast and completion in the real arena.

The first design conversation can use the factual Ashatiel roster audit as its
baseline and work through one character at a time. Neither Drasus nor CoC
determines our final roster, defenses or difficulty numbers.

## Follow-up: kit decoding and Zoe's armor helpers

The CRE kit field at `0x244` needs its two 16-bit words swapped before a
`KIT.IDS` lookup. This is verified against SCS's `CRE_read_kit` in
`stratagems/sfo/sfo_autofunc.tpa:11886–11890` and `reverse_long` in
`stratagems/sfo/general/lib_tools.tpa:591–604` (word swap, not byte reversal).
Current effective resources resolve as follows:

| Creature | Raw bytes | Normalized kit ID | Verified kit |
|---|---|---|---|
| BDASHA01 | `00400000` | `0x40000000` | Barbarian |
| BDASHA02 | `00000004` | `0x00000400` | Illusionist |
| BDASHA03 | `00000440` | `0x00004004` | Cavalier |

Zoe (`BDASHA04`) is an un-kitted fighter/thief with base Hide in Shadows 0
(`0x45`). Her LEAT05 armor's indirect helpers provide no hidden route to 150:
`c0ivbp3.eff` is a -99 Backstab modifier (opcode 263), applied only to the Invisible
Blade kit; `C0ARCAS3.eff` protects Eldritch Knights against `C0ARCAS1`; and
`C0ARCAS1.eff` disables wizard casting (opcode 145). None increases Hide in
Shadows or recursively casts a spell that does. The kit filters are visible in
the current ITM and in Artisan's `Invisible_Blade.tpa:295–308` and
`Eldritch_Knight.tpa:211–234`. Opcode meanings were cross-checked against
[IESDP](https://gibberlings3.github.io/iesdp/opcodes/bgee.htm#op263).

This closes the named equipment-helper uncertainty, not every possible live
source of skill bonuses. Do not promise that a native branch requiring Hide in
Shadows >=150 works for her. It also does not prove all potential invisibility
or backstab routes are impossible. Probe code and output are in the same scratch
directory as `kit_zoe_probe.py` and `kit-zoe-probe.txt`.
