# Design 04 — Creature Softening (PROPOSAL)

Depends on `docs/research/06-creature-danger.md` (verified stats/resistances on this install,
post-AK/CDTweaks/SCS). Goal: make ambush/trash fights *fair* — stop nullifying the player's
toolkit — without gutting iconic mechanics or scripted set-pieces. Pairs with the rest-table
curation in `design/01` (lever 3) and the trash cuts in `design/02*`.

## Two complementary approaches
- **(A) Table/pack curation** (cheapest, no CRE edits): keep the rigged creatures out of the
  *rest tables* and thin them from trash packs. Done in design 01/02.
- **(B) CRE softening** (edit the creature): needed where the rigged creature is the *placed*
  encounter you still fight (e.g. the Korlasz catacombs are wall-to-wall `BDSKGR*` even after a
  70% cut). Without (B) the prologue dungeon stays a blunt-weapon-only slog.

Recommend **A everywhere + B on the prologue skeletons** (highest leverage, smallest blast radius).

## Priority 1 — Korlasz catacomb skeletons `BDSKGR00–04`
Verified: **missile 90% / slash 50% / pierce 50% / crush 0%**, plus `RING95` (immune
sleep/charm/hold/horror/confusion/poison) and engine-undead immunity → archery dead, most
weapons halved, all low-level CC blank. The single worst toolkit-nullifier in SoD.

Proposed (the rest-table set, and ideally the placed catacomb set):
- **Missile 90 → 0** (archery should work — this is the biggest single quality win).
- **Slash 50 → 0, Pierce 50 → 0** (swords/spears do full damage; crush stays full).
- Leave the engine undead immunities (CC-immunity is thematically fine for *undead*; the
  resistances are the real problem, not the CC). Optionally drop `RING95` if you also want
  low-level CC to work on them — flag for you; default = keep.
- `BDSKGR07` (hidden skeleton **mage**): fine as a set-piece elite, but remove from random/trash
  packs so it isn't a surprise caster in filler.

## Priority 2 — Trolls (`TROLL01/SM`, `TROLFR01`, `BDTROLL1/2`)
Verified: `TROLLREG` does op17 "set HP to 100%" on down unless finished with fire/acid; SCS adds
+2 HP/round. This is the *intended* troll mechanic — **do not remove it.** Instead:
- Keep trolls **out of rest tables** (design 01 already pulls `TROLL01` from BD7100's table).
- For placed trolls, leave the mechanic. The Troll Claw cut (32→12) already reduces the volume.
- No CRE change recommended (preserves the fire/acid skill-check that makes trolls trolls).

## Priority 3 — situational (low priority, scripted-only)
- **`IMMUNE1` carriers** (op120 immune to non-magical weapons): `BDWOLFVA`, `BDSHSOUL`,
  `BDSKGR08` boss, `BDIMP`. All scripted/elite, not in random rest tables → leave as-is (a
  mundane-weapon party has +items by then; it's an intended elite trait).
- **Slimes `JELLOC`/`JELLYGR`** (missile 100%, JELLOC splits): keep out of rest tables (design 01
  already excludes them from the "safe fodder" list); leave the CRE (immune-to-arrows is the
  slime's whole identity).

## "Safe fodder" rest-table whitelist (from the audit)
Use only these in rest tables: **wolves, bandits, hobgoblins, orcs, huge spiders, boars** —
none have toolkit-nullifying resistances. Everything else (skeletons/trolls/slimes/fiends/
shadows) → scripted placed encounters only.

## Decisions for you
1. Apply CRE softening (B) to the prologue skeletons, or rely on table curation + cuts alone?
   (Recommend B — the catacombs are skeleton-dense even after cutting.)
2. Drop `RING95` so low-level CC works on the catacomb skeletons, or keep undead CC-immunity?
   (Recommend keep — undead CC-immunity is genre-correct; the resistances are the real issue.)
3. Scope of softening: only the prologue `BDSKGR*`, or the same resistances wherever `BDSKGR*`
   appear game-wide? (Recommend game-wide — same CREs, consistent feel.)

## Implementation note (later)
WeiDU `COPY_EXISTING` each `BDSKGR0*.cre`, patch the damage-resistance fields (verify offsets via
the bg-modding skill / IESDP — research/06 corrected one IESDP offset already), reversible. If
dropping `RING95`, remove the item from the CRE's inventory/equip slots. Live saves: already-
spawned skeletons keep old stats; newly-spawned (post-install) use the patched CRE.
