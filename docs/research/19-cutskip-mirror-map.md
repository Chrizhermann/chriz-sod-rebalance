# 19 — CUTSKIP mirror map: the SoD cutscene-skip rig, fully audited

Status: **verified** against the live install's `override/CUTSKIP.bcs` (decompiled
2026-07-13, now in the corpus as `research/data/sod_baf/CUTSKIP.baf`) and the dev
install's post-v0.6.1 copy. Closes the systemic audit left open by issue #5 (PT-5).

**Verdict up front: no new actionable mirrors.** Every shipped component is either
already skip-proof (comp245/280), defuses its mirror at the launch site
(comp120/130/140/150+160), or is untouched by the mirror's vanilla replay
(comp197/260/270). Three mirrors are watch items for the not-yet-built ending rework.

## 1. How the rig works (mechanism, verified from the decompile)

- A skippable cutscene arms itself: `SetAreaScript("cutskip",OVERRIDE)` +
  `SetGlobal("BD_CUTSCENE_BREAKABLE","GLOBAL",N)` + `SetCutSceneBreakable(TRUE)`,
  and disarms both (`BREAKABLE=0`, area script restored) in its final block.
- When the player skips, `CUTSKIP.bcs` fires as the area's OVERRIDE script. Its first
  block does generic teardown (fade, clear actions); its second block is one giant
  `Switch("BD_CUTSCENE_BREAKABLE","GLOBAL")` whose `RESPONSE #N` is selected by the
  global's VALUE — each response is a hand-mirrored **end-state replay** of cutscene N.
- Consequence for us (the PT-5 lesson): patching a cutscene's actions does NOT patch
  its mirror. A skipped cutscene replays the VANILLA end-state.
