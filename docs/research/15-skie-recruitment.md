# 15 — Skie: current SoD recruitment lifecycle (research)

> Research data gathered by subagent 2026-07-10; verified against dev install +
> repo decompiles. DATA ONLY — decisions live in `docs/design/` and
> `docs/01-remix-wishlist.md`. Evidence-cited throughout; `UNVERIFIED` labels
> mark inferences not proven in-game.
>
> Dev install = `C:\Games\Baldur's Gate II Enhanced Edition modded - dev eet install`
> (read-only). Decompiles via `weidu.exe` (v24600) into scratchpad. Line numbers
> for `BD*.baf` refer to the repo corpus `research/data/sod_baf/`; the dev
> `BDSKIE.dlg`/`.bcs` were freshly decompiled (they carry comp190's gate).

---

## 0. TL;DR — minimal talk-to-join surface

- **The join machinery already exists and already IS "talk-to-join":**
  `BDSKIE.dlg` states **5→6** (first recruit) and **1→2** (re-recruit) call
  `JoinParty()`, gated only to the camp areas **BD0120/BD0130** via the shared
  SoD `bd_joined`/`bd_npc_camp` LOCALS. **Those two are the ONLY `JoinParty()`
  calls in her entire dialog.** Everything else is plot scaffolding that
  eventually deposits her into that camp pool.
- **Her BG1 soundset is already in place.** The SoD joinable `BDSKIE.CRE` voices
  from the exact same strref block as the BG1-imported `SKIE.CRE` → WAV resrefs
  `SKIEE##`. A "BG1 soundset swap" is essentially a no-op (details §5).
- **Already handled by shipped components:** night "don't tell Daddy" visit
  (comp190), the BD7000 beast vignette (comp210 area removal), Entar in the city
  (comp185).
- **Still entangled (deferred):** the Ducal-Palace first meeting (states 8–15,
  ends by making her *leave*), the BD2000 Bence intro (33–36), the BD4000/BD4100
  `bd_skie_plot` subquest negotiation (37–62), the BD7100 Bence dig/discipline
  (84–90). A clean talk-to-join means picking ONE early spot, wiring a short
  exchange to `JoinParty()`, and neutralising these spawns/gates.
- **Depends on the epilogue/dream pass (do NOT touch here):** trigger-less state
  0 → `bdcut60y` (the hooded-man/Irenicus dream that turns Skie into the
  "Unknowable Horror" `bdskiedr`); her canonical death/trial (`BDSKIED.CRE`).

---

## 1. Identity & file inventory (dev `override\`)

| File | Size | Role | Key fields (verified) |
|---|---|---|---|
| `BDSKIE.CRE` | 3952 | **The joinable** | `dlg=BDSKIE`, DV=`BDSKIE`, EA=128 (NEUTRAL), override script=`BDSKIE`, class script empty (combat AI applied on join) |
| `BDSKIE.bcs` | 8818 | Her override state machine (§4) | — |
| `BDSKIEC.bcs` | 12950 | Generic BD **party combat AI** (`BDAI_*`, potions, stealth, attack) — nothing recruitment-specific | — |
| `BDSKIE.dlg` | 13495 | **91 states / 196 transitions** (§3) — carries comp190's `False()` on state 16 | — |
| `BDSKIEJ.dlg` | 52 | Journal/join stub — **empty** (`BEGIN ~BDSKIEJ~`, no states) | — |
| `BDSKIED.CRE` | 3872 | Skie **dead body** (finale/trial) → epilogue pass; referenced `BD4100.baf:40` | — |
| `BDSKIEDR.CRE`/`.bcs`/`.ITM` | — | Dream "**Unknowable Horror**" form + its script + natural weapon → dream pass | — |
| `BDCSKIE1.bcs`/`BDCSKIE2.bcs` | — | Beast-vignette cutscenes (BD7000) | — |
| `SKIE.CRE` / `SKIE6.CRE` | 3492/3512 | **BG1 Skie** (EET-imported): `dlg=skie`, DV=`SKIE`, script `SKIE_` — the BG1 soundset donor (§5) | — |

Different identity between eras: the SoD joinable is `BDSKIE` (dlg/DV/script all
`BDSKIE`); the BG1 creature is `SKIE`/`skie`/`SKIE_`. They are **not** the same
CRE; they only share audio strrefs.

---

## 2. Where she physically appears (every spawn)

Method column: `CreateCreature` = script-spawned; `ARE actor` = statically
placed. All areas grepped in `sod_baf` + a binary scan of every `override\*.are`
(only `BD4000.ARE` contains her resref).

| # | Area | Method / evidence | Gate | Status |
|---|---|---|---|---|
| 1 | **BD0102 Ducal Palace** (war council) | `CreateCreature("BDSKIE",…)` ×5 council variants — `BD0102.baf:33,82,133,184,235`; despawn `ApplySpellRES("bddest","bdskie")` `BD0102.baf:295` | plot 51 council | **ACTIVE** — comp185 removed Entar but kept Skie. Also leaves via `EscapeBD0102`→`DestroySelf` (`BDSKIE.baf:63-79`) |
| 2 | **BD0103** night camp | `CreateCreature("bdskie",[443.476],NW)` ×2 — `BD0103.baf:920,984` | 2nd sleep, `BD_MDD005` | **PRE-EMPTED** by comp190.1 (`csr190wake.baf` EXTEND_TOP sets `BD_MDD005=1` first → both blocks skip) |
| 3 | **BD2000** (Bence intro) | `CreateCreature("bdbence",…)`+`CreateCreature("bdskie",…)` — `BD2000.baf:901,920` | `bd_plot`→293 | **ACTIVE** (entangled) |
| 4 | **BD4000** (subquest hub) | **static ARE actor** — `BD4000.ARE` (only area with her placed); driven by `BDSKIE.baf:98-139` | `bd_skie_plot`<10 | **ACTIVE** (entangled) |
| 5 | **BD4100** | `CreateCreature("bdskie",[2167.948],SW)` — `BD4100.baf:550`, unconditional at `bd_skie_plot=10` (per comp210 note, independent of BD7000) | `bd_skie_plot=10` | **ACTIVE** (entangled) |
| 6 | **BD7000** (beast vignette) | `CreateCreatureObject("bdskie",…)` + ogre `BDCCOGR1`; cutscene `bdcskie1` — `BDSDDSKI.baf:28-35` | Chapter 8, `bd_sddskie` | **UNREACHABLE** — comp210 zeroed BD7000's worldmap visible-flag |
| 7 | **BD7100 Coast Way camp** (Bence dig) | `CreateCreature("bdskie",[219.3452],SE)` — `BD7100.baf:562`; kill-Bence vignette `:564-578`; cleanup `DestroySelf` `:548-551` | `bd_sddskie` switch | **ACTIVE** (entangled) |
| 8 | **Camp BD0120 / BD0130** | shared camp-NPC framework (`bd_npc_camp`); dialog **states 1-7** | recruited / dismissed | **THE JOIN POINT** |
| 9 | Dream (BD4100) | `ChangeAnimation("bdskiedr")` — `BDCUT60Y.baf:73`; launcher `BD4100.baf:85-123` | `bd_plot` 590 | **DREAM/epilogue pass** |

Cutscenes that move/stage her: `BDCUT04.baf` / `BDCUT04A.baf` (palace roll-in;
`BDCUT04A.baf:12` fires `ActionOverride("BDSKIE",StartDialogNoSet(Player1))` →
opens the palace meeting), `BDCUT05.baf` (night-visit rest/wake, dialog state 26
target), `BDCUT60Y.baf` (dream), `BDCSKIE1/2` (beast vignette).

---

## 3. Dialogue map — `BDSKIE.dlg` (91 states, 196 transitions)

Binary header verified: 91 states (0–90), 196 transitions. States **0, 33, 36,
52** have `trigIndex = -1` (no trigger); all others carry triggers.

### Join / camp cluster — the recruitment core
| States | Trigger | Role | Actions |
|---|---|---|---|
| **1–4** | `OR(2) AreaCheck(BD0120/BD0130)` + `GlobalGT("bd_joined","locals",0)` | **Re-recruit / dismiss** (she's already been in party) | **2 → `JoinParty()`**; 3 → dismiss to camp (`bd_joined=0`,`bd_npc_camp=1`); 4 → `bd_joined=0` |
| **5–7** | `OR(2) AreaCheck(BD0120/BD0130)` + `Global("bd_joined","locals",0)` | **First recruit in camp** | **6 → `JoinParty()`**; 7 → exit |

`bd_joined` / `bd_npc_camp` are LOCALS on her CRE — the standard SoD camp-companion
handshake. **States 2 and 6 are the only `JoinParty()` calls in the file.**

### Plot scaffolding (all currently gate-in via her override script / area scripts)
| States | Trigger / entry | Role | Notes |
|---|---|---|---|
| **8–15** | `bd_plot_003 bd0102=2` + `EscapeBD0102=0`; entered by `BDCUT04A.baf:12` | **Ducal Palace first meeting** | sets `bd_pc_remembers_skie`, `bd_skie_entar_caelar` (state 13), `EscapeBD0102=1`, journal 256388. **Ends by her LEAVING** (state 15 farewell → override script walks her out & `DestroySelf`) — she does NOT join here |
| **16–32** | state 16 = `False()` **+** `BD_MDD005=1` | **Night "don't tell Daddy" visit** → `bdcut05` rest cutscene (state 26, journal 259627) | **DEAD:** comp190.2 (`csr190skie.d`) put `False()` on state 16 (the sole root); comp190.1 stops the BD0103 spawn. Whole 16–32 subtree unreachable |
| **33–36** | trigger-less; entered by `BDSKIE.baf:81-96` in BD2000 (`bd_plot=293`) | **Bence Duunton intro** | `EXTERN BDBENCE`; sets `bd_plot` 293→294 |
| **37–62** | `bd_skie_plot` <5 / <10 / =10 in BD4000/BD4100; entered by `BDSKIE.baf:98-150` | **Subquest negotiation** | CHA/class checks; party interjections `SAFANJ/VICONIJ/DORNJ/BDGLINTJ/KHALIJ/JAHEIRAJ/BDCORWIJ`. Advances `bd_skie_plot` 5→10→15; each terminal state `EscapeArea` (she leaves again) |
| **63–83** | `bd_sddskie(MYAREA)=2` + `AreaCheck(BD7000)` | **Beast fight** (kills ogre) → `bdcskie2`; `bd_sddskie_discipline` choice (82–83) | **UNREACHABLE** (comp210 removed BD7000) |
| **84–90** | `bd_sddskie=4` + `AreaCheck(BD7100)` | **Bence dig/march** | `EXTERN BDBENCE 107-110`; reads `bd_sddskie_discipline` |
| **0** | **trigger-less** | **Hooded-man DREAM** → `StartCutSceneEx("bdcut60y")` | Irenicus (`bdireni`) kills dream-Skie and morphs her into `bdskiedr` "Unknowable Horror" (`BDCUT60Y.baf`). **Dream/epilogue pass, not recruitment** |

### The trigger-less-state-0 question (important, partially UNVERIFIED)
Documented engine rule (`bg-modding/ie-scripting.md`): the start-scan takes the
first state whose trigger passes, and *trigger-less states always pass* — so an
early trigger-less state can hijack dialog starts. State 0 is index 0 and
trigger-less, which would predict every generic open landing on the dream.

**Evidence says it does NOT hijack in practice:** the palace meeting is opened by
`StartDialogNoSet` (`BDCUT04A.baf:12`) and demonstrably reaches the trigger-gated
state 8 (shipped SoD shows the palace conversation, not a dream); and comp190's
author bothered to `False()`-gate state 16 to remove it from *selection*, which
only makes sense if the scan reaches trigger-carrying states normally. Working
model: **trigger-less states 0/33/36/52 are reached only via scripted/targeted
entry, and the trigger-gated camp states (1/5) are what a camp click selects.**
`UNVERIFIED` — confirm in-game once a recruit path is wired; gating/removing
state 0 in the dream pass is the belt-and-suspenders fix and costs nothing.

---

## 4. Scripts

- **`BDSKIE.bcs` (override) — the real driver.** Blocks: BD0102 hostility +
  "hey, over here" nudge (`bd_skie_banter`, lines 28–61); `EscapeBD0102=1` → walk
  to `[401.728]` then `DestroySelf` (63–79, this is how she leaves the palace);
  BD2000 `bd_plot=293` → `StartDialogNoSet` (81–96, enters state 33); BD4000
  `bd_skie_plot` gated `StartDialogNoSet` (98–119) + chapter-11 `DestroySelf`
  (121–129) + `EscapeArea` at plot 10/15 (131–139); BD4100 `Dialog(Player1)`
  (141–150).
- **`BDSKIEC.bcs` — generic party combat AI only** (`BDAI_INIT_NPC`, potion use,
  find-traps/hide, attack loops). No recruitment logic. Applied when she joins.
- **`BDSDDSKI.baf` — beast vignette controller** (Chapter 8, `bd_sddskie` in
  MYAREA=BD7000): spawns Skie + a throwaway `BDCCREC2` (dagger, killed) + ogre
  `BDCCOGR1`, runs `bdcskie1` (she kills the ogre: *"And THAT's what happens when
  I don't get what I want."*), then her dialog states 63+. **Dead with BD7000
  (comp210).**
- **`BD7100.baf` — Bence confrontation** (Coast Way camp): spawns her, she
  `EquipMostDamagingMelee`, can jab/kill Bence (`SEQ_ATTACK_JAB`, *"the skills
  that saved your life from an ornery boar…"*), or leave; increments
  `bd_sddskie(BD7100)`. Cleaned up once `bd_bridgefort_plot>0`.
- **`BDCUT60Y.baf` — the dream** (`bdireni` casts, `VerbalConstant DYING`,
  `ChangeAnimation("bdskiedr")`, horror attacks Player1). Pure hooded-man content.

---

## 5. Soundset — BG1 vs SoD (the "BG1 swap")

CRE sound table read at **offset 0xA4** (100 dwords of strrefs) on all three
CREs, then each strref resolved to its WAV resref via `dialog.tlk`:

- **Both `BDSKIE.CRE` (SoD joinable) and `SKIE.CRE`/`SKIE6.CRE` (BG1) reference
  the same strref block 203891–203926 (+205335/205336).** Resolved samples:
  `203891→SKIEE02`, `203892→SKIEE04`, `203896→SKIEE07`, `203910→SKIEE25`,
  `203911→SKIEE26`, `203922→SKIEE36`, `205335→SKIEE38`, `205336→SKIEE39`
  (TLK flags=7 → sound present). **`SKIEE##` = BG1 Skie's original voice clips**
  (EET strref = BG1EE strref + 200000). Audio is BIF-resident — no loose
  `SKIEE*.wav` in `override\` or `lang\en_us\sounds\` (expected).
- **=> The SoD joinable already sounds like BG1 Skie.** A "BG1 soundset swap" is
  effectively already satisfied — no new audio to import.
- **Exact deltas (BDSKIE.CRE vs BG1 SKIE.CRE), if byte-identical is wanted:**
  - slot[2]: BDSKIE `203892` (SKIEE04) vs BG1 `203922` (SKIEE36)
  - BDSKIE has an extra slot[56]=`203922`; BG1 has none there
  - BG1 fills 5 extra slots BDSKIE leaves empty — slot[74]=`210207` (text-only,
    **no WAV**), slots[75-78]=`203908/203909/203910/203911` (select-rare/happy)
  - Concrete swap = `WRITE` SKIE.CRE's 400-byte sound table (`0xA4`..`0x234`)
    into BDSKIE.CRE. Trivial, but **likely unnecessary** — the deltas are a
    couple of battlecry/rare-selection variants, same actress.

---

## 6. Rework surface (what to gate / re-point / add) — DATA, not decisions

**Already handled (shipped):**
- Night visit (states 16–32 + BD0103 spawn) — comp190.
- Beast fight (states 63–83, BD7000) — comp210 (worldmap removal).
- Entar in city (palace context) — comp185 (Skie herself untouched).
- Assassination residue (tangential NPC lines) — comp195.
- BG1 soundset — already present (§5); optional byte-identical copy only.

**Must gate / re-point / add for clean talk-to-join:**
1. **Expose the existing camp join early.** States 5→6 / 1→2 already do
   `JoinParty()` gated to BD0120/BD0130. Minimal path = get her into the camp
   NPC pool (`bd_npc_camp`) at the chosen point, OR clone that short exchange to
   her first meeting.
2. **Re-point the palace meeting (8–15) from "leave" to "join,"** if the palace
   is the chosen spot — currently state 15 + `BDSKIE.baf:63-79` walk her out and
   `DestroySelf`. Replace departure with a join offer / camp-availability flag.
3. **Neutralise the plot chain** she currently rides to reach camp: BD2000 intro
   (spawns `BD2000.baf:901,920`; states 33–36), BD4000 subquest (static
   `BD4000.ARE` actor; states 37–62), BD4100 spawn (`BD4100.baf:550`), BD7100
   Bence dig (`BD7100.baf:562`; states 84–90). Drop/guard the spawns and confirm
   no non-Skie content reads their globals (`bd_skie_plot`,
   `bd_sddskie*`, `bd_plot 293/294`).
4. **Confirm state 0 doesn't shadow the recruit dialog** in-game after wiring
   (see §3 note).

**Depends on the epilogue / dream / hooded-man pass (out of scope here):**
- State 0 + `bdcut60y`/`bdcut60a` + `bdskiedr` "Unknowable Horror" (`bd_plot`
  590) — hooded-man/Irenicus removal.
- Skie's canonical **death + trial** (`BDSKIED.CRE`; `BD4100.baf:40` cleanup;
  `bd_skie_entar_caelar`/`bd_skie_plot` may feed the finale) — epilogue pass owns
  removing the death and any plot-var expectations.
- The **BDBENCE (Bence Duunton) arc** is shared plumbing; fully cutting it wants
  its own disentangle pass.

---

## 7. Open questions / UNVERIFIED

- **First-join beat in vanilla.** The only `JoinParty()` is the camp states, yet
  the subquest states end with her *leaving* (`EscapeArea`), not joining — so the
  flag that first makes her camp-recruitable is set later, most likely through
  the **BDBENCE 107–110** resolution (states 84–90). Not fully traced;
  `BDPARTY.bcs`/`BDVISIT.bcs` (the camp framework) not opened. Trace before
  replacing the entry, if the design wants to preserve any of the vanilla flow.
- **Trigger-less state-0 selection** vs. a camp/generic click — resolve in-game
  (§3).
- **Task brief vs. current decompile mismatch:** the brief's "crypt state 3" does
  not match this build — state 3 is a camp-dismiss reply; the first meeting is the
  **Ducal Palace** (states 8–15). "council states 12–14" ≈ the palace hub (state
  12 is the shared node). Flag for the design author so state numbers line up.
