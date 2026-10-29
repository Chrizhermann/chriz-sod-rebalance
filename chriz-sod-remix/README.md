# chriz-sod-remix

WeiDU tail-mod for the Siege of Dragonspear remix/overhaul. Research and design live in the
parent repo (`docs/`); every component ships only after explicit sign-off
(`docs/design/wave1/` carries the DECIDED/OPEN state per component).

Current release: **v0.6.16**. The component overview below describes this version.

**v0.6.16 — 290** accepts every victory remark in the vanilla shape, whoever added
it, such as Sirene NPC for BG:EE's, and shortens the pause after each one to 2
seconds like the vanilla remarks. Any other way of writing the remarks' timer
still stops 290 before anything is written. **265, 135, 140, 200, 245, 256 and
266** read their timer names from the game's own `GTIMES.IDS`, so a mod that
names a timer value differently, as Dark Tidings does for 60 seconds, no longer
stops them.

**v0.6.15 — 256** installs alongside Tweaks Anthology's "Summoned Creatures
Clear Fog of War" (`cdtweaks` 3500): the hostile bridge elementals leave its
ally-only fog clearing (`CDTFOW`) behind instead of stopping the installation.
Every other unreviewed donor effect still stops 256 before anything is written.

**v0.6.14 — 292 / 293 / 294 (EET, choose one)** hand Imoen over into Shadows of
Amn. Before the campaign switch, her SoD gear goes through EET's import rules like
the party's, and she keeps only her BG2 belt, correctly equipped. 292 (CEBG
default) makes her EET's Shadows of Amn Imoen plus her tome boosts, 293 keeps her
as taken along, and 294 (requires EEex) dual-classes her to mage at her end-of-SoD
thief level. Requires **160 + 290** and EET_end; works with 910 in either install
order. Install before leaving SoD, and raise a dead Imoen before the ending.
Lab-tested on engine 2.7.3.0.

**v0.6.13 — 198** makes Skie available in the palace hall before the
first rest. Recruit Yeslick, Branwen and Ajantis near the palace; Coran and Garrick
at the Elfsong; Kagain, Alora and Xan in the Elfsong district; Tiax in the Flaming
Fist jail; and Kivan and Shar-Teel at the Coast Way camp. Conversations are short.
Saved recruits keep their build and belongings, while fresh starts use BG1 donors
and normal SoD join XP. Previously recruited, dismissed companions move to each
later camp; unjoined companions stay behind. Known deaths prevent replacements.
Requires 110 and 197. Compile-checked on captured resources; in-game checks are
deferred to the next overall install.

The palace bedroom already permits normal resting in the inspected area data.
Use the normal Rest button to prepare spells; this addition does not reuse the
one-time story bedtime or departure choice. Its actual behavior remains a user
playtest check.

**v0.6.13 — 177** lets you report Korlasz's defeat to Liia after the
first night, including departure day, without interrupting the council. The early
and late conversations pay the same 22,000 XP to each present party member, once. A journal
reminder points to Liia until you report, including on an existing unpaid city
save. Requires **175 + 180**; append after **176** if present. It also corrects an
older 24,000 award, so installing 176 separately first is unnecessary. Previously
paid rewards stay paid. Compile checks passed; in-game verification is deferred
to the user's next overall installation.

**v0.6.13 — 285, Avernus portal and a fairer final battle,** skips the lift ride
and its battles, without replacement XP, and enters the existing confrontation
through a portal effect. Belhifet requires +1 weapons, has 60% magic resistance,
and moves 25% faster without extra attacks. His ordinary-difficulty HP targets
are 350/400/450/475/500 on Easy/Normal/Core/Hard/Insane; existing physical
resistances remain. The opening mass dispel is removed in favor of delayed,
targeted Breach. Insane starts with four devils and replenishes at most one
every four rounds; killing reinforcements frees space under the living cap.
Hephernaan retains his devil appearance while using a finite cleric/mage book,
with lighter preparation and fewer spells below Insane. No separate Extra
Challenge component is added. Install before first entering BD4700, preferably
from a save before entering the lower tower BD4600, so saved area/creature data
does not retain the old setup. Runtime balance and presentation need a playtest.

