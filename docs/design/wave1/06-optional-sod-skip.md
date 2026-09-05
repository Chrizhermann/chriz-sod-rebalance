# Optional SoD skip at palace arrival (EET)

Status: user-requested on 2026-09-05; inventory scope approved on the same date.
Dialogue/XP source prototype and a ground-pile probe are prepared; the full skip
is not implemented or installable. The native ground-pile probe failed its
collection gate on 2026-09-05; the proposed receptacle method is rejected for the
tested build. This is not part of released
v0.6.5, the frozen CEBG r4 recipe, or the separate component-290 ending work.

## DECIDED: requested behavior

- An optional, deliberately small early-alpha feature; not a blocker for the
  weekend installer.
- After defeating Sarevok and arriving in the sleeping room, offer:
  "Do you want to skip SoD? You will get 250000 experience on your main character
  if you skip."
- The first question has Yes and No replies. Each leads to its own confirmation.
  Declining either confirmation returns to the first question.
- Confirming skip adds exactly 250,000 XP to the protagonist, once only. It is an
  additive award, not an XP floor, a replacement XP total, or party-shared XP.
- Confirming play-SoD resumes the existing campaign normally and awards no XP.
- Use the normal safe EET transition into BG2; do not invent a new ending or
  carry the SoD party into BG2 as a replacement for EET's normal opening.
- Work in an isolated source worktree and disposable test data only. Do not
  launch a game, change a live/stream install or save, amend the frozen collection
  recipe, or publish a release under this request.

## Proposed component and scope (not implemented)

Home: this repository's existing `chriz-sod-remix` mod, optional component
**910**, label `csr_optional_sod_skip`, displayed as "Offer to skip SoD at palace
arrival (EET)". Proposed source files are `lib/comp910.tpa`, a dedicated dialogue,
and small arrival/handoff scripts. No dependency on component 290.

For the first bounded candidate, require EET plus remix components **110, 140,
150, and 160**. These give one known party-preserving arrival and Imoen layout.
Do not silently broaden this to standalone SoD, fresh SoD starts, or arbitrary
palace-overhaul combinations. The runtime offer is for a continuous BG1 import
(`SOD_fromimport=1`) at the initial `bd_plot=50` arrival.

Transitions and Endless BG1 are research references, not new dependencies.
Compatibility with their modified transition/arrival paths is not certified;
installation guards and the exact supported resource layout must be verified
before any candidate is offered. Do not describe either whole mod as incompatible
without checking the installed components and actual resource changes.

## Verified source seams

The requested room exists in the current remix. There is no need to move the
choice before Sarevok or invent a different story beat:

1. Component 140 preserves the EET/SoD bootstrap in BD0120 invisibly, then uses
   the existing BDCUT00Z move to **BD0103, the palace guest suite**.
2. Component 150's `baf/csrarr.baf` sets `CSR_ARRIVE`, restores visibility and
   control, and leaves the first night behind the servant's `CSR_BEDTIME` choice.
3. Component 160's `baf/imoen103.baf` takes two area-script passes to replace the
   scene Imoen and bring the imported Imoen into the room. A prompt must wait for
   this setup and the party-item impound to finish, rather than interrupting the
   arrival response or an existing dialogue/cutscene.

Relevant current sources: `lib/comp140.tpa`, `baf/exit0120.baf`,
`lib/comp150.tpa`, `baf/csrarr.baf`, `lib/comp160.tpa`, `baf/imoen103.baf`.
The older decompiled `research/data/sod_baf/BD0103.baf` and research document
`docs/research/10b-dungeon-skip-plumbing.md` explain the retained item impound;
they are historical installation snapshots, not proof of a new live test.

EET v14.0 source was read without modifying the test copy:
`EET/compile/baf/K#TELBGT.baf` and `EET/lib/bg2_BCS.tph`.

- K#TELBGT takes current party equipment into the **local** K#ImportContainer,
  handles the normal party breakup/rest and campaign globals, and calls the
  SoA campaign transition. It does not sweep the palace's storage containers.
- EET's AR0602 patch explicitly imports from
  `BD6100*K#ImportContainer`. The party must use that existing BD6100 handoff;
  merely invoking K#TELBGT from BD0103 is not the same route.
- The native BD6100 ambush is driven by `bd_finale` values below 6. A candidate
  must suppress that scene before arrival, complete the existing handoff once,
  and prove the resulting campaign/gear state rather than just a queued action.
