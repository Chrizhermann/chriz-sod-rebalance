# Component 256: combined-stack donor compatibility

The September 9 combined installation rejected `BDOLONEI.CRE` during preflight
with `unreviewed donor effect 326 (C0PR#MO1)`. This was an omission in our reviewed
donor whitelist, not evidence of an Artisan's Kitpack defect. No Kitpack or other
mod source needs changing for this failure.

## Reviewed semantics and correction

The installed `ArtisansKitpack/lib/MonkRevision-Mystic.tpa`, lines 427–433,
adds two opcode-326 deliveries of `C0PR#MO1` to mage/sorcerer creatures.
Parameter1 is 1 or 19; parameter2 is SPLPROT row 105, whose installed values
`0x10d -1 1` mean class equals effect parameter1. Target is 0, power 0,
timing 1, duration 0, probability 100/0, and special 0.

The effective MO1 helper clears its own previous MO1/MO2 effects, initializes
the custom monk-equipment eligibility stat to 1, and invokes MO2 to reset it
for the two exception kits. The bridge's generalist mages match neither kit.
This is equipment-policy initialization; it grants no combat spell, APR or
damage bonus. None of the twelve selected equipment resources uses that
policy. Preserve the pair on both mage clones rather than stripping it.

`comp256_creatures.tpa` now accepts only that reviewed MO1 delivery shape on a
class-1/19 donor. When it occurs, preflight additionally requires MO1/MO2 and
the unchanged row-105 meaning. All other unknown effects still fail before
any owned encounter resource is written. Helper spells, SPLPROT and donor
creatures remain unchanged. No spellbook, AI, difficulty or encounter-design
change is part of this correction.

The bounded donor audit inspected all eight selected templates together:
BDOLONEI, BDCRUE45, BDELFIRL, BDELFIRM, BDELFIRG, ELEARL01, ELEAR01 and
ELEARG01. Their 49 effects contained only this previously unrecognized pair,
on BDOLONEI. The optional SUMELEAR fallback's six effects were also reviewed;
no additional allowance was needed. Existing proficiency, Kitpack helper and
elemental-immunity allowances remain as before.

## Verification boundary

All 63 component tests pass using real WeiDU 249. New cases cover byte-exact
MO1 preservation on both mages in both CRE effect formats, signature drift,
unknown helpers, non-caster donors, missing dependencies and altered class
filter semantics. An independent byte mutation checks the embedded V2
effect's special field at +0x40, after the save bonus at +0x3c.

The public installer was rehearsed in disposable games populated from the
completed combined installation's effective resources and copied WeiDU log.
The original library reproduces the MO1 failure. The corrected library
installs successfully and retains the canonical 364-row component prefix,
appending only component 256. Its resource writes are the intended six existing
resources and 21 new assets. Historical log description comments can regenerate
in this reduced fixture because the earlier TP2 packages are not present;
this is not a byte-exact whole-install replay.

Ignored evidence is under `research/data/issue14-fullstack-20260909/`:
`old-complete/report.json` reproduces the failure without any resource or TLK
write; `fixed-complete/report.json` records the successful append and all output
hashes. Both recheck 472 protected source files and 129 read resources without
changes. The adjacent install logs and `donors.json` retain the detailed evidence.
Game resources, logs, backups and the frozen failed receipt were read only.
This establishes installer/resource compatibility on
that stack; native Haste delivery, defensive recasts, balance, pathing and
rendering remain on the combined manual checklist.

## Recovery guidance for the collection task

Appending corrected 256 after installed 260, 265, 270, 280, 290, 900 and 910
is resource-wise valid in this exact retained stack. Their actual uninstall
manifests do not overlap the six existing resources that 256 patches:
BD2000.ARE/BCS, BD2000/BD2000N.TIS, BDPHOSSE.DLG and BDBWOOSH.ITM. All 21
new names are absent from both override and KEY resources. Component 290's
Bence edits leave his bridge aftermath branch intact. Component 256 only
adds TLK strings; it does not replace existing string entries.

The failed attempt reached no component resource write and recorded zero
restored files; its backup directory contains only empty `OTHER.256`.
Nevertheless, the collection receipt still says `fresh_copy_required`.
An append requires the collection's supervised reconciliation of the missing
component, source fingerprint and ordering record before continuation. A
successful manual WeiDU append alone is not permission to resume the runner.

The alternative supervised rollback of the whole 34-component SoD suffix and
reinstallation of its 35-component run is different from removing 255 alone
mid-stack. Resource order presents no new bridge-specific obstacle if that
process proves restoration of the original prefix and reinstalls the full
suffix using consistent source and backups. It touches substantially more
state and was not rehearsed here. Recovery remains the collection task's
responsibility; this work performed no real-game uninstall or recovery.
