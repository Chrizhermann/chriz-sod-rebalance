# Ashatiel: fair reset and arena boundary feasibility

> **Subsequent user clarification:** the reset is for the player party; the
> enemies do not need a literal dispel/rest procedure. They start present,
> hostile and prepared out of sight, reacting to early contact or advancing
> after a few rounds. Preserve the research below as mechanism evidence; the
> [current design](../design/wave1/09-ashatiel-party-brawl.md) governs staging.

Research date: 2026-09-26. No encounter implementation or live-game actions.
The initial research brief requested an **agreed party brawl**, with both sides
dispelled/rested before preparation. The later clarification above limits that
reset to the player party. Substantial enemy prebuffing and visible wooden
barriers preventing escape remain intended; the solo duel and refusal/ordinary
battle stay available. The earlier preserve-existing-buffs brief is superseded.

This note establishes technical constraints, not an approved spell package,
roster, arena location, or definition of every reset edge case. See the
[current design](../design/wave1/09-ashatiel-party-brawl.md),
[sequence audit](24a-ashatiel-sequence.md), and
[map research](24-ashatiel-map-triage.md).

## Read-only evidence

Effective resources read from
`%USERPROFILE%\CEBG-Tests\Combined-20260908\game`:
`ACTION.IDS`, `SPELL.IDS`, `BD4000.ARE`, `BDREMOVE.SPL`, `SPIN746.SPL`,
and `BDDELEN1.SPL`. The resource extractor reads override/KEY/BIFF bytes directly;
no WeiDU operation targeted the game. The parsed evidence is
`%USERPROFILE%\CEBG-Tests\Ashatiel-20260926\reset\resources.json`.

Historical decompiles were used only as source-pattern evidence. The current
project's own `chriz-sod-remix/baf/csrkorlb.baf:16-25` is also relevant.

## Rest is feasible, but define the reset in separate steps

