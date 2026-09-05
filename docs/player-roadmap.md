# What's next for the SoD remix?

Status snapshot: 6 September 2026. These are priorities, not promised dates.

- **WIP — optional full SoD skip.** A bedroom choice lets you continue SoD or
  move into the normal BG2 opening with 250,000 extra XP for your main character.
  It uses normal carried-inventory import handling; automatic recovery of loose
  loot is deferred. The candidate is implemented and installed in an isolated
  test copy; final in-game transition and equipment checks are still outstanding.
  Not released or ready for a collection pin yet.
- **Planned design — a better Boareskyr Bridge finale.** Remove the explosive
  barrel gimmick. Several wizards attacking the bridge with fire and earth
  elementals is the proposed replacement, not a finalized encounter.
- **Planned design — Ashatiel as a party encounter.** Explore a Chosen of
  Cyric-style fight with a warning, time to buff, and properly prepared enemies.
  The roster, mechanics, and roughly 30-second preparation window still need
  the agreed full design discussion.
- **Planned audit — less filler across the campaign.** Check for missed trash,
  scripted waves, respawns, and travel encounters, while protecting worthwhile
  story and siege battles. Further cuts will follow evidence and keep/cut
  decisions; they have not already been made.

**Already released, separately:** v0.6.6's shorter post-victory ending. That is
component 290, not the full-campaign skip above. Component 291 is a repair tool,
not a normal collection selection.

Wider ideas such as the deeper Caelar/Avernus rework and further chapter passes
remain in the wishlist; this snapshot does not promote them into first-alpha
commitments.

Maintainer references: [full-skip candidate/test status](design/wave1/06-optional-sod-skip-testing.md);
[bridge issue #14](https://github.com/Chrizhermann/chriz-sod-rebalance/issues/14),
[Ashatiel issue #15](https://github.com/Chrizhermann/chriz-sod-rebalance/issues/15),
[filler audit #16](https://github.com/Chrizhermann/chriz-sod-rebalance/issues/16).
The future acquired-item registry is tracked separately in
[issue #18](https://github.com/Chrizhermann/chriz-sod-rebalance/issues/18).
The planned directions are recorded in master at `25ab509`,
`docs/01-remix-wishlist.md`, under the September 5 roadmap additions.
