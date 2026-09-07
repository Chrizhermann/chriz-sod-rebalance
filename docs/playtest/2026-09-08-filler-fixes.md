# Approved filler fixes — verification, 2026-09-08

Status: installer and resource-copy verification passed. Native combat, spell
casting, quest interaction and save/reload acceptance have not been run for this
change. No live or designated dev installation was modified; these components
are unreleased on the issue-16 branch.

## Changes and boundaries

- 135 removes BD0063's recurring dead-magic application, two descriptions,
  eight vanilla caster remarks, and the optional Aura remark. The assassins,
  entry hooks, ordinary Minsc/Corwin warnings and rest-unlock logic remain.
  WeiDU selects it by default; explicit component selection can omit it.
- Fresh 230 preserves Ymori. Append 235 on older installations to restore only
  his schedule and update the future road-north award from 23,200 to 23,100 party
  XP. His CRE remains deactivated until the native body-quest Activate action;
  items, container script and dialogue are unchanged.
- 265 appends one BDMISC68 to BD5000's existing Dead_fighter container without
  rebuilding existing items, retires the three obsolete displacer grants,
  suppresses the exact BD5110 Guardian and removes two BDSHSOUL summon actions
  from Shadow Aspect. Regular shadows and surrounding AI/quests remain.
  Its 3,200 party-XP allowance changes the future coalition award to 106,800.
- Subsequent user decision: component 175 pays a flat 22,000 per character on
  every difficulty. Tail component 176 updates the earlier 24,000 award without
  reinstalling existing components or altering already-paid XP. The same return
  dialogue, six per-character actions and one-time gate remain.

Apply the ARE changes before visiting BD2000, BD5000 and BD5110. The installer
does not edit saved areas, recover items into already visited areas, or add/subtract
XP already paid. A current antimagic effect in an existing save can persist for
its remaining duration; 135 stops future applications and does not restore buffs
that the old effect already dispelled.

## Verification

The initial filler pass's WeiDU 249 validation passed: 99 tests under `tests/`, 41 research tests,
14 ending-verifier self-tests, and parse checks for the TP2 plus all 40 TPA
libraries. No tests were skipped in these runs. The counts include the
existing regressions as well as the new filler tests.

The flat-22,000 follow-up passes 110 tests under `tests/`, including 11 new
public-installer cases for fresh 175 and append-only 176. The copied effective
dev `CSRCELE.DLG` also passes: exactly six bytes change (the six amount digits),
all other bytes and source hashes remain unchanged, and already-corrected data
is a byte-exact no-op in a second disposable fixture. The reward's one-time
gate, per-character delivery and payment before DestroySelf are preserved;
unknown/partial awards and changed quest gates are rejected. Evidence is in
ignored `research/data/issue16-flat-xp-176/actual-resource-smoke.json`.

Real WeiDU tests run in disposable synthetic games. Component 135 is checked
against independently compiled retained blocks, including absent/present Aura,
different string ranges, original/corrected resources and rejected partial edits.
Component 235 uses the public installer, byte-exact actor/CRE/item preservation,
known old/new rewards, prerequisites, malformed structures and once-guard tests.
Component 265 checks container records/charges/flags, exact summons, independent
library scopes, original/corrected data and rejection before resource writes.
Public 265 integration verifies prerequisites, its global ban without optional
240, exact chapter award preservation and rollback for invalid/duplicate awards.

Two negative fixtures exposed overly broad XP patch guards: a second reshaped
road-north award pair and simultaneous old/corrected coalition payout anchors.
Both now fail safely and have regression coverage.

Actual EET and standalone BD0063 resources also passed isolated 135 checks:
18 to 6 blocks on EET (Aura present), 17 to 6 on standalone. Each output was
byte-equal to the independently compiled six preserved blocks. Source games
were unchanged. The 265 effective-resource test similarly preserved the exact
original scripts except the three obsolete item grants and two banned summons,
and preserved existing raw corpse inventory before adding one amulet.

The final public 135/235/265 suffix ran with WeiDU 249 against copies of current
dev EET resources and their full IDS dependencies. Only these eight files changed:
BD0063.BCS, BD2000.ARE/BCS, BD5000.ARE/BCS, BD5110.ARE, BDASHIRU.BCS and BD4000.BCS.
Copied TLK bytes and source input hashes remained unchanged. Assertions checked
the exact Ymori schedule-only ARE change and decompiled spell, summon and XP
outcomes. Source resources and all resulting binary assets remain outside Git.

Local ignored evidence: `research/data/issue16-audit/public-smoke-20260908-063554/`
contains `result.json`, the public installation log and decompiles. Initial
resource-only fixtures omitted BIFF-owned IDS dependencies; completing that
fixture resolved its missing-symbol errors. This was not a game-patch failure.

## Remaining acceptance and triage

Native acceptance remains: encounter casting/buff retention, Ymori's staged
activation, corpse pickup/Mizhena turn-in, absence of the Guardian, and hardest-
difficulty Shadow Aspect combat. These are not established by installer tests.
The user explicitly assigned Ymori proportionate side-quest priority.

BD5000 still has companion warnings about large-cat tracks/claw marks. The
physical clues remain, but the warnings refer to the removed displacer pack;
recorded for later density/text triage, without restoring the pack. Its old
death-dependent hobgoblin rearm path remains dormant. Other ambient and travel
arena cuts are still design questions, not newly approved scope.