- Helper family: `CUTMOVE`/`CUTMOVE1`/`CUTMOVE2`/`CUTMOVE3` (party area-move used by
  response #11; corpus'd alongside). `CUTSKIP1.bcs` / `CUTSKIP2.bcs` are the SAME rig
  for the BG1:EE and BG2:EE campaigns respectively (confirmed by content: cutgor/cutsar
  vs CUT41A/cut01g) — relevant to the sibling `chriz-bg-rebalance` repo, not this one.
- Vanilla oddity: `BDCUT202` arms `BREAKABLE=43` but CUTSKIP has **no RESPONSE #43** —
  skipping it gets generic teardown only. Not our problem; noted for completeness.
- QA tail block: an `INI("QAMODE",1)`-gated debug string; inert in normal play.

## 2. ID → cutscene map (from `SetGlobal("BD_CUTSCENE_BREAKABLE",...,N)` grep over the corpus)

| RESPONSE # | Armed by | Scene | Intersects our mod? | Verdict |
|---|---|---|---|---|
| 1 | BDINTRO | Korlasz-dungeon walk-in intro | comp140 rewrites BDINTRO | **CLEAR** — comp140 seam 1 deliberately strips the breakable rig (arming it would strand BD0120 on cutskip); mirror unreachable |
| 11 | BDCUT11 | Hooded-man interrogation vision (destroys BDIRENI/BDCAELAR/BDHEPHER, chains `cutmove`) | comp120 removes the bdcut11 launch from BDCUT10 | **CLEAR** — dead code (cookbook §5 already noted this) |
| 14 | BDCUT14 | Coast Way bridge collapse (wall + parley timer) | comp200 | **FIXED by comp245** (v0.6.0) — dev decompile diff verified: wall pair gone, THREE→FIVE_ROUNDS |
| 15/16/17 | BDCUT15/16/17 | Caelar bridge parley staging/end | comp200 | **CLEAR** — #16's wall-down pair (`force_wall` off + door open) is a benign no-op post-comp200 |
| 20 | BDCUT20A | Boareskyr Bridgefort parley end (spawns/destroys BDCAELAR/BDHEPH2/BDSERV at bd7100, arms `bd_bence_delay`) | comp197 guards bd7100/bdbence for in-party Skie | **CLEAR** — mirror replays the vanilla flow comp197 deliberately keeps reachable; touches no Skie state |
| 30 | BDCUT30A | bd3000 FF arrival | none | not ours |
| 41/42 | BDCUT41/42 | bd4000 war-council scenes (#41 chains bdcut42; #42 ends in bddelanc dialog) | comp260's ch-11 XP chunk rides bd4000.bcs `AddXPObject(Player1,20000)` | **CLEAR** — skip path converges on the same dialog → same transition block → chunk fires |
| 43 | BDCUT202 | (no handler — vanilla gap) | — | n/a |
| 44/45 | BDCUT203/204 | M'Khiin/Baeloth goblin scenes (#45 sets `BD_Baeloth_run_away`) | comp260 actor cuts nearby | **CLEAR** — mirrors only reposition/destroy/face; they spawn nothing we removed |
| 46–49 | BDDDD1–4 A/B/C | The four chapter rest-dreams (BD0072) | comp130 | **CLEAR** — skipdrm.baf parks `bd_ddd=4`; dreams never launch, mirrors dead |
| 50 | BDCUT08 | (chains bdcut09) | none | not ours |
| 51 | BDCUT61A | **Trial entry** (chains bdcut61t) | ending rework (planned) | **WATCH** — the trial/jail removal must handle or defuse this mirror |
| 52 | BDCUT57 | Belhifet staging (bdbelhif heal + dialog) | ending rework (planned) | **WATCH** |
| 59 | BDCUT59 | (chains bdcut59a) | none | not ours |
| 60/61/62 | BDCUT45/45A/45B | Basement reveal + portal variants | comp280 | **FIXED by comp280** (v0.6.0) — both `bddispel`×6 mirrors (#61, #62) removed, verified; #60 carries no dispel |
| 65/66 | BDCUT50/51 | Avernus scenes (bdpremat/bdcaelar) | ending rework (planned) | **WATCH** (only if those scenes are touched) |
| 67 | BDCUT65 | **SoD→BG2 transition into BD6100** (party LeaveAreaLUA, then IMOEN2 dialog; launched by BDCUT64X, which is NOT itself skippable) | ending rework (planned) | **WATCH** — interacts with the EET hard requirement (party must end in BD6100); mirror #67 jumps the party in bd6100 and starts the IMOEN2 dialog |
| 68 | BDCUT02 | Palace-intro assassins vs Imoen (sets `bd_001_plot=2`) | comp150/160 rework the palace flow | **CLEAR** — comp150's arrival rig (`baf/csrarr.baf`) pre-sets `BD_INTRO_IMOEN_CUT=1`, the exact gate on BD0103's launcher; scene never fires |

Not skippable at all (no `BD_CUTSCENE_BREAKABLE` setter → **no mirror exists**):
**BDCUT10, BDCUT28** (the two comp120 targets the issue asked about first),
BDCUTKOR (comp170), BDSODTRN (comp140), BDCUT00Z (our skip-spine target), BDCUT64X.
None of our own custom rigs (`baf/`, `dlg/`) arm the breakable system — verified by grep.

## 3. Comp245/280 install verification (dev vs live decompile diff)

The complete diff between the live (vanilla) and dev (v0.6.1-installed) CUTSKIP is
exactly: response #14 minus `AmbientActivate("force_wall",TRUE)` +
`CloseDoor("force_wall_door")`, `bd_caelar_timer` THREE→FIVE_ROUNDS (comp245); and
responses #61+#62 each minus six `ReallyForceSpellRES("bddispel",PlayerN)` (comp280).
Nothing else differs. Both components landed surgically.

## 4. Corpus gap — closed

The corpus was generated from `BD*.bcs` only (1232 files = exact `BD*.bcs` count in
the live override), which is why CUTSKIP was invisible to every audit before PT-5.
Added from the live install (2026-07-13): `CUTSKIP.baf`, `CUTMOVE.baf`,
`CUTMOVE1-3.baf` → corpus now 1237 files. Any future regeneration must include the
pattern `CUT*.bcs`, filtered to the SoD rig family (CUTSKIP + CUTMOVE*), or simply
keep these five files.

## 5. House rule (also added to methods-cookbook §16 and the bg-modding skill)

**Every time a `BDCUT*`/`BDDDD*` cutscene is patched, grep `CUTSKIP.baf` for its
`RESPONSE #N`** (N from the scene's own `SetGlobal("BD_CUTSCENE_BREAKABLE",...,N)` —
note: N is NOT always the cutscene's number, e.g. BDCUT45A→61, BDCUT02→68). If the
scene can still launch under our mod, its mirror must receive the same end-state
edits, count-guarded (comp245 is the reference implementation). If the launch is
removed, the mirror is dead code — leave it. When killing a cutscene entirely, prefer
comp140's approach: strip the arming actions too, so the area script is never left
pointed at "cutskip".