The installed IDS exposes `Rest()` (96), `RestParty()` / `RestPartyEx()` (230),
and `RestNoSpells()` (243). Per-actor `Rest()` restores resting benefits without
advancing game time or showing a rest movie. `RestParty` has different party-wide
rest semantics. A short preparation scene should therefore be prototyped with
per-participant `Rest()`, rather than assuming an ordinary eight-hour party rest
is harmless during the siege. [IESDP action reference](https://gibberlings3.github.io/iesdp/scripting/actions/bgeeactions.htm#96)

SoD already uses `ActionOverride(Player1..Player6,Rest())` in `BDCUTJEG` and
`BD0103`; its separate `AdvanceTime` actions are visible in those scripts.
This is useful native precedent for party iteration without a rest UI.
Korlasz's existing Remix AI explicitly applies `RESTORE_FULL_HEALTH` before
`Rest()`. Use that separation as the prototype: spell/ability restoration and
full HP should each have an acceptance check, rather than calling Rest and
assuming every requirement was satisfied.

The current `RESTORE_FULL_HEALTH` ID is 3746, resolving to `SPIN746.SPL`.
Its effective three effects cast `#CUREDIS`, cast `#CUREPSN`, and apply an
HP effect with parameter1=100 and parameter2=2. These are install-shaped
resources, so this probe is not a claim about every SR/vanilla installation.
The helper is a useful reference, not an automatic approval to inherit all its
cures into the new reset.

Recommended staging dependency, still not implementation:

1. Accept only the new agreed-brawl dialogue branch; mark setup in progress once.
2. Secure the arena and stage its participants before allowing attacks.
3. Remove the agreed prior temporary effects, then restore living participants'
   HP and rest resources.
4. Establish enemy preparation and release player-controlled preparation.
5. Start combat after preparation; never repeat the reset on a reload or script
   re-entry.

Enemy prebuffs must follow the reset, not precede it. The two preserved dialogue
routes must never inherit this reset accidentally. The exact enemy reveal/spawn
timing relative to the approximately 30-second player preparation remains a
presentation choice.

## Fully dispelled is more than a normal Dispel Magic cast

Opcode 58's always-dispel mode removes dispellable effects without a level roll;
it does not redefine undispellable effects as dispellable. Therefore a guaranteed
normal dispel alone is not proof that every prior combat buff is gone.

Opcode 17 optionally removes limited-duration effects, retaining equipped
(timing 2) and permanent (timing 9) entries; that option also removes magical-slot
items. Opcode 321 can instead remove named-source effects, optionally limited to
the timed list. Its source filter does not distinguish an ITM and SPL sharing a
resref, and an empty source is unsafe. These offer prototype mechanisms, not a
blanket compatibility guarantee. [IESDP opcode reference](https://gibberlings3.github.io/iesdp/opcodes/bgee.htm#op17)

For AK/SR/SCS compatibility, do not call a broad effect-list wipe a dispel.
Permanent class features, equipped-item benefits, spell-slot infrastructure,
and mod bookkeeping are not prior battle preparations. Some mod infrastructure
can also live in long timed effects or child resources: timing alone is not an
authoritative buff classifier. Conversely, a buff can carry permanent ancillary
markers, so retaining all permanent entries is not proof that its whole package
was reset. This is a compatibility risk to investigate, not a reproduced AK bug.

The safe research direction is a documented reset contract plus a small tested
cleanup helper. Compare the helper against actual installed representative
resources and party state before choosing either broad timed cleanup or an
explicit set of cleanup rules. Do not reapply an entire CLAB to repair an
overbroad wipe; that risks duplicate grants and changes outside this encounter.

**Do not reuse `BDREMOVE` as the reset spell.** In the effective resource it
contains two opcode-177 external-effect applications and an opcode-168 creature
removal effect. It is not a buff dispel. `BDDELEN1` does contain always-successful
opcode 58, but also an additional removal effect; its presence proves a native
pattern, not suitability for wholesale reuse.

## Specific safeguards and unresolved semantics

| Case | Constraint / later check |
|---|---|
| Mod kits and daily abilities | Preserve learned abilities, class/kit state and slot counts. Verify native rest recharges expected innates, including any mod-specific cooldowns. |
| Consumables | Reset must not silently recreate consumed potions, scrolls or ammunition. Daily item-use recharge must be checked separately from consumable charges. |
| Long-lived buffs, potions, rage, shapeshifts | Decide which count as prior preparation. Confirm cleanup leaves ordinary equipment and natural form usable. |
| Contingencies and stored sequencers | Their storage/release abilities need a policy; generic effect removal is not proof of a clean, reusable spellbook state. |
| Poison, disease, fatigue, level drain and curses | Full HP and rest are not evidence of comprehensive status treatment. Specify the reset's cures; do not silently remove permanent story conditions or curses. |
| Dead or absent party members | A full rest does not authorize resurrection. Avoid soft-locking setup on a missing Player slot; determine how a reduced living party enters. |
| Familiars and permanent pets | Do not use a generic kill/despawn sweep. They are not interchangeable with temporary summons. |
| Prior summons, clones, traps and clouds | Clearing effects on six PCs does not clear world objects. Decide treatment explicitly; clear only owned/identified objects if needed. |
| Rest scripts and timers | No simulated eight-hour jump by default. Native rest and mod listeners still require testing for unwanted banter, script, ability or cooldown behavior. |
| Reset retry and saving | One-time setup flag, phase-aware recovery, and no repeat rewards/refills on reload. |

These are implementation requirements and unresolved boundaries; they are not a
request to burden the player with a long configuration checklist.

## Visible physical barriers are feasible without repainting the search map

BD4000 has seven existing ARE door objects, each linked to WED door data.
Doors carry separate blocked-cell lists for open and closed states; scripts can
open/close/lock them. This provides a native model for temporary physical
boundaries instead of replacing the entire search-map bitmap during play.
Visible wooden art and the collision/visibility boundary are separate pieces
that must agree. [ARE doors](https://gibberlings3.github.io/iesdp/file_formats/ie_formats/are_v1.htm#formAREAV1_0_Door),
[WED doors](https://gibberlings3.github.io/iesdp/file_formats/ie_formats/wed_v1.3.htm)

| Effective BD4000 door | Open blocked cells | Closed blocked cells | Caution |
|---|---:|---:|---|
| Door01 | 0 | 99 | Existing castle gate; current lock difficulty 100. |
| Door02 | 19 | 18 | Existing moving gate; open state still occupies cells. |
| Door03 | 15 | 20 | Existing moving gate; open state still occupies cells. |
| Door04 | 0 | 73 | Invalid/all-minus-one selection boxes; not an ordinary clickable door. |
| Door05 | 0 | 30 | Script-controlled blocker used in castle entry/breach logic. |
| Door06 | 0 | 26 | Script-controlled blocker used in castle entry/breach logic. |
| Door07 | 0 | 130 | Siege progression opens it; must not be commandeered casually. |

There is a particularly relevant native wooden-boundary precedent:
`research/data/sod_baf/BDDSWALL.baf` describes the breach as patched with wooden
planks, then opens `door04` after the Bwoosh explosion and disables the
`wall_breach` trigger. That identifies a map-art/door reference worth inspecting
for new barricade art; it does not justify moving or altering the original
breach. The historical script is not proof that an extracted/repositioned
wooden wall will render or block correctly elsewhere.

The existing scripts already open/close doors 05/06 during plot transitions and
open door07 on Ashatiel's refusal/death paths. Reusing those *patterns* is useful;
reassigning those door objects to a new arena would risk the preserved paths.
The map audit should choose the location before choosing which boundary geometry
and wooden assets can be reused or need new door/animation data.

No new wooden barricade asset or working door has been prototyped here.
Dedicated encounter-owned doors plus matching visible art are a promising
approach, not a verified runtime result. An ARE animation alone does not create
collision. A line of creatures posing as a fence creates targeting, pathing and
AI problems and is not the preferred first prototype.

Closing paths must happen only after everyone is inside; reopen on completion
and on any supported cancellation/recovery path. Make the arena boundaries
unopenable by ordinary lockpicking/Knock/bash if the no-escape rule is intended.
That property needs a real engine test, as do spells/mod movement abilities that
could cross an ordinary physical fence. Console/debug teleport is not a normal
gameplay requirement.

No-escape also does not mean no hiding. Preserve terrain that genuinely breaks
line of sight, and do not carry the solo duel's loss-of-sight cheating rule into
the new party route. Wooden barriers can block movement without necessarily
providing useful hiding cover; visual appearance alone proves neither.

## Smallest meaningful validation after design approval

- Static: compile on supported standalone/EET fixtures; phase guards; preserve
  duel/refusal branches; inspect all door and effect payloads; exercise partial
  parties and Ashatiel-first death without prematurely completing the fight.
- Native reset sample: depleted spells/innates, wounded participants, ordinary
  and undispellable buffs, one AK kit, SR spell markers, equipment and stored
  sequencer; verify full HP/resources, intended cleanup and no permanent loss.
- Native boundary sample: walk every exit/corner, test large sprites and hiding,
  check spectators remain outside, finish combat and verify reopening. Save/reload
  once during preparation and once after victory.

These are bounded mechanical tests separate from the user's later balance and
gameplay-feel test. No live acceptance is claimed by this research.
