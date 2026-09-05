# Changelog

## v0.6.6 - 2026-09-06

- Add component `290`: end SoD after the short playable victory celebration,
  with Dazzo's rest conversation as the deliberate endpoint. Remove the
  post-victory murder, arrest, trial, escape, and ambush sequence.
- Preserve EET's installed import rules and BG2 item placement. The new route
  carries internal import data forward without sending the party through the
  removed ambush; it does not award the party a bag of equipment.
- Fix full-cutscene suspension of the EET carrier. Fresh `290` includes the
  correction; tail component `291` repairs existing `290` installations without
  uninstalling or reinstalling earlier components. Missing saved-area containers
  abort visibly before inventory is touched.
- Add native SoD ending support and platform-aware prerequisite resources.
  Standalone installation/static checks pass; native credits testing is pending.
- Verify the EET guard, actual victory sequence, celebration save/reload, and one
  six-marker inventory handoff with exact potion-bag contents. Expanded party
  variants and multiplayer remain untested.
- Retain v0.6.4 installer ordering and v0.6.5 scrying-pool fixes. Record the bridge,
  Ashatiel, and campaign-filler roadmap tasks without implementing those designs.

## v0.6.5 - 2026-09-05

- Fix component `120` on the current no-Aura four-state `BDSCRY.DLG` by
  targeting the Hooded Man picker route through its semantic local flag instead
  of assuming an optional state `4` exists.
- Apply the same guarded native-layout patch to component `225`'s Imoen and
  Caelar picker routes, while preserving the existing text-only omen and
  component `220` Essence rehome.
- Add WeiDU integration coverage for the native dialog, fail-closed changed
  layouts, and the installed scrying-pool verifier; use the CI-provided WeiDU
  executable when available on `PATH`.

## v0.6.4 - 2026-09-04

- Declare component `210` before component `197`, satisfying the latter's real
  WeiDU dependency when installing the complete 30-component selection.
- Add a regression that preserves all 31 declarations (including the mutually
  exclusive `900`/`901` pair) and locks the dependency-safe order.
