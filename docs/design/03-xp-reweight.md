# Design 03 — XP Reweight (PROPOSAL)

Depends on `docs/research/03-xp-economy.md`. Goal (user): "give lots of XP for big main quests,
because we delete a lot of trash." Translate the XP removed by the trash cut into the big
guaranteed quest awards, so progression is preserved (or slightly raised) but **earned from
quests, not trash grinding**.

## The numbers we're working with (per character)
- Total SoD gain ≈ **665–715k/char**. Quest XP ≈ **585k** (scripts ~235k + dialogue ~350k);
  kill XP ≈ **80–130k**.
- A ~70% trash cut removes ≈ **50–90k/char** (~10% of total SoD XP). Net reinjection target
  after retained 30% trash + buffed "meaningful" fights ≈ **40–70k/char** (design figure ~60k).
- **No SoD XP cap on this install** (XPCAP all −1), so reinjected XP actually lands.

## Mechanic nuance that drives the method
- Kill XP is **split across the party**; quest awards (`AddexperienceParty`/`AddXPObject`) give
  the **full** amount to **each** member. So shifting XP from kills → quests is per-character
  *more* generous at the same nominal total — good, it matches "big quests feel rewarding."
- **Most SoD quest XP is in `.dlg`, not `.baf`** (~350k vs ~235k). The reweight mod **must
  patch dialogue awards**, not just scripts. (WeiDU: `COMPILE` a `.d` patch / `ADD_TRANS_ACTION`
  or `REPLACE_TEXTUALLY` on the decompiled action; more involved than `.baf` — budget for it.)

## Reinjection targets — the big guaranteed milestones
Scale these proportionally to absorb the removed trash XP (preserve reward *shape*):

| Award | Where | Current | Type |
|---|---|---|---|
| 4 chapter transitions (Ch.9/10/11/12) | BD7100, BD3000, BD4000, BD4400 | 65k total | script |
| Coldhearth Lich | BD1200 | 22k | script |
| Kherriun + Dark Magicians | BD5300 | 12k | script |
| Free Halatathlaer (dragon spirit) | BDHALAT/BDCORWIJ | 32k | dialogue |
| Free Daeros ghost | BDDAEROS | 18k | dialogue |

These ~149k/char of guaranteed awards are the natural carriers. A **uniform ~1.10–1.15× scale**
on them re-injects ~15–22k; to hit ~60k, either scale wider (include more mid-tier quest awards)
or apply a larger factor on the top milestones. Exact factor finalized once the cut proposals
(`docs/design/02a/02b/02c`) report the precise removed-trash XP per region.

## Decision for the user
- **XP-neutral** (preserve total SoD progression; just move it from trash → quests) — default,
  cleanest, keeps balance vs the rest of the modded game.
- **Generous** (+10–20% net; you said "lots of XP for big quests") — viable since there's no
  cap, but watch over-leveling into BG2. Recommend XP-neutral unless you want SoD to leave you
  a bit stronger.
- Scope: scale only the **guaranteed main-quest** milestones (above), or also bump notable
  **side-quest** awards (M'Khiin, ogre tribe, etc.)?

## Implementation note (later)
Two-surface patch in the tail-mod: (1) `.baf` — recompile area/creature scripts with scaled
`AddexperienceParty` values; (2) `.dlg` — patch the dialogue award actions. Both reversible.
Coordinate with the trash-cut mod so the removed-XP figure and the reinjection match.
