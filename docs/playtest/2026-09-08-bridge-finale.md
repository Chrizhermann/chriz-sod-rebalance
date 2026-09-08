# Boareskyr first-version encounter — acceptance record

Component **256** is implemented for the agreed combined manual session with
[PR #21](https://github.com/Chrizhermann/chriz-sod-rebalance/pull/21). It has not
been fought in the native engine. No live/designated dev game or save has been
modified by this implementation work.

## Installation and checkpoint boundary

Use a save from **before the first entry into BD2000**. The old area's actors,
region script and animation state can be cached in a visited-area save. A save
made just before the battle in an already visited bridge area is insufficient.
The installer deliberately does not rewrite saved areas or mid-finale globals.

Append 256 to the designated dev copy after its existing rows, along with the
applicable filler corrections from PR #21. An installed 255 stays installed;
256 supersedes its encounter. Do not reinstall earlier components. Record the
exact commits and appended WeiDU rows when preparing the combined test copy.
That combined copy and its checkpoint saves have not yet been prepared.

## Agent verification

Final Windows verification: **167 regression tests + 41 research tests + 14 ending
contract self-tests passed**, with no skips. The TP2 and all 48 TPA libraries
parse successfully. The 57 new component tests also passed using Linux WeiDU
249 on a case-sensitive temporary copy; the final optional-Skie change received
its own six-test Linux world rerun.

The public installer succeeds against copies of both current effective EET
resources and the standalone SoD reference. The final EET run uses the filler
PR's already-corrected BD2000 ARE/BCS and preserves Ymori's exact actor record.
All 123 EET and 116 standalone source resources retain their original hashes.
All seven copied component libraries match the final implementation bytes.
Standalone's native Skie aftermath spawn is preserved when another component
has not already removed it; the EET target's already-removed variant also works.

Local ignored evidence: `research/data/issue14-public-combined-final-1788871428820403200/report.json`,
`research/data/issue14-public-standalone-1788871355717481800/report.json`,
`research/data/issue14-public-smoke/tests-final.log`, and
`research/data/issue14-world-review/linux-world-skie-result.json`.
These are resource/installer checks, not a native fight or full standalone campaign.

- Real WeiDU fixtures exercise the public installer, finite creature spellbooks,
  compiled AI decisions, both native finale entry seams, victory predicates,
  resource-local dialogue edits and both PVRZ/palette tile formats.
- Public integration checks installation, an existing 255 followed by 256,
  synthetic uninstall restoration, and failure before any encounter/TLK write
  when a late art resource conflicts. Synthetic uninstall is confined to throwaway
  test games and is not an instruction for real installed WeiDU rows.
- The two old spawn lists and both old success predicates are replaced precisely.
  The wider siege and the original Bence/Khalid/journal/rest aftermath survive.
  `Barrel_spot` retains its retreat destination while its old controller is detached.
  BDFISTM1's obsolete warning actor has no remaining creation route. Bence opens
  the normal passage after plot 293 without reading old portal globals.
- The final formation was checked against the actual search map and closed-door
  cells. Full creature footprints do not overlap and party-sized paths reach
  every actor. This catches static obstruction, not dynamic combat congestion.
- Resulting day/night tile records were decoded and visually compared. All three
  baked barrel clusters and the four closed-door alternatives are cleaned; WED
  data, water-overlay alternatives and the original transparency silhouette remain.
- Preparation uses actual caster-level instant casts plus one-copy removal;
  normal combat casts spend their own memorized copies. Haste's once-attempt guard
  applies to the owned freshly created group, not arbitrary third-party haste.

## Short manual run

One proper fight on the user's usual difficulty is the first native acceptance
pass. There is no need to fight all five tiers in that session: automated checks
cover the tier selection and resource counts. Use Insane if assessing the upper
challenge envelope is convenient.

1. Finish the siege/retreat normally. Confirm one short warning, two mages, two
   veterans, two earth elementals and two fire elementals. No barrels, portal,
   barrel instructions or sudden old failure sequence should appear.
2. Watch the mages' starting protections and one normal Haste cast. Confirm the
   nearby frontline actually receives Haste, rather than merely seeing a cast
   animation. Check that fighting through protections prompts a limited defensive
   recast and that interruptions/control remain useful.
3. Fight normally and watch for blocked actors, endless pursuit, spell spam or
   repeated friendly Fireballs. Grease is deliberately uncommon when melee units
   could enter its persistent area. The finite group receives no reinforcements.
4. After all eight are defeated/removed, confirm Bence's aftermath and onward
   passage. Save/reload after victory: no duplicate roster, Bence or reward.
5. If convenient, inspect the bridge at night too. Report visible seams, water
   coverage problems or any remaining barrel artwork. The installer/render checks
   already cover both assets; this is a brief native visual check.

There is **no collapse timer** in version 1. Version 2 will need the separate
visible, generous five-turn timing discussion and an observed Insane fight.
Do the assassin, XP and quest-loot samples from the
[combined filler checklist](2026-09-08-filler-fixes.md#next-manual-session--agreed-2026-09-08)
in this same session. Ymori remains a low-priority side-quest check.