- Do not patch K#TELBGT.BCS, AR0602.BCS, CAMPAIGN.2DA, STARTARE.2DA, or write
  ENDOFBG1. Let EET own its normal transition effects.

### Effective import rules: source-template-only inspection is insufficient

On 2026-09-05 the effective `K#TELBGT.BCS` and `AR0602.BCS` were decompiled
read-only from `C:\Users\chris\Games\CEBG-SOD120-v065-test\game`. Outputs went to
an external inspection directory; the game's WeiDU.log SHA-256 was identical
before and after (`47a3d364d37085f0c5e29cfd404737223f9a1ae133604a4bfd3e1c142bee4f07`).

`EET_end/EET_end.tp2:724-761` generates item-import blocks from BDSODIMP's
PartyHasItem references and IMPORT01/02/03 plus K#IMPORT.2DA. These blocks run
**before** the bulk item bank: an eligible party item is removed and registered
in K#IMPORT's bag/store. The bare K#TELBGT source template does not contain them.
AR0602 subsequently runs the existing BDSODIMP and IMPORT-table rules before
banking the remaining inventory and reading the BD6100 bank.

Therefore **directly moving all bedroom storage to the bulk BD6100 bank is not
sufficient** for this approval. The stored-item adapter must make eligible
possessions participate in the effective selection rules, without duplicating
an item already covered by a party copy, inventing destinations, or bypassing
bag handling. No such adapter has been enabled or claimed tested yet.

Inspected effective resource SHA-256 values:

- K#TELBGT.BCS: `e4035461e31c20a815ad4cf625b2f49a4f8e39d20f16f7fd995d908174a968c3`
- AR0602.BCS: `ca22da807a3d7dda475d2891b12e1b3c379a0842f0b3ed0202992bd7ba066eae`

## DECIDED: equipment scope (approved 2026-09-05)

A direct bedroom skip has a real item-loss edge:

- BD0103's retained `BD_PARTY_ITEMS` block moves all six backpacks into
  **PlayerChest00**. Waiting for arrival setup does not put them back.
- With component 160, imported Imoen temporarily leaves the party and keeps her
  own items while waiting in BD0103. The native party-slot sweep can miss them.
- Component 140 also redirects BG1 finale ground piles beside the bedroom beds.
  These are not carried inventory and are not collected by K#TELBGT.

Christopher approved including the stored party backpacks, imported Imoen's
equipment, and **verified imported BG1 finale ground loot** in EET's normal BG2
equipment-import handling. This makes eligible possessions available to the
existing import rules; it does **not** mean keeping all equipment in BG2, giving
everything to the protagonist, or inventing item destinations. His expectation
that some items become BG2 loot is context to verify, not a new placement rule.

There is no permission to collect arbitrary palace/world loot or award SoD quest
rewards. Exact provenance of the imported ground pile must be verified before
collection. Do not use a whole-room sweep merely because the imported pile is in
that room. EET and the installed BG2 import rules still decide item eligibility
and availability.

Gold is already impounded by BDCUT00Z. No new gold refund, skipped quest reward,
romance outcome, or item entitlement is authorized by the XP-only request.
If a candidate needs any further meaningful choice in those areas, stop and ask.

## Upstream investigation and licensing boundary

