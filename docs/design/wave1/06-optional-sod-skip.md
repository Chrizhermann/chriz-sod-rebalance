# Optional SoD skip at palace arrival (EET)

Status: user-requested on 2026-09-05; simplified inventory scope approved on
2026-09-06. Component 910 is **accepted for v0.6.7**, tested on an isolated
v0.6.5-based copy. The `20260906-r3` test candidate retains carried
party inventory and uses the original EET handoff. The rejected ground-loot
collector and private staging area have been removed. The direct Yes route was
accepted in-game on September 6 for v0.6.7; visual polish and remaining variant
coverage are follow-ups. This is not part of v0.6.5/v0.6.6, the
frozen CEBG r4 recipe, or the separate component-290 ending work.

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
- Work in an isolated source worktree and disposable test data only. Native
  testing was subsequently authorized in coordinated PC windows; never overlap
  another game task or the user's play session. Do not change a live/stream
  install/save or amend the frozen collection recipe. The initial no-publication
  boundary was superseded by explicit v0.6.7 release approval on September 6.

## Candidate component and scope

Home: this repository's existing `chriz-sod-remix` mod, optional component
**910**, label `csr_optional_sod_skip`, displayed as "Offer to skip SoD at palace
arrival (EET, experimental)". Sources are `lib/comp910.tpa`, `dlg/csrskip.d`, and
`languages/english/csrskip.tra`; small scripts are embedded in the TPA. No
dependency on component 290.

For the first bounded candidate, require EET, EET_end, and remix components
**110, 140, 150, and 160**. These give one known party-preserving arrival and Imoen layout.
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
   scene Imoen and bring the imported Imoen into the room. The prompt waits for
   this setup and arrival control restoration. Component 910 holds the native
   party-backpack impound until a confirmed No, so a confirmed Yes can use
   carried equipment directly.

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

Therefore **directly moving bedroom storage to the bulk BD6100 bank would not
be sufficient** to preserve the effective selection rules. The current design
avoids putting party backpacks into storage at all on Yes. Its only off-party
adapter is for imported Imoen's belongings, as described below. The final
native handoff remains an acceptance gate.

Inspected effective resource SHA-256 values:

- K#TELBGT.BCS: `e4035461e31c20a815ad4cf625b2f49a4f8e39d20f16f7fd995d908174a968c3`
- AR0602.BCS: `ca22da807a3d7dda475d2891b12e1b3c379a0842f0b3ed0202992bd7ba066eae`

## DECIDED: equipment scope (revised 2026-09-06)

A direct bedroom skip has a real item-loss edge:

- BD0103's retained `BD_PARTY_ITEMS` block moves all six backpacks into
  **PlayerChest00**. Waiting for arrival setup does not put them back.
- With component 160, imported Imoen temporarily leaves the party and keeps her
  own items while waiting in BD0103. The native party-slot sweep can miss them.
- Component 140 also redirects BG1 finale ground piles beside the bedroom beds.
  These are not carried inventory and are not collected by K#TELBGT.

The earlier September 5 scope included verified imported ground loot. After
rejecting the collector's long delay, Christopher explicitly replaced that part
with: **"Use normal carried inventory; defer loose-loot recovery."**

- Party equipment stays carried until EET handles it. A confirmed No releases
  the original backpack-to-PlayerChest00 block, preserving normal SoD behavior.
- Imported off-party Imoen's existing belongings remain included. Only eligible
  items actually on her, including carried bags, and absent from the party are
  passed through the small adapter. It waits for actual receipt before applying
  the corresponding effective EET import-store rule. Remaining belongings go
  to the existing bulk bank. Fresh Imoen's equipment is excluded.
- No ground-loot recovery, private snapshot, installed-bag catalogue, or queued
  pickup scan. The original BDSODTRN ground-copy behavior is left untouched.
- No arbitrary palace/world loot or SoD quest rewards. EET and the installed
  BG2 import rules still decide item eligibility and availability. This is not
  a promise to keep every item in BG2 or to invent new item destinations.

The proposed save-persistent "ever acquired" registry is deferred in
[issue #18](https://github.com/Chrizhermann/chriz-sod-rebalance/issues/18). Its
format, retroactive treatment of existing saves, and BG2 integration are not
part of component 910.

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

## Historical prototype and ground-probe result

The original bounded prototype lives in
`research/prototypes/optional-sod-skip/`. The following 2026-09-05 results are
historical, not a description of the current public component-910 source.

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
This is historical evidence only. Ground recovery is now deferred, so no
replacement collection mechanism is required for the current skip.

## Current candidate and remaining acceptance (2026-09-06, r3)

1. Delay only the imported game's native backpack impound until confirmed No.
   Fresh SoD starts retain the native behavior and receive no skip offer.
2. After arrival and component-160 setup, show the three-state prompt through
   an invisible-animation helper with its donor's action-blocking effects removed.
3. On Yes, handle only actual eligible belongings on imported off-party Imoen;
   keep party equipment carried. A 15-second receipt timeout restores control,
   blocks handoff/XP, and asks for a reload if that exceptional transfer fails.
4. Move the party to BD6100 with the ambush suppressed. Wait for all existing
   party members to arrive, then invoke the original K#TELBGT. It owns the
   normal inventory selection, bulk banking, party breakup, and BG2 transition.
5. Award the additive 250,000 XP to Player1 once in AR0602, outside the SoD cap.

The public installer creates exactly three resources (`csrskask.cre`,
`csrskask.bcs`, `csrskip.dlg`) and changes only BD0103.BCS, BD6100.BCS, and
BALDUR.BCS. It changes no ARE or BDSODTRN resource. Protected EET resources were
hash-verified unchanged in the installed r3 copy. The obsolete worker and private
area are absent from the current source and removed by the disposable tail update.

**34 automated tests pass on Windows / WeiDU 249.** Coverage includes real
installer compilation/decompilation, prerequisites and rejected layouts, the
exact resource set, protected-resource identity, confirmation loops, XP gates,
the delayed impound, receipt-before-registration ordering, and failure cleanup.
The obsolete collector replay was removed with the rejected collector; synthetic
tests do not establish native scheduling, bag transfers, or save persistence.

Historical native evidence: the earlier candidate passed the automatic prompt,
both confirmation-decline loops, confirmed No, helper cleanup, and real No
save/reload with no skip XP. Its Yes route did not complete BG2 acceptance.
The r3 build completed the Yes route in the six-person fixture. Christopher
accepted it and the resulting AR0602 save confirms 412,209 protagonist XP,
the once guard, and sampled native import handling. The changed No impound
gate still needs a focused native retest.

See [candidate test handoff](06-optional-sod-skip-testing.md) for the exact copy,
fixture, expected XP, and evidence. Imported-Imoen and above-500k-XP fixtures,
full servant/rest/council continuation, and final item selection/save-reload
remain unverified. Christopher authorized v0.6.7 publication with these limits
recorded and visual polish deferred. No standalone support or collection-pin
change is implied by that release.