**v0.6.13 — 170/900:** relocated Korlasz jailbreak loot and Coast Way camp-chest
treasure keep the original item's identification state instead of arriving
identified. Existing chest/creature records and authored rewards are unchanged.

## Components

v0.6.11 lets **197** remove Skie's obsolete bridge appearances after **115** or
**256** has changed the victory routes. It recognizes the original two victories,
115's four branches, 256's consolidated victory and the 115/256 pair, preserving
their guards and all actions except Skie creation. If 197 is appended late,
256's guarded Bence wrap retains control. Unknown layouts still stop safely.
For an affected collection build, follow the
[recovery handoff](../docs/recovery/2026-09-16-cebg-alpha16-skie.md); do not blindly
rerun the selection or edit its install history.

**115** fixes carried Khalid's Bridgefort entry. He remains controllable while
Adirran handles the local briefing and command choices. It requires **110** and
supports installation before or after **256**. Append 115 before first entering
BD2000; use a pre-entry save if Khalid has already been reset as an NPC.

v0.6.9 additions: **135** is the default treatment of the assassin ambush
(keep the fight, remove dead magic and its misleading remarks). **235** preserves
Ymori after an older 230 installation. **265**, after 260, puts Mizhena's amulet
on the existing `Dead_fighter` corpse and removes the missed Guardian and Shadow
Aspect's Shadowed Soul summons. Fresh 230 already excludes
Ymori from its cuts. Append these components; do not reinstall earlier rows.

**256** replaces the Boareskyr Bridge barrel/portal finale. Two mages,
two veterans and four fire/earth elementals form one finite encounter. The fire
mage casts regular Haste on an elemental when he sees an enemy; both have limited
defensive recasts. Mages are level 13 below Insane and level 14 on Insane. Difficulty changes
the elemental tiers while the fixed encounter XP stays 4,520. The day/night
barrel artwork is cleaned and Bence appears beside the party after combat for
the dialogue that opens the passage. Install before first entering BD2000, either alone
or appended after an existing 255. The old 255 need not be removed. With Tweaks
Anthology's "Summoned Creatures Clear Fog of War" (3500) installed first, the
hostile elementals leave its ally-only fog clearing behind.

**v0.6.12 timer update:** fresh 256 includes a collapse clock; append **258**
to upgrade an older 256 without uninstalling it. Story Mode has no deadline.
Easy/Normal/Core/Hard/Insane allow 10/8/7/6/5 unpaused minutes, with five minutes
initially on Legacy of Bhaal. Quarter/half/three-quarter warnings appear above
the protagonist and in the log, with native rock sounds and brief shakes.
Defeating the two mages and four elementals stops the clock while surviving
guards can still fight. Failure fades to black and opens native game over.
Save/reload and ordinary difficulty changes retain the deadline. Switching to
Story Mode disables it for that encounter permanently. Prefer a pre-fight save:
an old ongoing encounter gets a fresh budget on its first update after 258.
Native presentation and timing acceptance are pending.

Optional **257 — Extra Challenge** adds only the two Insane mage sequencers:
earth uses Greater Malison then Slow; fire uses Dispel Magic with Spell Revisions,
or Remove Magic without it, then Flame Arrow. It requires **current component256
resources** and must be installed before the enemies spawn. It changes only the
two Insane mages' AI assignments, preserving stats, spellbooks, Haste, roster and
world setup. Regular 256 can cast those spells normally but never uses sequencers.

Default-selected **266** caps Shadow Aspect's Insane Mislead at one use per actor,
preserving its other spells and ordinary Shadow summons. It can be appended to
an older installation; no reinstall of 240 or 265 is required. Broader changes
to that encounter are deferred.

**197** now gives recruited Skie the normal SoD companion XP tiers based on the
protagonist's XP, with no unconditional 250,000 floor or reduction of higher XP.
It corrects the condolence/rejoin routes and makes her stock SCS invisibility
and Freedom potions movable without changing their mechanics.

Use saves from before entering BD2000, BD5000 and BD5110 for the area repairs.
Visited-area saves retain their cached actors and container contents. The
road-north award becomes 23,100 party XP and the coalition award 106,800; these
changes affect future payouts only. Liia's prologue award is a flat **22,000 XP
per character on every difficulty**. Fresh 175 already includes it; append **176**
to update an older 24,000 reward, without reinstalling 175 or changing XP already
received. The reward still occurs once, after reporting the jailbreak to Liia.

