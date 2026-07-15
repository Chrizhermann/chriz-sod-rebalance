# Chapter Pass — Coast Way tier (BD1000 / BD1100 / BD1200 / BD7000)

**Status: IMPLEMENTED through v0.6.3 (2026-07-15) — all selected components
installed + semantically verified on dev; runtime playtest pending for the latest
follow-up.** Components: 200 (Crossing field pass), 210 (BD7000 removal + Rasaad
at camp), 215 (BD7000 XP), 220 (dig-site re-garrison + XP chunk), 225 (single
Caelar omen), 245 (skip-proof bridge), and 900/901 (treasure choice; 900 selected).
Inputs: the user's parked notes (`02-coastway-notes.md`) + the verified census
(`docs/research/12-coastway-census.md`) + user sparring rounds.

Implemented specifics (final numbers): removal mechanism = actor appearance-
schedule 0 (verified live hour-bits; matched by CRE@x@y, count-guarded);
garrison 175,495 kill-XP → kept 46,875, cut 128,620 → **chunk 17,100/char**
on the lich clean-kill (`AddexperienceParty(22000)` + `(17100)`); Rasaad camp
spot [640.3690] (companion row, no Chapter gate — recruitable all campaign,
guarded by vanilla's own `bd_rasaad_spawn`); BD7000 removal = its static WMP
visibility flag zeroed (the only reveal mechanism; save-baked worldmaps keep
it — applies to runs that haven't generated the SoD map yet); treasure chest =
Container009 (509,3220): SW1H01 + Gemblade + Suncatcher +2 + Boot and a Half
of Speed + Wand of Paralyzation (5) + Ring of Free Action + SODTRE08 ×2 +
SODTRE09 (skipped: mundane hunter gear, BDSTAKE, Crusader Tract, DW#*
randomiser items); honor guard placed on the Door08→Secret02 corridor at
(3832,1962)/(3905,1983)/(3978,2003)/(4040,2022) facing west; horde-ins landed
on vacated cluster-A coordinates (known-walkable); dwarf-barricade beat = the
quest wight BD_DOD_WIGHT1 + 4 zombies (Deepvein's `Dead("BD_DOD_WIGHT1")`
dialog trigger verified); Semahl's five BDATKSEM untouched
(SPRITE_IS_DEADBDATKSEM==5 win condition verified).

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

**ROUND 2 LOCKED (2026-07-08):**
- **Hard group = option (a) "honor guard"**: 2× mummy (BDMUMM01) + 2× elite
  skeleton guard (top-tier BDSKGR), placed at the Secret02 threshold before the
  lich.
- **Layout as proposed**: L1 = pushover group A (4-5 zombies, entrance), pushover
  group B (3-4 ghouls), one lone-mummy scare in a burial niche; L2 = the HORDE
  ROOM (~16-18 weak: zombies/skeletons/a few ghouls, big ossuary chamber), one
  greater-ghast pair, pushover group C, the hard group at the door.
- **Dig-monsters**: DELETE the carrion crawlers (BDMCARRI/BDCCRAW1/CARRIO) and
  otyughs; **KEEP only umber hulks** ("just leave some umber hulks") — plan: one
  group of 3 of the 4 placed BDUMBER1 (burrowers are the one thing that fits the
  dig fiction).
- **SEMAHL CONSTRAINT (user)**: some creatures fight the giant Semahl (BDSEMAHL,
  the L1 rescue beat) — "nothing crazy." Verify his fight wiring before cutting
  and keep whatever small group his beat needs.
- **XP compensation**: collect MOST of the cut kill-XP and grant it as **ONE
  chunk, all at once, as a quest reward on the LICH** (user proposal, agreed).
  Implementation point: the existing clean-kill `AddExperienceParty(22000)`
  block (`BD1200.baf:10-18`) gets the chunk added. Caveat (surfaced): that path
  requires the phylactery destroyed first — vanilla's only closure, coherent
  with "finish the dungeon, collect the dungeon's XP"; the deferred lich rework
  keeps clean-kill as the standard path. Chunk sized at implementation from the
  summed CRE kill-XP (0x14) of every cut actor — "most" ≈ 80%, exact number when
  the sums are in.
- **Treasure container ("keep" flavor)**: an EXISTING BD1000 container that
  makes sense (camp area preferred) — picked at implementation from the ARE
  container list ("just do something that somewhat makes sense").

## 3a. Playtest follow-ups — dig site (user report 2026-07-08)

**Root cause VERIFIED (2026-07-10, post-220 dev BD1200.ARE parsed — 131 actors: 94
cut/sched-0, 11 moved/live, 26 kept/live):** the honor guard IS placed with live
schedules at (3832,1962)/(3905,1983)/(3978,2003)/(4040,2022) — but those four coords
were interpolated along the Door08(3670,1904)→Secret02(4124,2044) line, a corridor
holding ZERO vanilla-placed actors (unverified terrain), and idx96's (4040,2022) sits
essentially ON Secret02's closed-door footprint (4051,1987–4197,2102). Off-mesh
placement → the guard never engaged. The 7 horde-room moves that DID work all reused
vacated cut-actor coords. **Rule learned: place only on vacated coords (walkable by
construction) or WED-verified tiles — never interpolate.**

**EXECUTED 2026-07-10 (user decisions):** the six drowned are CUT and the honor guard
stands ON four of their vacated coords — mummies on the flanks (3533,1643)/(3315,1772),
skeleton warriors centre (3482,1682)/(3471,1632) — literal replacement, per the new
locked rule: **never place creatures where no enemy was placed before** (vacated
original-actor coords or searchmap-verified tiles only). NO backfill bodies: the
drowned's 4,800 party XP returns through the ledger chunk instead, regenerated
**17,100 → 17,800/char** (generator = research/scripts/gen220.py, which now reads the
pre-220 pristine AREs from the WeiDU backup — regenerating from the post-install
override would bake in wrong keys). Reinstalled + verified on dev (ARE parse: guard
live on the four coords, all 10 BDDEAD01 schedule-0; bd1200.bcs carries 22,000+17,800).
Placement options B/C below are kept for the record only. The BG2-style XP-tiered
miniboss idea ("lich-lite") is noted for LATER — research docs 17/18 in flight.

The gathered data (kept for the record):
1. **Drop the 6 BDDEAD01** ("Drowned in Blood", 800 XP each) from KEEP_1200 —
   idx 4/5/6/7/103/104, clustered in the Crimson-Pool room (x3235–3576, the room
   before the lich).
2. **Re-place the honor guard** (BDMUMM01 idx78/96 + BDSKGR08 idx108/109). Search-map
   parse (BD1200SR.BMP, 2026-07-10) PROVED the root cause: the four guards are the ONLY
   actors in the whole area on impassable void (palette idx0) — the real Door08→Secret02
   corridor is a bent diagonal staircase the straight-line interpolation cut across.
   Three verified placements to pick from (all searchmap-walkable, reachable, roomy):
   - OPTION A — room east-exit line (vacated cut-actor coords, west of Door08):
     (3495,1820)/(3457,1782)/(3533,1643)/(3576,1614).
   - OPTION B — literal corridor line, spaced down the real staircase (agent-recommended;
     reads as guards lining the approach, cleanly separate from the backfill room):
     (3704,1950) Door08 mouth / (3816,2034) / (3928,2070) / (4040,2118) Secret02 threshold.
   - OPTION C — 4-wide wall right at Secret02's door (player hits them together):
     (4056,2118)/(4008,2106)/(3976,2130)/(3944,2082).
   Facing the approach (orient ~NW) is a cosmetic nicety over the current W.
   **Reusable walkability recipe (any future placement):** a coord (x,y) is walkable iff
   `<AREA>SR.BMP` cell `(floor(x/16), floor(y/12))` has palette index ∈ {4,7,8,12}
   (4-bpp bottom-up BMP, cell = 16×12 px; verify reachability by flood-fill from a
   known-walkable point — palette idx0 = void).
3. **Backfill a varied weak mix** on the remaining vacated anchors (all walkable by
   construction): (3396,1665)/(3339,1688)/(3305,1644)/(3267,1766)/(3291,1733)/
   (3315,1772)/(3235,1804)/(3471,1632)/(3482,1682). Species menu (kill-XP): ZOMBIE 65 ·
   BDSHZOM1 65 · GHOUL 175 · BDSKGR04 250 · BDSKGR05/06 300 · BDSKGR02 400 · GHAST 650.
   (Banned per the no-cheese rule: BDSHSOUL/BDBONBAT/BDUNSLGU; SKELDED is a 0-XP corpse
   prop, not a combatant.)
4. **XP coupling (OPEN):** the 6 drowned (4,800 party XP) counted as "kept" when the
   17,100/char chunk was sized. Either size the backfill to ≈4,800 kill-XP (≈12–15
   weak bodies) so 17,100 stays exact, or resize: new = (128,620 + 4,800 − W)·0.8/6.
5. (Optional, separate room: the N-chamber vacated coords, x2950–3396/y894–1200 via
   Door04, could host a pushover pocket.)

Mechanics: revise KEEP_1200 + MOVES_1200 in `scratchpad/gen220.py`, regenerate
`lib/comp220_lists.tpa`, reinstall 220, re-verify. (220 sits mid-tail on dev; WeiDU
auto-redoes the later components 200/900/185/190/195 — all ours, acceptable on dev.)

## 3b. Dig-site scrying pool — LOCKED + SHIPPED (component 225, 2026-07-15)

The old flow was initially misread. `BD_SDDD12_CLOUDY` defaults to 0, so completing
the three-scepter pedestal made the **first** old vision free. Each picker choice then
set the pool cloudy; the two vanilla Essences paid for old visions two and three.
Component 220's cut of `BDWIGHDD` therefore removed a vial source but did not block
either post-component-120 vision: Imoen and Caelar needed only the free activation plus
the surviving Shelf vial. Full corrected trace: `docs/research/20-scrying-pool.md`.

**User decision:** retire the gimmick cleanly. The Imoen vision is incoherent when
component 160 can put her in the party, the Hooded-Man option was already gone, and the
original Caelar army cinematic is overbuilt. All picker choices and every route through
`BDSCRY01`–`BDSCRY07` are now unreachable. In their place, completing the pedestal and
bringing **both** Essences produces one exact, abstract, text-only Caelar omen—no dialog
menu, cutscene mode, area travel, actor creation, or repeat loop.

Component 225 keeps the three scepters and their 3,000 party-total completion reward,
requires and consumes both Essences atomically, grants 1,000 XP once to each of
Player1–6, restores the murky ambient state, and makes the pool permanently dormant.
`BDWIGHDD` stays schedule-zero; its vial is re-homed into the existing unlocked,
untrapped `Sarcophagus01` at `(2414,1736)` beside that container's scepter. The original
`BDSCRY.DLG` structure remains installed for third-party compatibility (including Aura's
state-0 interjection), but it has no live launcher and all six vanilla picker routes are
False-gated.

**Verification:** sandbox green; v0.6.3 tail-installed on the dev EET copy; installed-
resource verifier `SUMMARY: 0 failure(s)`. Natural item pickup, activation, save/reload,
and dormant re-click remain for the next SoD playthrough. The live v0.5.0 install was
not changed.

## 4. Backtracking without EET — [USER NOTE, global lever]

Parity with EET's backtracking on standalone. Global design (not this tier alone);
parked here until its own pass.

## Implementation-time verifications (before/while building)

1. Semahl's fight wiring on BD1100 — which undead engage him; keep the beat
   functional with a small group.
2. `Sddskie1`/`Skie_escape` + SDD123 globals — confirm nothing downstream reads
   them before deleting BD7000 content.
3. BD7000 worldmap reveal mechanism (EET vs standalone) for the removal shape.
4. Tsolak/Isabella/Ikros carried gear — completes the treasure-component payload.
5. BD1000 container enumeration — pick the treasure crate.
6. Actor-coordinate layout for BD1100/BD1200 — choose kept clusters per the
   locked layout, position the hard group at Secret02, sum the cut kill-XP.
7. Rasaad's camp spot among the `BD1000.baf:149-283` relocation points.
