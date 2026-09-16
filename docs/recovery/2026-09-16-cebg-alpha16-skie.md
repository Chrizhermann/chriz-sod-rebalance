# CEBG alpha.16: component 197 recovery

## Result

Use **SoD Remix v0.6.11** and append **component 197 only** to the inspected
partially installed alpha.16 game. The public installer passed this operation
on disposable copies of its current effective resources, after all later SoD
writers. Reinstalling the other 37 SoD components or restarting the collection
installation is unnecessary for this failure.

This investigation did not modify the original game, its recovery ledger, or
the stream installation. The collection agent owns the recipe pin and supervised
continuation. This report is installer/resource evidence, not a new gameplay test.

## Confirmed failure and current state

The diagnostic archive's `logs/steps/0116-c656b8d09bdc1ad9/attempt-0001/`
contains `process-output.log`, `before.log`, and `after.log`. Component 197
expected two native BD2000 Skie spawns, but component 115 had duplicated those
victories into four mutually exclusive carried/ordinary Khalid branches.
WeiDU rolled back 197's earlier BD0102 and BDSKIE edits; its BD2000 write and
subsequent dialogue/helper changes never happened.

The original 332 component rows remain intact, with 37 successful SoD rows
appended, for 369 total. Component 197 is absent. The current WeiDU.log matches
the diagnostic `after.log` byte for byte. Its failed backup directory contains
only an empty `OTHER.197` marker; no failed component resource needs restoration.

Later writers matter:

| Later component | Overlap with 197 | Result to preserve |
| --- | --- | --- |
| 215 | BD7100.BCS | Travel XP changes |
| 230 | BD2000.BCS | XP changes |
| 256 | BD2000.BCS, BDBENCE.BCS | Consolidated victory, both Khalid routes, eight enemy guards, combat-clear/retry approach |
| 290 | BDBENCE.DLG | Ending edits, including state 65 and removed arrest/murder roots |

Component 256 consolidated the four Skie spawns into **two**, one in each Khalid
route. Do not restore the pre-197 BD2000 backup over the current script: that
would discard subsequent changes. Do not infer safety from a two/four count alone.

## Fix and verification

The new bridge helper recognizes the two native victories, their four #115
copies, the single #256 victory, or the paired #115/#256 victory. It verifies
the known conditions and spawn actions. Paired copies must have complementary
Khalid guards and agree in all other content except the three ordinary-only
Khalid retreat actions. Unexpected counts, missing branches, differing payloads
and extra unrecognized spawns still fail. Only the intended Skie spawn lines
are removed.

Late recovery also needs Bence ordering protection: 197 prepends its legacy
conversation starter. It now excludes `CSR256_STAGE(BD2000)=3`, leaving 256's
combat-clear, dialogue-validity, proximity and retry handling in control even
when 197 is appended afterward.

Focused coverage:

- Synthetic real-WeiDU tests cover all four shapes, both 197/256 orders,
  preservation of foreign conditions/actions, malformed layouts and compiled
  Bence priority.
- Public installer tests cover 197 without 115, actual 115 followed by 197,
  and a 197 tail append against copied current alpha.16 resources.
- The tail rehearsal retains all 369 existing installed component identities,
  languages and ordering; only 197 is appended, making 370. The minimal fixture
  uses `--quick-log` because other mods' source packages are absent, so its log
  comparison excludes display comments. Normal collection logging can be used
  on the complete installation.
- BD2000's entire compiled script is unchanged except the two removed spawn
  actions. Existing Bence blocks survive except 197's intended missing-Skie
  quest gate; the prepended starter defers to 256. BD7100 changes only at the
  intended party-safety guard. BDBENCE dialogue states outside 25/32/33/39 remain
  semantically identical, preserving 290's edits. Existing TLK entries and text
  remain intact; new recruitment text is appended.
- Exactly ten effective resources change: BD0102.BCS, BDSKIE.BCS, BD2000.BCS,
  BDBENCE.BCS, BD7100.BCS, BD4000.ARE, BDSKIE.DLG, BDBENCE.DLG, BDNEDERL.DLG,
  BDDIALOG.2DA. Shared potion items, other copied resources and unrelated scripts
  remain unchanged.

## Collection continuation

1. Confirm the same failed installation is selected, 197 is still absent, and
   the 369-row sequence and current resources have not drifted. Do not apply this
   as a reinstall to a copy where 197 has since succeeded.
2. Pin the immutable v0.6.11 release/tag and its published checksum. Deploy the
   updated mod source and matching TP2 while retaining all existing backups,
   WeiDU.log and collection recovery state.
3. Append **only 197** through the collection's supervised recovery. The direct
   equivalent, shown for the collection agent rather than executed here, is:

   ```powershell
   & .\setup-chriz-sod-remix.exe .\chriz-sod-remix\setup-chriz-sod-remix.tp2 --language 0 --use-lang en_US --force-install-list 197 --no-exit-pause --noautoupdate
   ```

4. Require a successful 197 result, one appended row, unchanged previous
   component identities/order, and the preserved bridge/ending results above.
   Then record the recovery through the collection's normal ledger workflow
   and continue the pending recipe. No uninstall, old-resource restore, manual
   WeiDU.log edit or replay of the full 38-component request is needed.

Inspected-copy SHA-256 checkpoints (September 16, 2026):

| File | SHA-256 |
| --- | --- |
| WeiDU.log | `743f3352923138238ec164b4b46ea18a8a7c24f673a48be9b391ef868c4481a2` |
| override/BD2000.BCS | `4f28de0b27885b879a0e1fd48a92295675be0b849f52ff35d3335f92e06a3efe` |
| override/BDBENCE.BCS | `90cdfdb4134dee10220f3312b4381448fc0b23c47034b5e6d103e938ca81ad03` |
| override/BDBENCE.DLG | `2dba943b02b732133fc013837879c367c21a9d626168672b8887813eb5704818` |

The local capture, full input hashes and test logs are under
`C:\Users\chris\CEBG-Tests\115-197-20260916`. Re-run the public effective tests
against a refreshed capture if these inputs or the installed component sequence
change. The source capture is read-only input, never a WeiDU target.

```powershell
$env:CSR_197_FIXTURE = 'C:\Users\chris\CEBG-Tests\115-197-20260916'
$env:WEIDU_EXE = '<path to WeiDU 249>'
python -m unittest discover -s tests -p test_comp115_comp197_order.py -v
python -m unittest discover -s tests -p test_comp197_effective.py -v
```
