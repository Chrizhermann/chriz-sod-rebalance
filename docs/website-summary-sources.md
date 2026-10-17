# SoD Remix website summary — implementation and source note

Prepared 4 October 2026 for the installer/website chat. This file is editorial
handoff material, **not public-facing website prose**. Publish or adapt
[website-summary.md](website-summary.md) in a dedicated SoD Remix subsection.
The rules-page entry can simply read: **“This run uses SoD Remix.”**

## Authoritative version and scope

- GitHub's latest published release was checked read-only on 4 October 2026:
  [v0.6.12, Boareskyr Bridge collapse timer](https://github.com/Chrizhermann/chriz-sod-rebalance/releases/tag/v0.6.12),
  published 27 September, neither draft nor prerelease.
- The annotated tag resolves to source commit
  `b2af8328a9c78dfa7ff2fd71f73f2c0ea6738544`.
- Remote master was also checked at `b2af8328a9c78dfa7ff2fd71f73f2c0ea6738544`.
  The primary local checkout remains at `115e23c` with a v0.6.11 README and
  unrelated design WIP. Current-feature claims therefore use **tagged v0.6.12
  source**, not that checkout's older release text.
- The tag contains 43 installer declarations in seven groups. That is not 43
  distinct headline features: several rows are repairs/upgrades or alternatives.
  The [complete tracked feature inventory](https://github.com/Chrizhermann/chriz-sod-rebalance/blob/v0.6.12/docs/00-feature-inventory.md)
  provides the broad coverage cross-check; the installer/source links below
  resolve individual behaviors and superseded entries.
- This is a summary of the **remix's available shipped components**, not proof
  that every component is selected in the website's current run. Check the
  collection manifest/installed selection before making run-specific claims.
  The separate companion stat-rebalance project is not part of this inventory.

## Published feature coverage

All links in this table are pinned to v0.6.12. Component numbers are internal
traceability for the website maintainer, not suggested public copy.

| Public topic | Components and precise source |
| --- | --- |
| Rest interruptions | 100, [public installer](https://github.com/Chrizhermann/chriz-sod-rebalance/blob/v0.6.12/chriz-sod-remix/setup-chriz-sod-remix.tp2). The felt-rate table changes rest interruption chance, not all travel ambush rates or pack sizes. |
| Party retention, fresh start | 110/145, [installer](https://github.com/Chrizhermann/chriz-sod-rebalance/blob/v0.6.12/chriz-sod-remix/setup-chriz-sod-remix.tp2), [145](https://github.com/Chrizhermann/chriz-sod-rebalance/blob/v0.6.12/chriz-sod-remix/lib/comp145.tpa). Do not promise new banters for every retained NPC or universal mod-NPC support. |
| Imoen, Skie, Khalid | [160](https://github.com/Chrizhermann/chriz-sod-rebalance/blob/v0.6.12/chriz-sod-remix/lib/comp160.tpa), [197](https://github.com/Chrizhermann/chriz-sod-rebalance/blob/v0.6.12/chriz-sod-remix/lib/comp197.tpa), [115](https://github.com/Chrizhermann/chriz-sod-rebalance/blob/v0.6.12/chriz-sod-remix/lib/comp115.tpa). Recruitment/continuity, not general NPC build rebalancing. |
| Prologue/story | 120/130/140/150/170/180/185/187/190/195; [component labels](https://github.com/Chrizhermann/chriz-sod-rebalance/blob/v0.6.12/chriz-sod-remix/languages/english/setup.tra), [Korlasz implementation](https://github.com/Chrizhermann/chriz-sod-rebalance/blob/v0.6.12/chriz-sod-remix/lib/comp170.tpa). 187/190/195 complete removed-scene cleanup, not additional story arcs. |
| Coast Way and dig site | [200](https://github.com/Chrizhermann/chriz-sod-rebalance/blob/v0.6.12/chriz-sod-remix/lib/comp200.tpa), 210, [220](https://github.com/Chrizhermann/chriz-sod-rebalance/blob/v0.6.12/chriz-sod-remix/lib/comp220.tpa), [225](https://github.com/Chrizhermann/chriz-sod-rebalance/blob/v0.6.12/chriz-sod-remix/lib/comp225.tpa), 245. The lich/quest core and scepter puzzle remain; 245 makes the barrier change survive cutscene skipping. |
| Road north/temple routing | 230/235, [240](https://github.com/Chrizhermann/chriz-sod-rebalance/blob/v0.6.12/chriz-sod-remix/lib/comp240.tpa). 235 repairs old installations that cut Ymori; fresh 230 preserves him. |
| Dragon | [250](https://github.com/Chrizhermann/chriz-sod-rebalance/blob/v0.6.12/chriz-sod-remix/lib/comp250.tpa): Hard/Insane stat additions, not a new AI/spell package. |
| Bridge overhaul, optional challenge, timer | 256/257/258, [current release report](https://github.com/Chrizhermann/chriz-sod-rebalance/blob/v0.6.12/docs/releases/v0.6.12.md), [README](https://github.com/Chrizhermann/chriz-sod-rebalance/blob/v0.6.12/chriz-sod-remix/README.md). Story: no deadline; Easy/Normal/Core/Hard/Insane: 10/8/7/6/5 unpaused minutes. 257 adds only the Insane sequencers. 258 upgrades old 256; fresh 256 includes it. 255's durable barrels are superseded, not another feature of the replacement fight. |
| Coalition scouting/river/undead | [260](https://github.com/Chrizhermann/chriz-sod-rebalance/blob/v0.6.12/chriz-sod-remix/lib/comp260.tpa), 265/266/270. Targeted enemy cuts, Mizhena's amulet relocation and finite Mislead; not removal of every spawn/quest fight. |
| Removed combat restrictions | 135 and 280, [labels](https://github.com/Chrizhermann/chriz-sod-rebalance/blob/v0.6.12/chriz-sod-remix/languages/english/setup.tra), [README](https://github.com/Chrizhermann/chriz-sod-rebalance/blob/v0.6.12/chriz-sod-remix/README.md). The basement reveal dispel is distinct from Belhifet's unreleased opener change. |
| XP/rewards/treasure | 175/176/215, ledgers in 220/230/240/260/270, 900/901; [README](https://github.com/Chrizhermann/chriz-sod-rebalance/blob/v0.6.12/chriz-sod-remix/README.md), [900](https://github.com/Chrizhermann/chriz-sod-rebalance/blob/v0.6.12/chriz-sod-remix/lib/comp900.tpa). Liia pays 22,000 per character. Several cut-combat awards return 80%; say milestone compensation, not proven exact XP neutrality or a guaranteed finishing level. 900's present payload covers the removed Coast Way Forest. |
| Ending and full skip | 290/291/910, [README ending/skip sections](https://github.com/Chrizhermann/chriz-sod-rebalance/blob/v0.6.12/chriz-sod-remix/README.md). 291 repairs an older EET ending; 910 is experimental and EET-only, from continuous BG1 import at palace arrival, with 250,000 XP once to the protagonist in BG2. Existing inventory-import rules still determine what reaches BG2. |

## Unpublished work and design sources

- **Avernus interim overhaul: implemented, uncommitted/unreleased, native test pending.**
  Worktree: `%USERPROFILE%\.codex\worktrees\avernus-finale\chriz-sod-rebalance`,
  branch `codex/avernus-finale`, based on v0.6.12. Read
  `docs/design/wave1/11-avernus-interim-finale.md` and
  `chriz-sod-remix/lib/comp285{,_portal,_belhifet,_hephernaan}.tpa` there.
  The accepted profile specifies +1 weapons, 60% MR, 450 Core/500 Insane HP,
  25% movement, targeted Breach, capped devil replacements and difficulty-aware
  Hephernaan preparation. Its 28 September record reports 16 offline checks;
  do not describe that as gameplay acceptance. No separate Extra Challenge
  variant is implemented. This is absent from the published tag.
- **Ashatiel: design only.** Primary checkout's
  `docs/design/wave1/09-ashatiel-party-brawl.md`, updated 26 September, and
  `docs/research/26-ashatiel-party-sheets.md`. The former preserves duel/refusal
  and records the third group-brawl route. Player preparation/reset, right-lane
  arena direction and victory cleanup have decisions, while exact roster,
  loadouts, integration and balance remain open. Do not advertise a released
  Chosen-of-Cyric-style encounter.
- **Further plans:** primary `docs/01-remix-wishlist.md`, especially the Caelar
  arc and later playthrough improvements; `docs/design/wave1/10-playthrough-followups.md`
  for XP presentation and loot; `docs/research/22-filler-audit.md` for broader
  unapproved density changes. The newer Avernus worktree design supersedes the
  primary checkout's older claim that no lift implementation exists. Caelar
  as final boss remains a long-term direction, not the v0.6.12 ending.
- The old `docs/design/00–05` agent-authored proposals were deliberately not used
  as decisions. The wishlist also contains historical superseded notes; tagged
  implementation and later dated decisions take precedence.

## Verification limits and handoff

“Published” does not mean every branch was played through on every supported
installation. v0.6.12's timer shipped with automated/installer checks and an
explicitly deferred native playtest. The tagged README likewise records limits
for Shadow Aspect, standalone ending and the experimental full skip. Existing
SCS/Spell Revisions handling is not evidence of a completed compatibility matrix.
Keep those distinctions in release/download details; do not turn the website
intro into a universal compatibility or balance claim.

This request produced only these two documentation files. No gameplay source,
game installation, save, release, website or unrelated WIP was changed. No
tests were rerun for this writing task; test counts above are attributed to
their existing records. The draft is saved in the owner repository for the
installer chat to retrieve; no cross-thread message or publication is implied.
