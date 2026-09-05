# Changelog

## Unreleased - optional SoD skip candidate

- Add experimental EET component 910: a two-confirmation bedroom choice,
  normal EET BG2 handoff, and a once-only additive 250,000 protagonist XP award.
- Keep party equipment carried for EET's normal import handling by delaying the
  palace backpack impound until a confirmed No. Include existing imported Imoen
  belongings without collecting fresh Imoen or palace equipment.
- Remove the rejected ground-loot collector, pickup scan, and private staging
  area. Loose-loot recovery and the proposed acquisition-history registry are
  deferred (issue #18).
- Add real WeiDU integration and compiled-script regression coverage. Final
  native Yes acceptance remains outstanding; this is not a published release
  or collection-pin update.

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
