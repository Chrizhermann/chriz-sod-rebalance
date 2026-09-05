# Optional SoD skip at palace arrival (EET)

Status: user-requested on 2026-09-05; source research only. Implementation is
paused for the equipment-scope choice below. This is not part of released
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

## OPEN: equipment scope before implementation

A direct bedroom skip has a real item-loss edge:

- BD0103's retained `BD_PARTY_ITEMS` block moves all six backpacks into
  **PlayerChest00**. Waiting for arrival setup does not put them back.
- With component 160, imported Imoen temporarily leaves the party and keeps her
  own items while waiting in BD0103. The native party-slot sweep can miss them.
- Component 140 also redirects BG1 finale ground piles beside the bedroom beds.
  These are not carried inventory and are not collected by K#TELBGT.

Question to settle: **Should confirming skip automatically include the stored
party backpacks, imported Imoen's equipment, and imported finale ground loot in
EET's normal BG2 equipment-import handling?**

Recommendation: yes, preserving the existing BG1 possessions without requiring
the player to unpack or re-recruit someone before an immediate skip. This is a
proposal, not permission to collect arbitrary palace/world loot or award SoD
quest rewards. Exact provenance of the imported ground pile needs verification
before sweeping a whole room. Do not promise that every imported item is then
freely available in BG2: EET and the installed BG2 import rules still decide that.

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

## Required candidate tests and user check

No implementation or candidate tests have run yet. Begin TDD after the open
equipment choice is resolved:

- Compile a synthetic three-state question/confirmation dialogue; test both
  confirmation declines looping back without changing XP or campaign state.
- Verify a confirmed No permanently records play-SoD, adds nothing, and leaves
  the servant/rest/council flow unchanged.
- Verify confirmed Yes uses `AddXPObject(Player1,250000)` exactly once, never
  `AddExperienceParty`, `SetXP`, or a threshold. Guard before awarding; check
  save/reload and repeated trigger evaluations cannot award again.
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

Release/pin readiness: **not ready**. This is a durable request and bounded design
handoff only. Keep v0.6.5 and the frozen r4 recipe unchanged; a later tested
candidate and separate publication authorization are required.
