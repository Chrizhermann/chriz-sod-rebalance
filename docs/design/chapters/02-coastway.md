# Chapter Pass — Coast Way tier (BD1000 / BD1100 / BD1200 / BD7000)

**Status: ROUND 1 DECIDED (2026-07-08) — round 2 open on dungeon layout details.**
Inputs: the user's parked notes (`02-coastway-notes.md`) + the verified census
(`docs/research/12-coastway-census.md`) + sparring round 1 (all decisions user-made).
Nothing below is implemented yet.

## 0. What the census corrects

- **There is no separate "first camp" area.** The Flaming Fist Encampment IS
  BD1000 (Coast Way Crossing) — companions are relocated into it at
  `BD1000.baf:149-283`. "Put Rasaad in the camp" therefore means: move his spawn
  block to BD1000.
- The "vampire hunters area" = **BD7000 Coast Way Forest** (worldmap node), also
  hosting the 22-orc warband, a random-encounter hook — and **a Skie sub-quest**
  (regions `Sddskie1`/`Skie_escape`).
- The dwarf dungeon's undead are **100% pre-placed actors, zero scripted spawns**
  — a cut is pure ARE surgery, no script seams to respect (boss/quest scripts are
  separate and untouched).

## 1. Coast Way Crossing (BD1000) — DECIDED (round 1, 2026-07-08)

- **West spider installation FULLY removed**: the 8 placed NW spiders (SPIDPH ×3,
  BDSPIDGA ×2, SPIDGI ×2, SPIDHU ×1 at X≈467-644/Y≈1459-1594) AND the `Spiders02`
  re-arm spawn point AND the two web traps beside them. East spider group
  untouched. (User: "the 8 placed ones, delete all the rest.")
- **Magic wall removed** from the bridge fight: drop `BDCUT14.baf:397-403`
  (bdwforce cast + SPFLESHS VFX + `AmbientActivate("force_wall")` +
  `CloseDoor("force_wall_door")`).
- **Fight-interrupt timer = FIVE_ROUNDS** (~167% of vanilla's THREE_ROUNDS;
  `SetGlobalTimer("bd_caelar_timer","bd1000",...)`, `BDCUT14.baf:417`).

## 2. BD7000 REMOVED + Rasaad to camp — DECIDED (round 1, 2026-07-08)

- **The whole area is removed** ("just remove it") — worldmap entry stripped /
  never revealed (standalone-vs-EET reveal mechanics verified at implementation).
- **Rasaad**: his spawn block (`BD7000.baf:20-78`) is self-contained — relocated
  to the BD1000 camp (one of the companion camp spots, `BD1000.baf:149-283`;
  exact spot picked at implementation).
- **Removed-content treasure = a mod-wide CHOICE component** (user proposal,
  agreed): one component "treasure from removed content" with two flavors —
  (a) collected conveniently in a container, (b) removed with the content. Every
  chapter pass reuses it. BD7000 payload: Gemblade (BDDAGG03), Tsolak's ring09
  (Ring of Free Action — situational, many parties have spares), SODTRE08 ×2 /
  SODTRE09 / BDMISC63. Container location TBD at implementation (a camp crate in
  BD1000 is the natural spot). Tsolak/hunter carried gear still unverified —
  check before finalizing the payload.
- **The Skie sub-quest dies with the area** ("probably just remove") — consistent
  with the broader direction: SoD's Skie plot gets removed/heavily rewritten (tied
  to Entar-stays-dead); Skie-playable (wishlist item 12) is unaffected.
  Implementation check: verify no downstream content reads the `Sddskie1`/
  `Skie_escape` globals before deleting.

## 3. Dwarven dig site (BD1100/BD1200) — SHAPE DECIDED (round 1); layout = round 2

**User's target shape (2026-07-08), replacing the ~203-hostile garrison:**
- **ONE horde room** — a single chamber that "makes sense" fiction-wise, packed
  with tons of WEAK undead (the AoE set-piece). Nothing else big.
- **A couple of scary-but-few encounters** (more scary, fewer bodies).
- **~3 easy pushover groups** (plain zombies/skeletons).
- **ONE hard group of big, tough undead** — candidate placement: the threshold
  "room that has to be opened" before the lich (BD1200 has a script-detected
  secret door `Secret02`, `BD1200.baf:213-221` — verified).
- **Everything else deleted.**

**Hard bans (LOCKED, and noted as a cross-chapter rule):**
- **Shadowed souls (BDSHSOUL ×10) removed — and everywhere else they appear in
  SoD** ("those creatures should not exist anywhere": no-save, no-attack-roll
  touch).
- **Bone bats (BDBONBAT ×17): not fun — removed.**
- **Unsleeping Guardian (BDUNSLGU): not fun — removed.**

**Lich fight: DEFERRED** (improve later, not v1). User verdict on the vanilla
mechanic: the phylactery sequence is boring if you know it, frustrating if you
don't (lich vastly over-leveled). Parked ideas for that later pass: (a) telegraph
the phylactery openly (dwarves' notes / Deepvein says it plainly) and put it
where the fight happens so the loop is visible; (b) make phylactery destruction
a mid-fight power-down (strips his defenses) instead of a hidden kill-permission;
(c) level-appropriate SCS brain + one signature sequencer (Korlasz pattern)
instead of raw level inflation. The 22,000 XP clean-kill award and quest scripts
are untouched by the garrison cut.

**[ROUND 2 — proposed layout, awaiting user tweaks]** (numbers are proposals):
- L1 (upper): pushover group A (4-5 zombies, entrance corridor), pushover group B
  (3-4 ghouls), one scary single (a lone mummy in a burial niche). Dig-monsters
  (26 crawlers/umber hulks/otyughs) — OPEN: cut to one small scare (e.g. an umber
  hulk pair, save-able gaze) or delete entirely.
- L2 (lower): the HORDE ROOM (~16-18 weak: shambling zombies + skeletons + a few
  ghouls) in the big ossuary chamber; one scary pair (greater ghasts — paralysis
  saves, no drain); pushover group C; the HARD group at the Secret02 threshold.
- Hard-group composition options (all SoD-native, no cheap mechanics):
  (a) honor guard: 2× mummy (BDMUMM01) + 2× elite skeleton guard (BDSKGR07/08) —
      recommended: big, tough, everything save-able/curable;
  (b) all-elite skeleton pack: 4-5 top-tier BDSKGR — pure armored melee, wants
      blunt weapons (tactical, never unfair);
  (c) mummy anchor: 1 leveled-up mummy mini-boss (Korlasz-crew treatment) + 2
      greater ghasts.
- XP ledger row sized after the layout locks (delivery per prologue §7 rule if
  compensation is wanted).

## 4. Backtracking without EET — [USER NOTE, global lever]

Parity with EET's backtracking on standalone. Global design (not this tier alone);
parked here until its own pass.

## OPEN — round 2

1. §3 layout sign-off: the proposed distribution above (counts, rooms), hard-group
   option (a)/(b)/(c), dig-monster disposition, horde-room placement (L2 ossuary
   vs an L1 chamber).
2. §3 XP ledger: compensate the cut garrison (one collected award) or let it go.
3. §2 container spot for the "keep removed-content treasure" flavor (camp crate?).
