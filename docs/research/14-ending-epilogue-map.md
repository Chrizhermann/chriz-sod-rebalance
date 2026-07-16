# 14 — SoD Ending / Epilogue Chain (verified state-machine map)

> Research data gathered 2026-07-10 and extended 2026-07-16; verified against repo
> decompiles, the dev EET install, and native standalone SoD resources.
> DATA ONLY — the approved disposition lives in
> `docs/plans/2026-07-16-post-victory-ending-design.md` and `docs/01-remix-wishlist.md`.

**Purpose:** the verified, link-by-link map of SoD's entire post-victory ending — Belhifet
victory → celebration → Skie's murder → arrest → imprisonment → trial → verdict → escape →
canon-party reunion → the Shadow-Thief ambush → the EET/BG2 handoff. The vanilla map remains
source evidence for the approved removal; it is not a statement that those beats currently ship
as removed. Every claim carries `file:line` evidence.

**Sources:** `research/data/sod_baf/*.baf` (repo's 1232 decompiled SoD scripts); EET glue
decompiled read-only from the dev install (`K#TELBGT.BCS`, `K#IMPORT.2DA`) into scratch;
`BDRUMOR3.dlg` decompiled from the dev install. Dev install = `…dev eet install\` (read-only).
The SoD scripts here are the **EET-imported** copies (K#-prefixed EET injections are baked into
`BD6100.baf` etc.). Native `BD6100.BCS` was also extracted/decompiled read-only from standalone
SoD on 2026-07-16, so §5 is now verified rather than inferred.

---

## 0. The spine — `bd_plot` state ladder (the whole chain in one table)

The global `bd_plot` ("global") is the master epilogue clock. It advances ~monotonically from
the Avernus descent (500) to the BG2 jump (700). Chapter is a parallel axis (`chptxt12`→12,
`chptxt13`→13). Values marked **(dlg)** are set in dialogue, not in any `.baf` (confirmed: the
`.baf` set contains no setter — only `BDDEBUG` mirrors them).

| `bd_plot` | Ch | Area(s) | Beat | Evidence |
|--:|:--:|---|---|---|
| 500 | →12 | BD4400 | Descend into Avernus. **+20,000/char**, `chptxt12`, `SaveGame(38)` | `BD4400.baf:29-52` |
| 510 | 12 | BD4500 | Avernus traversal | `BD4500.baf:28` |
| 555/560 | 12 | BD4601 → BD4700 | Approach Belhifet's arena | `BD4601.baf:5,319`; `BD4700.baf:7` |
| 560 | 12 | BD4700 | Caelar / Belhifet / Hephernaan confrontation (`bdcut57`/`57a`) | `BD4700.baf:1-9`; `BDCUT57.baf`, `BDCUT57A.baf` |
| 570 | 12 | BD4700 | **Belhifet defeated** — *"After all this time… this cannot be the end."* Door unlocks | `BD4700.baf:20-51` (strref 265535) |
| 577 | 12 | BDCAELAR/BDAUN | Caelar's fate resolves (`bd_caelar_fate` **(dlg)**; redeemed→`bdcaeld`) | `BDCAELAR.baf:68`; `BDAUN.baf:33`; `BD4700.baf:11-18` |
| 586/587 | 12 | BD4300 | Return to Dragonspear Castle courtyard | `BD4300.baf:184,198,1030` |
| **590** | 12 | BD4100 | **Celebration → sleep** (`bdcut60`→`60x`→`60a`); the Skie-murder "dream"; the Hooded Man is present | `BD4100.baf:82-124`; `BDCUT60.baf`, `BDCUT60X.baf`, `BDCUT60A.baf`; setter **(dlg)**, mirrored `BDDEBUG.baf:307-309` |
| **591** | 12 | BD4100 | Wake to Skie's corpse; every companion reacts; Bence Duncan opens the arrest dialog | `BD4100.baf:1-29,126-543` |
| — | →13 | **BDCUT61** | **Arrest / entry seam**: strip ALL companions → `bd_<name>_party_epilogue`; `chptxt13`; move to bd0112 | `BDCUT61.baf:1-245` |
| 600 | 13 | BD0112 | Prison cell block; guard escort (`bdcut61a`→`bdcut61t`) | `BD0112.baf:1-15`; `BDCUT61A.baf`, `BDCUT61T.baf` |
| — | 13 | **BD0035** | **The trial**: Duke Belt (`bdbelt`) presides; evidence flags from past deeds; verdict sets `bd_player_exiled` **(dlg)** | `BDCUT61T.baf:1-105` (bd0035 area script is empty) |
| 605 | 13 | BD0104 | Post-verdict: gear stripped into `Equipment_p1`/`Equipment_party`; thrown in holding cells | `BDCUT62.baf:1-94` |
| — | 13 | (cell) | **Hooded-Man / Irenicus dream** (`bdcut63`): *"…your power grows, child of Bhaal. Awake."* | `BDCUT63.baf` (strref 237719/265770) |
| 615 | 13 | BD0104 | Escape begins | `BD0104.baf:289-290` |
| 621/625/630/631 | 13 | BD0104 → BD0105 | Escape route + helper (thief `bdmercz` / Belt+`bdff1709`); secret door | `BDMERCZ.baf`; `BD0105.baf:6-59`; `BDCUT64.baf`, `BDCUT64A.baf`, `BDCUT64B.baf` |
| 640–664 | 13 | BD6000 | **Sewers escape**; Bence hunts you (*"Die in the name of Skie Silvershield!"*) on the non-exile branch | `BD6000.baf:34-159` |
| 660–671 | 13 | BD6200 | **Canon-party reunion**: Imoen2 + Minsc/Dynaheir/Khalid/Jaheira rejoin → `bdcut64x`→`bdcut65` | `BD6200.baf:228-276`; `BDCUT64X.baf`, `BDCUT65.baf` |
| 680 | 13 | **BD6100** | **"The Ambush"**: fog, Shadow Thieves (Mae'Var), party knocked out; movie `sodcin05` | `BD6100.baf:18-127` |
| 690 | 13 | BD6100 | Ambush resolves; **`CreateCreatureObject("K#TELBGT",Player1,…)`** | `BD6100.baf:31-127` |
| **700** | →SoA | — | `K#TELBGT`: bank gear → `K#ImportContainer`/`K#IMPORT`; `INTRO15F`; **`MoveToCampaign("SoA")`** | `K#TELBGT.BCS` (dev install) |

In vanilla, `bd_plot 590→671` carries the sleep/murder/arrest/jail/trial/escape/reunion band and
BD6100 carries 680→700. The approved remix instead retains the public BD4300 celebration at
plot 590, ends through Dazzo, and makes `BDCUT60` onward plus BD6100 unreachable. The preserved
EET invariant is the **destination** `BD6100*K#ImportContainer`, not physical entry into BD6100
(§4).

---

## 1. Link-by-link (with evidence)

### 1.1 Belhifet fight & victory — BD4700 (Avernus), chapter 12
- **Belhifet is the CURRENT final boss.** He is fought in `BD4700` (Avernus arena). Entering at
  `bd_plot 560` launches the confrontation cutscene `bdcut57`/`57a` where Belhifet orders Caelar
  to bring him the Bhaalspawn and Caelar turns on him (`BDCUT57.baf:20-134`,
  `BDCUT57A.baf:28` — *"Now, Caelar, my servant—prove yourself to me. Bring me the
  Bhaalspawn."*).
- **Caelar's fate** is carried by `bd_caelar_fate` (GLOBAL, set in dialogue): `1` = redeemed
  (she allies, then dies → corpse actor `bdcaeld`, `BD4700.baf:11-18`); `2/3` = Hephernaan
  (`bdhepher`) path (`BD4700.baf:20-42`). Either way **Belhifet is the one you kill.**
- His death sets `bd_plot 570` and barks strref 265535 *"After all this time… this cannot be the
  end. This cannot… be!"* (`BD4700.baf:44-51`). He summons scaled devil allies (abishai / erinyes
  / bone fiend / cornugon / hamatula) by difficulty (`BD4700.baf:53-99`).
- The **20,000/char + `chptxt12`** award is at the *descent* (`BD4400.baf:29-43`, `bd_plot 500`),
  not the kill. This is the last guaranteed chapter award in the game (see doc 03).

### 1.2 Return & celebration — BD4300 → BD4100 (`bdcut60`)
- `BD4300` (Dragonspear courtyard) runs the return at `bd_plot 586/587`.
- The **celebration** plays in `BD4100` (reclaimed Dragonspear castle) at `bd_plot 590`.
  `BDCUT60.baf` is the going-to-sleep beat: strref 266919 *"The celebrations last long into the
  night… you climb into your own bedroll, falling instantly into a deep sleep."* It seats the
  party as `SEQ_SLEEP`, flags the area `DREAMAREA`, creates the cutscene director `bdcutid`, and
  chains `bdcut60x` (`BDCUT60.baf:1-49`).
- **The launch of `bd_plot 590` + `bdcut60` is dialogue-driven.** `BDDELANC` state 77 sets
  `bd_plot=590`; its public victory chain runs through state 83 into `BDBENCE` 64–66. Sergeant
  Dazzo's two terminal routes (`BDDAZZO` states 2 and 3) both run `StartCutSceneMode()` and
  `StartCutSceneEx("bdcut60",FALSE)`. `BDDEBUG.baf:307-309` mirrors the same launch for QA.

### 1.3 The Skie murder ("dream") — `bdcut60x` → `bdcut60a`
- `BDCUT60X.baf` stages the dream: creates **`bdskie`** (Skie) and **`bdireni` (the Hooded Man =
  Irenicus)**; the Hooded Man **takes the party dagger `dagg10`** (the murder weapon) and opens
  dialogue (`BDCUT60X.baf:16-27`). This is the framing: Irenicus/Slayer makes the PC *appear* to
  murder Skie.
- `BDCUT60A.baf` executes it: the "Unknowable Horror" `bdskiedr` dies and swaps animation to
  `bdskied` (**Skie's corpse**); the PC is `BDSLOW`'d, dragged to the body, and plays `SEQ_DIE`
  as the "killer" (`BDCUT60A.baf:18-56`). Journals 259854 / 266909. See doc 09 for the cosmetic
  Ring/`bdskiedr.itm` thread that ties the four rest-dreams to this finale.

### 1.4 Wake & arrest — `bdcut60a` tail → `BDCUT61`
- The party wakes; **Bence Duncan** (`bdbence`) + Flaming Fist arrive (*"What the hells—? No—gods,
  NO!"*, strref 239372) and Bence opens the arrest dialogue (`BDCUT60A.baf:97-121`).
- `bd_plot 591` fires every companion's horror bark (`BD4100.baf:126-522`); evil/low-rep variants
  differ; **Viconia, M'Khiin, Baeloth leave the party outright** (`LeaveParty`+`EscapeArea`).
  Corwin (or Bence, if she's gone/dead) opens the transition dialogue (`BD4100.baf:524-543`).
- **`BDCUT61` is the arrest seam** (§6): it removes **every** joinable — records
  `bd_<name>_party_epilogue=1` and `DestroyAllFragileEquipment` for Aura, `L#BRIST` (mod), Corwin,
  Jaheira, Khalid, Minsc, Dynaheir, Glint, Rasaad, Baeloth, Viconia, Voghiln, M'Khiin, Edwin,
  Safana, Dorn, Neera + generic Player2-6 — then `LeaveAreaLUA("bd0112")`, `IncrementChapter
  ("chptxt13")`, journal 256378, `bd_npc_camp_chapter=7` (`BDCUT61.baf:1-245`). **No XP.**

### 1.5 Imprisonment — BD0112 → `BDCUT61A` → `BDCUT61T`
- `BD0112` forces `chapter=13`, sets `bd_plot 600`, launches `bdcut61a` (`BD0112.baf:1-15`).
- `BDCUT61A` seats the party, takes **weapons** into `bdimoitm` (Imoen's item-carrier creature),
  marches them past guards, and chains `bdcut61t` (`BDCUT61A.baf:1-76`).

### 1.6 Trial — BD0035 (`bdcut61t`); Entar's role
- `BDCUT61T` moves the party + `bdimoitm` into **`bd0035`** (the trial hall), gathers the
  `witness` + guards, and hands the scene to **Duke Belt** (`bdbelt`, `StartDialog
  "Commoner_talk1"`) (`BDCUT61T.baf:1-105`). **`bd0035`'s own area script is empty** (1 line) —
  the trial is entirely cutscene- + dialogue-driven.
- The trial reads **evidence flags from past deeds**, set in `BDCUT61T` from prior globals:
  `bd_madele`, `bd_poison`, `bd_illness`, `bd_traitor` (`SDD303_executed`), `bd_thrix`,
  `bd_paladin` (PC is a paladin), `bd_reputation` (rep >16 or <6) (`BDCUT61T.baf:21-83`).
- **Entar Silvershield** (`BDENTAR`) is Skie's father. He does **not** appear as a speaking actor
  inside the trial cutscenes; the on-stage accusers are Duke Belt, **Duke Eltan** (`bdeltan`),
  the witness, and **"Entar Guard 1/2"** + `bdff1697` (destroyed in `BDCUT62.baf:5-14`). Entar's
  live `.cre`/`.dlg` are used in the **chapter-7 Ducal Palace** scene, not here (§4, §6).
- **Verdict:** the trial dialogue sets **`bd_player_exiled`** (0 = convicted→escape branch; 1 =
  exiled branch). Not set in any `.baf` (dialogue-only) — it forks BD6000 / BDCUT64 downstream.

### 1.7 Holding & the Irenicus dream — `BDCUT62`, BD0104, `BDCUT63`
- `BDCUT62` (post-verdict): moves `bdimoitm` to `bd0104`, then **banks the party's whole
  inventory** — `Equipment_p1` takes ALL from `bdimoitm`+Player1; `Equipment_party` takes ALL
  from Player2-6 (`BDCUT62.baf:23-74`) — destroys the trial actors, throws the party into the
  holding cells (`bd0104`), sets `bd_plot 605`, `SaveGame(39)` (`BD0104.baf:111-118`).
- **`BDCUT63` = the Hooded-Man/Irenicus dream in the cell**: PC plays `SEQ_DIE`, movie `sodcin03`,
  `bdireni` says strref 237719 *"Curious. Your mind is not so open to me as it once was—you resist
  my will. Your power grows, child of Bhaal."* then 265770 *"Awake."* and opens dialogue
  (`BDCUT63.baf:1-22`). This is the endgame's on-screen hooded-man scene.
- **Note — BD0104 is DUAL-USE.** The same area is the chapter-7/8 Coalition/refugee/Tiax cell
  block (`BD0104.baf:60-99`, incl. the `AddexperienceParty(1000)` **Tiax-invite** award gated
  `chapter<9` — *not* an epilogue award) AND the chapter-13 jail. Removing the jail use must not
  damage the early-game use.

### 1.8 Jailbreak / escape — BD0104 → BD0105 → BD6000
- Escape route runs bd0104→bd0105 (`bd_plot 615/621/625/630/631`), gated on a helper contact.
  **Two branches** (by `bd_player_exiled`): the thief **`bdmercz`** opens the way on the
  convicted branch (`BDCUT64.baf:64-82`, `BDMERCZ.baf`), or **Belt + `bdff1709`** on the exile
  branch (`BDCUT64.baf:140-164`, `BDCUT64A.baf`). `BDCUT64` also seeds **BG2 starter gear**
  (basic long swords + small shields into `Sword1/2`,`Shield1/2`) and plays movie `restdung`.
- `BD6000` = the **sewers** escape (`bd_plot 640-664`). On the non-exile branch Bence Duncan
  turns hostile and hunts the PC (*"…Die in the name of Skie Silvershield! Kill h**/her**!"*,
  `BD6000.baf:121-141`); Corwin may aid (`bdschae2`). `BDCUT64B` bridges bd0105→bd6000.
- **Pursuit mobs** (the "avenge Skie" encounters spawned across the escape): `BDFIST60`,
  `BDFISTCE`, `BDCHAINS`, `BDSTONE`, `BDSEWER` all bark *"Justice for Silvershield!"* /
  *"no mercy for Skie Silvershield's killer"* (grep hits in each).

### 1.9 Canon-party reunion — BD6200 (`bdcut64x` → `bdcut65`)
- `BD6200` (`bd_plot 660-671`) resurrects **Imoen2** (`bdresurr`+`bdrejuve`, `BD6200.baf:228-253`)
  and, if their `bd_<name>_party_epilogue` global is set, re-homes **Minsc, Dynaheir, Khalid,
  Jaheira** as the canonical BG2 opening party (`BD6200.baf:28-226`). **Only these five** are
  reassembled — every SoD-only companion stripped at BDCUT61 stays gone.
- `bd_plot 670→671` → `bdcut64x`. `BDCUT64X` is the JoinParty sequencer (adds Imoen2, then each of
  Minsc/Dynaheir/Khalid/Jaheira one by one, re-looping the cutscene) then chains `bdcut65`
  (`BDCUT64X.baf:1-150`).
- `BDCUT65` moves the party from bd6200 into **`bd6100`** and lets Imoen2 open the finale dialogue
  (`BDCUT65.baf:1-61`). **This is the "exit BD6200" seam** → BD6100.

### 1.10 The Ambush & BG2 handoff — BD6100 → `K#TELBGT` (§4)
- `BD6100` "The Ambush" (`bd_plot 680`): fog, the Shadow Thieves `bdfinal1-5` (Mae'Var named,
  strref 239808-239809 *"Load them onto the cart… Our client is anxious to have his prize."*),
  companion death-barks (Khalid/Jaheira/Minsc/Dynaheir), the party is slept/knocked out
  (`bdsleep`/`bdfinal`), movie `sodcin05` (`BD6100.baf:18-127`). When all six are down
  (`bd_finale`→5, `BD6100.baf:681-687`) it fires **`CreateCreatureObject("K#TELBGT",Player1,…)`**
  (`BD6100.baf:126`) → the EET jump.

---

## 2. Who's the Hooded Man / Irenicus, and every hooded-man beat

`bdireni` = the Hooded Man = Irenicus. Endgame appearances that a full removal must handle:
- **`BDCUT60X`** — present at the Skie-murder dream, takes the murder dagger `dagg10`.
- **`BDCUT63`** — the cell dream (*"your power grows, child of Bhaal"*).
- **`BD4100.baf:31-45`** — an EET cleanup block destroys `BDIRENI` (+`BDBENCE`,`BDSKIED`) once
  `Chapter>13`, i.e. the hooded-man actor is a live BD4100 object.
- **Mid-campaign** hooded scenes and the four rest-dreams are catalogued in **doc 09**; CLAUDE.md's
  verified finding: mid-campaign hooded scenes set nothing the endgame reads (safe to remove).
- **`BDRUMOR3.dlg` (tavern rumors, ch 8/9/10)** — coupled foreshadowing residue, e.g. ch8
  strref 267030 *"There was a hooded fellow here asking about you… the scars, and the voice…
  Something really… off."*; ch9 seeds Bhaal-temple rumors (267038). Removing the hooded man
  orphans these lines (they only add journal entries; no plot gate).

---

## 3. XP / chapter / autosave surface inside the chain

- **BD4400** — `chptxt12` + **20,000/char** (`AddXPObject` ×6), `SaveGame(38)` (`BD4400.baf:33-52`).
  The only guaranteed award in the tail; it is at the Avernus *descent* (bd_plot 500).
- **BDCUT61** — `chptxt13`, **no XP** (`BDCUT61.baf:241`).
- **BD0104:78** — `AddexperienceParty(1000)` is the **chapter-<9 Tiax-invite** award (dual-use
  area), **NOT** part of the epilogue.
- **`SaveGame(39)`** at chapter-13 entry (`BD0104.baf:111-118`). No other awards anywhere in
  590→700. (Confirmed by grep of the full cutscene/area set.)

---

## 4. The actual EET invariant — VERIFIED with evidence

**Vanilla sends the party through BD6100, but BG2 only hard-requires the gear in
`BD6100*K#ImportContainer`.** Verified chain:
1. `BD6100.baf:126` `CreateCreatureObject("K#TELBGT",Player1,0,0,0)` (after the party is knocked
   out, `bd_finale`=5).
2. **`K#TELBGT.BCS`** (decompiled from dev install) does, in order:
   - Captures BG1-NPC stats via EEex Lua (`K_FP_CaptureStats(...)` for Branwen/Xan/Ajantis/
     Yeslick/…), gated on `InPartyAllowDead`.
   - Sweeps **named legacy items** (Golden Pantaloons `MISC47`, Twinkle/Icingdeath, Kazgaroth's
     Horn/Claw, Helm of Balduran, all BG1/SoD uniques + `C0AU*` Aura items) into the **`K#IMPORT`
     store** (`AddStoreItem("K#IMPORT",…)`).
   - Banks the **entire remaining inventory** of Player1-6 into **`K#ImportContainer`**
     (`TakeCreatureItems(PlayerN,ALL)`), rests the party (`K#REST`/`K#UNREST`), removes Player2-6.
   - `GivePartyAllEquipment()`, `SetGlobal("bd_plot","GLOBAL",700)`, forces
     `SPRITE_IS_DEADKHALID/DYNAHEIR=1` (they die canonically in the ambush), `StartMovie
     ("INTRO15F")`, then **`MoveToCampaign("SoA")`** + `DestroySelf`.
   - Reads **`ENDOFBG1`** to gate the BG1-NPC (C#Ajantis…) blocks — confirming that global is
     load-bearing.
3. `K#IMPORT.2DA/.ITM/.STO` are the named-item vaults the BG2 side restores from. The installed
   `AR0602.BCS` independently moves the ordinary inventory from the exact source
   `BD6100*K#ImportContainer` into its local import container. It does not test that the party
   ever visited BD6100.

**NEVER-modify (restated, with why):**
| File / global | Role | Evidence |
|---|---|---|
| `K#TELBGT.BCS` | Runs the banking + `MoveToCampaign("SoA")` | decompiled (dev install) |
| `K#TELBGT.CRE` | Carrier created in BD6100 to run that script | `BD6100.baf:126` |
| Existing `BD6100*K#ImportContainer`, `K#IMPORT.STO/.ITM/.2DA` | The cross-campaign gear vaults | `K#TELBGT.BCS`; installed `AR0602.BCS` |
| `K#REST.SPL` / `K#UNREST.SPL` | Sleep/wake used by the handoff | `BD6100.baf:84-89`; `K#TELBGT.BCS` |
| `AR0602.BCS` | BG2-side reader; hardcodes BD6100 gear source | decompiled dev install |
| `CAMPAIGN.2DA` / `STARTARE.2DA` | Campaign routing | CLAUDE.md (inherited); third-party mods patch |
| `ENDOFBG1` (global) | Gates BG1-NPC import logic | `K#TELBGT.BCS` |

**Approved resolution:** add a local `K#ImportContainer` to BD4300; clone the currently installed
`K#TELBGT.BCS/.CRE` at tail-install time; run the clone from BD4300; and patch only the clone to
move `BD4300*K#ImportContainer` into `BD6100*K#ImportContainer` before its normal campaign move.
This preserves every installed item sweep and stat-capture addition while never moving the party
into or displaying BD6100; the cross-area action may still serialize its destination container.
Original K# resources, AR0602, BD6100, campaign tables, and `ENDOFBG1` remain untouched. A missing
local container must fail closed before banking so an already-baked BD4300 save cannot lose gear.

---

## 5. Standalone (non-EET) SoD end path — verified

- This decompile is the **EET** copy: the `K#*` actions are EET injections baked into
  `BD6100.baf`. The base-game beats (fog → Shadow-Thief ambush → knockout → movie `sodcin05`)
  are the shared SoD content; the EET-only tail is `CreateCreatureObject("K#TELBGT",…)` →
  `MoveToCampaign("SoA")`.
- On **standalone** BG:EE+SoD (no BG2), both native BD6100 terminal paths run
  `EndCutSceneMode()`, `ContinueGame(FALSE)`, and `EndCredits()` after the ambush/movie. There is
  no `K#TELBGT` or `MoveToCampaign`.
- Verified 2026-07-16 by extracting and decompiling native `BD6100.BCS` from standalone SoD.
  The approved replacement calls the native campaign-termination actions from Dazzo in BD4300;
  it does not load BD6100 or replay `sodcin05`.

---

## 6. Removal surface — everything a full epilogue cut must re-home or re-time

**Approved live seam:** preserve `BDCUT59/59A/59B` and the short public celebration in BD4300.
Dazzo replaces both `BDCUT60` launches with the platform endpoint. Murder/arrest roots plus
production/debug launchers into the retired band are false-gated, making `BDCUT60` onward and
BD6100 unreachable. Retired resources remain on disk as inert, reversible content.

**Areas made unreachable:** BD4100, BD0112, **BD0035** (trial — empty area script), the
chapter-13 use of BD0104, BD0105, BD6000, BD6200, and BD6100. BD0104 itself is **DUAL-USE**:
its earlier Coalition/refugee/Tiax content remains byte-for-byte intact. BD4300 remains live.

**Cutscenes made unreachable:** `BDCUT60`, `60X`, `60A`, `60B`, `60Y`; `BDCUT61`, `61A`, `61T`;
`BDCUT62`; `BDCUT63`; `BDCUT64`, `64A`, `64B`, `64X`; `BDCUT65`; and the BD6100 ambush machine.
**Preserve live:** `BDCUT59`, `59A`, `59B`. Clone the installed K# handoff for EET; never edit
the original.

**Companions:** all stripped at `BDCUT61` (18 `bd_<name>_party_epilogue` globals). Only the canon
5 (Imoen/Minsc/Dynaheir/Khalid/Jaheira) reassemble at BD6200. SoD-only joinables (Corwin, Glint,
Rasaad, Baeloth, Viconia, Voghiln, M'Khiin, Edwin, Safana, Dorn, Neera, Aura, `L#BRIST`) simply
vanish. Their only "ending talk" is the horror bark at `bd_plot 591` (`BD4100.baf:126-522`).
Under the approved route BDCUT61 never launches, so the current party—including Skie, Imoen,
and mod NPCs—remains assembled until the platform handoff and no horror bark fires.

**Entar Silvershield coupling and resolution:**
- `BDENTAR.CRE` + `BDENTAR.dlg` exist in the dev override. **They are used in the chapter-7 Ducal
  Palace scene** (`BD0102.baf:31-268`, and `BDPALACE.baf:58-64`), which **introduces Skie and her
  father** — *not* only the trial. **Deleting `BDENTAR.cre/.dlg` therefore breaks BD0102/BDPALACE
  unless that scene is also removed/rehomed.** Component 185 has since removed the BD0102 Entar
  spawns/staging; the approved ending cleanup false-gates the last live `BDPALACE.BCS` reference.
  `BDENTAR.CRE/.DLG` remain inert rather than being destructively deleted.
- Trial guards: **`bdff1697`** ("BDGU1697") + "Entar Guard 1/2" (`BDCUT62.baf:5-14`) — trial-only,
  safe to drop with the trial.
- Journal residue naming Entar: `BD0120.baf:7551-7576` (BG1 "Rise of Sarevok" erase-block — a
  *different*, BG1-era context; do not conflate).

**Hooded-man residue resolution:** false-gate `BDRUMOR3` states 7/20/37; the `BDIRENI` actor and
`bdcut60x`/`bdcut63` are unreachable; component 130 already suppresses the four rest-dreams.

**Pursuit-mob scripts:** `BDFIST60`, `BDFISTCE`, `BDCHAINS`, `BDSTONE`, `BDSEWER` ("avenge Skie").

**Key globals in the band:** `bd_plot` 590-671; `bd_player_exiled` (verdict fork, dlg-set);
`bd_skie_plot`; the 18 `bd_<name>_party_epilogue`; `bd_finale`/`bd_dream_plot`/`bd_corwin_body_ot`.

---

## 7. Design questions — one open, the ending mechanics resolved

1. **Belhifet placement (parked on the wishlist).** Today Belhifet is the ch12 final boss
   (`BD4700`) and Caelar is redeemed/sacrificed (`bd_caelar_fate`). The remix wants **Caelar as
   the main antagonist & final boss** — so: keep Belhifet as a fight *before* Caelar, or have
   Caelar *defeat/replace* Belhifet in a scene (Belhifet defeated by Caelar)? This reshapes
   BD4700 + BDCUT57/57A + `bd_caelar_fate`.
2. **Resolved — ambush:** remove it entirely; no re-motivation. EET uses the container invariant.
3. **Resolved — handoff:** Dazzo runs the installed K# clone from BD4300; the bank moves across
   areas, while BG2 recreates its own opening party normally.
4. **Resolved — Skie/Entar:** Skie survives in the party; Entar's last live reference is gated;
   retired files remain inert.
5. **Resolved — BD0104:** preserve all earlier Coalition/refugee/Tiax content; chapter-13 use is
   unreachable.
6. **Resolved — verdict:** fully cut; no exile/escape flavor remains.
7. **Resolved — production trigger:** BDDELANC 77 sets plot 590; BDDAZZO states 2/3 launch
   BDCUT60. Both Dazzo endpoints are replaced; the debug launcher is retired.
8. **Resolved — standalone:** native termination is verified and called directly from Dazzo.
