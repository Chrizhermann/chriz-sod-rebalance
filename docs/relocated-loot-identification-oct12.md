# Relocated loot identification — 12 October 2026

Status: implemented locally from release `v0.6.12` (`b2af832`), not committed,
merged, released or applied to a game. Branch:
`codex/relocated-loot-identification-oct12`.

## Change

Relocating loot no longer automatically identifies it. This is limited to the
Korlasz jailbreak grants (170) and Coast Way camp-chest rewards (900).

- Newly granted loot retains the identified bit of its original instance when
  that instance exists. This includes an original deliberately identified by an
  earlier mod. The source resource is read only.
- Existing creature inventory and chest records retain all flags, expiration,
  charges and other data. Authored reward counts, charges, equipment slots,
  undroppable equipment, cash, gems, bags and keys are unchanged.
- If another mod removed the original instance/resource, the existing authored
  reward remains, but receives no free identification. A technical log line
  explains that fallback. Mundane items remain naturally known to the engine.
- Sillune's newly authored invisibility potions, including the SCS potion alias,
  are no longer forcibly identified. They have no source-instance relocation.
- The existing Ring of Free Action reward is an authored replacement for the
  Tsolak death-drop route, not a copied RING09 inventory record. It likewise
  starts without a forced identified flag. This change does not alter or
  reimplement the original death-drop machinery.

The original drop references come from existing research
`docs/research/10a-korlasz-item-inventory.md`,
`docs/research/12-coastway-census.md`, and the component's existing reward list.
Read-only inspection of the EET reference on 12 October found the relevant
original magical drops unidentified. Korlasz's equipment had other instance
flags (2); those are not identification. Unrelated original cleric equipment
included an already identified item and remains untouched.

## Boundary

No treasure relocation, encounter, XP, quantity or balance redesign. No broad
scan of other delivery paths; that larger follow-up remains separate. Existing
saves that already contain these creatures or containers are not repaired.

If multiple matching source instances disagree about identification, installation
reports that concrete ambiguity instead of arbitrarily selecting one. Duplicate
copies that agree are supported. Valid empty source areas/creatures and removed
source items are supported; malformed resource/table bounds are still rejected.

## Verification

Run from this worktree, with WeiDU 249 available via `WEIDU_EXE` or the existing
test-runner lookup:

```text
python -m unittest discover -s tests -p test_relocated_loot_identification.py -v
python -m unittest discover -s tests -p test_treasure_container_installer.py -v
```

The first executes every actual 170 `ADD_CRE_ITEM` line in isolated synthetic
creatures, with the production source-identification setup: original identified
and unidentified donors, multiple/reordered copies, untouched control records,
authored charges/flags, and ordinary WeiDU uninstall. It does not execute the
unrelated jailbreak AI/dialogue setup.

The second executes the public 900/901 installer. Coverage includes varied and
empty destination chests, source identification preservation, empty/absent
sources, genuine mixed-ID ambiguity, malformed areas, EET/non-EET marker
variants, repeated install, exact uninstall restoration, and the existing
900/910 install-order check.

These are automated source/WeiDU checks, not a new in-game playtest. SR changes
to item mechanics are out of scope: no ITM/SPL file is written.

Result on 12 October: both commands passed (one all-grants test and 14 public
treasure-installer tests). WeiDU 249 parsed all three changed/added TPA files;
`git diff --check` passed. No game copy or native-game test was used.