- [Endless BG1 v20.2, maincomponent/general.tpa](https://github.com/Gibberlings3/EndlessBG1/blob/v20.2/c%23endlessbg1/maincomponent/general.tpa)
  has an EET direct-skip path through BD6100 followed by K#TELBGT. Its additional
  handling for off-party NPC equipment is relevant evidence that the native
  party-slot sweep is not an automatic catch-all. Its Duke Belt offer occurs
  before SoD, so its entry hook is not this requested bedroom hook.
- [Transitions v2.4 readme](https://github.com/Gibberlings3/transitions/blob/v2.4/transitions/readme.transitions.english.txt)
  documents item-driven skipping of all or the remainder of SoD, as part of a
  substantially wider campaign/party/property system. It is not a drop-in
  dependency for a tiny bedroom question.
- Both upstream readmes state **CC BY-NC-SA 3.0**. No upstream implementation or
  assets have been copied into this repository. Researching the existing native
  EET handoff does not authorize silently absorbing either mod's code or assets.
  Any future actual reuse requires explicit attribution and license review.

## Source prototype and validation status

The bounded prototype lives outside the released payload in
`research/prototypes/optional-sod-skip/`. The public TP2, its v0.6.5 version, all
31 component declarations, component 290's separate worktree, and the frozen
collection recipe are unchanged.

`tests/test_optional_sod_skip.py` was added RED before the prototype sources,
then made green. Including the later native-result regression, the full
repository suite passes **24 tests on Windows with
WeiDU 249** (2026-09-05):

- Real compilation/decompilation of the three-state dialogue and XP action.
- Both confirmation declines loop with no side effects; confirmed play-SoD
  records choice 2 and awards nothing; confirmed skip cannot award before item
  readiness and adds 250,000 only to Player1 once in repeated/model-reload tests.
- The probe's installer refuses to run without a disposable-copy opt-in marker,
  creates exactly six new probe-owned resources, and leaves every pre-existing
  synthetic resource byte-identical.
- The read-only save verifier rejects unnamed-pile copies, duplicate/missing
  items, unrelated chest loot, duplicate named receptacles, and truncated data.

The state replay and synthetic SAV fixtures **do not test native script
scheduling, XP caps, campaign transition, or real save/reload behavior**. That
source-only work launched no game. A later explicitly authorized disposable
engine test is recorded below; no accepted/live game or save was modified.

### Ground-pile validation gate

The inspected BD0103.ARE has exactly four containers: PlayerChest00,
Imoen_equipment, and two bookcases; **none is a ground pile**. Component 140's
sole BDSODTRN import target is BD0103 [190.540]. The original hypothesis was a
narrowly owned, initially empty named ground-pile receptacle at that point.
Its required native merge behavior was tested below; no whole-room sweep or
low-level EEex mutation was substituted.

On 2026-09-05, after Christopher authorized PC use, the isolated two-room probe
was run in a new copy/profile on **BG2:EE 2.7.3.0 / EEex 1.2.0**. It failed:
the imported A/B tokens went into a new source-named pile while the preplaced
CSRBG1PILE remained empty. The source and destination control chests were
untouched. Full restart/reload and a new save preserved the failure. The
banking command was not run, as required by the failed precondition.

See `research/prototypes/optional-sod-skip/engine-results-20260905.md` for
version/hash evidence and test-harness caveats. This result rejects the empty
named-receptacle method on the tested build; it does not authorize a whole-room
sweep or treating the observed source name as a stable production identifier.
**A different provenance-safe collection mechanism is required.**

### Remaining before an installable candidate

- Complete the stored-item adapter against EET's effective eligibility rules,
  including duplicate-party-copy and bag handling, with disposable fixtures.
- Replace the rejected ground-pile collection method and verify its provenance
  and persistence in a disposable engine test.
- Wire the tested dialogue and guarded XP action into the bedroom arrival and
  handoff only after the replacement passes. Preserve both confirmation
  loops and the no-side-effect behavior already covered by the source tests.
- In the engine, verify a confirmed No permanently records play-SoD, adds
  nothing, and leaves the servant/rest/council flow unchanged.
- In the engine, verify confirmed Yes adds exactly 250,000 to Player1 once;
  check XP caps, save/reload, and repeated trigger evaluations, which source
  compilation and modeled replay do not establish.
- Use disposable fixtures to verify the arrival hook's ordering and prerequisite
  failures, and that only intended resources change. Separately test the actual
  campaign transition and agreed equipment handling on a disposable game/save
  when the user has explicitly coordinated a game test.
- Verify the final BD6100/AR0602 equipment transfer, protagonist XP delta,
  normal BG2 party state, campaign globals, and absence of the SoD ambush scene.
  A compilation pass is not live acceptance of those effects.

Tiny eventual user checklist: save before the question; decline each confirmation
once; confirm play-SoD and reload to check no repeat; reload the original save,
confirm skip, check protagonist XP increased by exactly 250,000 and the normal
BG2 opening starts; save/reload there and check the agreed imported items and no
second XP award.

Release/pin readiness: **not ready**. Remaining implementation includes the
bedroom offer hook, effective-EET-rule-aware stored-item adapter, and final
handoff, followed by a real end-to-end acceptance test. The present deliverable
is a tested source prototype plus a focused native probe, not a completed skip
candidate. Keep v0.6.5 and frozen r4 unchanged; a later tested candidate and
separate publication authorization are required.
