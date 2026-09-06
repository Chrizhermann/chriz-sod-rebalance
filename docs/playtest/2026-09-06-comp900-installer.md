# Component 900 modified-chest installer regression

## Confirmed defect

The community diagnostic for v0.6.7 reports component 900 failing because the
destination chest contains **three items, first item SW1H01**. Its assertion
requires exactly one SW1H01. WeiDU exits 2 overall but continues to install 910,
leaving the requested selection incomplete. The diagnostic does not establish
which earlier mod added the other items; no Randomiser-specific cause is claimed.

The same failure was reproduced independently using the public v0.6.7 installer
and WeiDU 249 in a disposable synthetic game. A three-item chest with SW1H01
first fails 900, and an invocation requesting `900 910` still installs 910.
Empty and replaced contents also fail. A single SW1H01 with nondefault metadata
installs but loses its original expiration, charge fields, and flags.

## v0.6.8 correction and verification

Component 900 now copies its target's complete original item records unchanged
and appends exactly the eight approved reward records. The existing relocation
strategy remains: copy the shared array to EOF, add the new target run, and
repoint only the item-table header and target first/count. The old target run
is orphaned, not a second active inventory. Existing same-resref records are
retained, not deduplicated or replaced. No new randomised-loot entitlement is added.

`tests/test_treasure_container_installer.py` exercises the real public installer:

- Empty chest, unmodified sword, nondefault item metadata, reported three-item
  shape, synthetic Randomiser-shaped records, and existing reward resrefs.
- Byte-exact original records, unaffected containers and opaque area bytes;
  no added area/script resources from 900 and no TLK changes.
- Zero-length shared item array and the maximum safe relocated count of 65535.
- Case/space target aliases; missing and ambiguous targets fail safely.
- Short/wrong headers, truncated/overlapping tables, high-bit offsets, invalid
  target or other-container runs, and item-count overflow fail without writes.
- Component 210 and area-resource prerequisites remain enforced; 901 changes
  no area bytes, and 900 remains usable without the EET marker.
- A single public invocation installs exactly `900, 910` in that order;
  protected EET resources and unrelated area bytes remain unchanged.

Windows results: **45 main tests + 33 research tests + 14 ending-verifier tests
= 92 passed**, with WeiDU-dependent tests enabled and none skipped. TP2 and all
36 TPA libraries parse. The initial missing-prerequisite test expected the
wrong WeiDU summary marker; the actual `SKIPPING` result and prerequisite reason
are now asserted along with unchanged resources and absence of the install row.

This is installer/binary validation, not a new native gameplay or full curated
stack test. No real game installation, desktop control, collection recipe, or
component 910 behavior was changed for this fix.

## Recovery boundary

For fresh installs, use v0.6.8 with the existing component selection and order.
For a mod-manager run already paused on an incomplete 900/910 suffix, use its
supervised recovery/reconciliation workflow. Merely replacing the ZIP does not
repair recorded receipts. Do not manually edit WeiDU.log or blindly rerun all
components. Collection/app recovery and its own release are separate work.