| # | Component | What it does |
|---|---|---|
| 100 | Rest-ambush 5× | Maps every active SoD rest-header day/night % through a felt-rate÷5 table (30 areas, felt 22–80% → 8–15% per rest). Composes with other mods (reads current values). BDNOREST untouched; pack size untouched (per-chapter decision). |
| 110 | Keep all companions | Neutralizes the 28 vanilla LeaveParty/DestroySelf strip blocks in BD0103.bcs; adds in-party skip-guards to 9 recruiter-area scripts so kept companions aren't yanked/converted mid-party. Mod-NPC strips untouched. |
| 115 | Khalid's Bridgefort continuity | Protects carried Khalid's party control and assigns local briefing/command choices to Adirran. Preserves the personal quest and normal non-carried route; adapts conflicting dialogue and scenes. Requires 110; install before first BD2000 entry. |
| 120 | No mid-campaign hooded man | Removes all five hooded-man appearances (palace bedside, bdcut11 vision, Boareskyr vision cameo, scrying option, Underground River cameo) + the two dangling dialogue replies. Component 290 removes the endgame chain. |
| 130 | Skip chapter dreams | Pre-sets `bd_ddd=4` from BDBALDUR.BCS — the four PLAYER1D rest-dreams never fire. Dream content documented in `docs/research/09-sod-dreams.md`. |
| 290 | Victory celebration ending | Keeps the real return and playable celebration; Dazzo ends SoD after the public victory dialogue. Removes the optional codas and murder/arrest/epilogue chain. EET enters normal SoA through its existing import rules; standalone ends at native credits. |
| 291 | Existing EET ending repair | Append-only fix for the original 290 carrier-script softlock. Fresh 290 already includes it; an already-corrected installation is left unchanged. Requires 290 and EET. |
| 292 / 293 / 294 | Imoen in Shadows of Amn (EET, choose one) | Before the campaign switch, an imported or recruited Imoen's SoD gear goes through EET's import rules like the party's (the rest is banked) and she keeps only her BG2 belt, correctly equipped. Then: 292 (CEBG default) EET's Shadows of Amn Imoen plus her tome boosts; 293 as taken along; 294 (EEex) dual-class to mage at her end-of-SoD thief level. Requires 160, 290 and EET_end. |
| 910 | Optional full SoD skip (EET) | Offers a confirmed bedroom choice after continuous BG1 import. Yes uses normal carried-inventory handling and grants 250,000 protagonist XP once in BG2. No continues SoD. Loose-loot recovery is excluded. |

This table highlights the global and ending components; `COMPONENTS.md` in the
release contains the complete inventory.

Component 115 also records companion history for road-north dialogue when installed
before SoD starts. It does not repair scenes that already played. Corrected BD2000
arrival, normal wardstone transfer and Adirran's briefing passed the user's playtest;
the saved Khalid retains normal party control. Later quest branches have installer
coverage without a complete new native run. See the
[continuity record](../docs/plans/2026-09-10-khalid-continuity.md).

## Install

Extract the release ZIP into the game directory that contains `chitin.key`,
close the game and any mod manager using that directory, then run:

```
setup-chriz-sod-remix.exe
```

v0.6.16 exposes **49 declarations in seven install groups**, including
the optional Extra Challenge group. Select according to prerequisites and installed
history; 176, 235, 258 and 291 update older components, while fresh versions include
those corrections. Choose one of `900`/`901`; `257` and EET-only `910` are optional.
On EET, choose one of `292`/`293`/`294` for Imoen's handover into Shadows of Amn.
Old per-install row counts are historical snapshots, not a current selection guide.

Position: tail-install (after EET_end on EET installs — all patches are in-place edits of
final files). Standalone BG:EE+SoD excludes EET-only `291`, `292`-`294` and `910`. Reversible via the
standard WeiDU backups (`weidu_external/backup/chriz-sod-remix`).

## Treasure compatibility (component 900)

v0.6.8 preserves the camp chest's existing item records, including empty or
mod-modified contents, and adds only the eight approved removed-content rewards.
It no longer requires or recreates a vanilla sword. Charges, expiration, flags,
other containers, and unrelated area data are retained. Invalid area bounds or
missing/ambiguous target containers still fail before writing.

Component 210 remains required; 900 and 901 remain mutually exclusive. The
optional skip (910) and component order are unchanged. If a mod manager paused
on an earlier 900 failure but subsequently installed 910, use its supervised
recovery flow. Do not edit WeiDU.log or blindly rerun the complete selection.
Public-installer synthetic tests cover this partial-install shape and the fix;
no new full-stack game installation or gameplay test is claimed for this patch.

## Live-save behavior

`.are`/`.bcs`/`.dlg` load by resref at runtime: changes apply to areas not yet visited and on
next area (re)load. Scenes whose gate globals are already past simply never re-fire.
Already-spawned creatures retain their saved AI assignments, so 257 requires new
bridge spawns. Existing area snapshots also retain actors and container contents;
use the pre-entry saves specified above for those changes.

## Verification boundary

The user accepted the harder bridge build, prompt Bence arrival, save/reload and
onward crossing. Liia's 22,000 reward/reload, Skie's XP/condolence route, the native
amulet reward and Guardian removal also have recorded checks. These do not mean
every component or spell has been tested in a complete campaign. The final 256/257
split and finite Mislead correction have no new native acceptance; Shadow Aspect
testing is deferred. The reported unequipped appearance after palace rest remains
unresolved. The [v0.6.10 report](../docs/releases/v0.6.10.md) records the earlier
offline checks and Khalid entry acceptance. The
[v0.6.11 report](../docs/releases/v0.6.11.md) covers the Skie installer/script
compatibility checks. The [v0.6.12 report](../docs/releases/v0.6.12.md) records the
timer checks; its native presentation and balance testing is deferred to the next
collection test pass. No new native playtest is claimed. Earlier native observations
remain in the [test record](../docs/playtest/2026-09-09-fast-sod-test-plan.md).

## Optional full skip (component 910)

Install after EET_end and components `110`, `140`, `150`, and `160`, before the
first palace-bedroom arrival in a continuous BG1 game. This is not a retroactive
skip for a save already staged in the bedroom, nor a fresh/standalone SoD option.
Confirming Yes uses the original EET handoff and grants **250,000 XP to Player1
once in BG2**, not shared party XP or a minimum XP floor. Confirming No restores
the original backpack impound and continues SoD; each confirmation can be declined.

Keep items carried. Automatic loose-ground-loot recovery is deliberately absent;
imported off-party Imoen's existing belongings are included, fresh Imoen's are not.
EET still controls item selection and BG2 placement. No EEex dependency is added.
The native Yes route and saved XP/import sample passed. Visual transition polish,
imported-Imoen/broader party variants, the final No continuation, and explicit BG2
reload coverage remain follow-ups. See the acceptance record in the release ZIP.

## Victory ending (components 290 and 291)

Component 290 keeps the short victory celebration and uses Dazzo's rest conversation
to end SoD. On EET it preserves the installed equipment-import rules and moves directly
into BG2's normal opening. Imported gear goes through EET's normal hidden import
bank; downstream placement is unchanged, rather than being awarded directly to
the party. Standalone SoD uses its native credits endpoint. Install 290
with its declared prerequisites before first visiting BD4300. An older save without the
local import container receives a diagnostic and keeps its equipment and control.

For an EET installation that already has 290, append **291** to repair the original
carrier-script softlock. Do not reinstall 290 or uninstall earlier components:

```
weidu.exe chriz-sod-remix/setup-chriz-sod-remix.tp2 --force-install-list 291 --language 0 --use-lang en_US --no-exit-pause
```

Fresh 290 installations already include this correction; 291 then leaves game resources
unchanged. The repair refuses unexpected endpoint or guard changes before writing.
The isolated EET guard/save-reload check and one real return/celebration run,
celebration reload, and reduced inventory handoff test passed. Six markers and a
bag reached the hidden AR0602 import bank exactly, with saved bag contents intact.
This verifies retention through the standard import rules, not that all equipment
is immediately lootable. Standalone runtime and the original expanded party and
inventory matrix remain untested. See the [runtime evidence](../docs/playtest/2026-09-06-ending-runtime.md).
