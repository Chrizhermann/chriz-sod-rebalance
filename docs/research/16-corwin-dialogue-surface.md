# 16 — Corwin (Schael Corwin) dialogue surface census

> Research data gathered by subagent 2026-07-10; verified against dev install decompiles.
> DATA ONLY — decisions live in `docs/design/` and `docs/01-remix-wishlist.md`.

Scope: enumerate Corwin's complete player-facing dialogue surface to size a future full
rewrite. Counts are from WeiDU 24600 decompiles of the **dev EET install** override
(post comp150/160/180/185/190/195 — i.e. the current remix state), copied out to scratch.
"SAY" = a line Corwin speaks; "REPLY" = a CHARNAME player-choice line; "VO" = SAY lines
carrying a `[BDxxxxx]` sound resref (droppable per mod rules, but counted).

## 1. File inventory

Dialog map rows (`PDIALOG.2DA` / `BDDIALOG.2DA` / `INTERDIA.2DA`), CORWIN:
`POST=BDCORWIN · JOIN=BDCORWIJ · DREAM=BDCORWID · INTERDIA=BDCORWIB`.

| File | Function | Exists | States | SAY | REPLY | VO (of SAY) | EXTERN |
|---|---|---|---:|---:|---:|---:|---:|
| **BDSCHAEL.dlg** | Pre-join **world + city-escort** (her `BDSCHAEL.CRE` dialog; she is a non-party escort through the city chapter) | yes | 284 | 284 | 443 | 89 (31%) | 42 |
| **BDCORWIN.dlg** | In-party **plot / camp hub** (assigned on join for the march) | yes | 57 | 57 | 83 | 14 (25%) | 17 |
| **BDCORWIJ.dlg** | **Interjection + banter + romance** reservoir (EXTERN'd from area/party dialogs; 171 EXTERNs) | yes | 335 | 335 | 321 | 208 (62%) | 171 |
| BDCORWIB | INTERDIA banter-timer file | **NO** | — | — | — | — | — |
| BDCORWID | Dream script (`DREAM_SCRIPT_FILE`) | **NO** | — | — | — | — | — |
| **TOTAL** | | | **676** | **676** | **847** | **311 (46%)** | 230 |

- **BDCORWIB and BDCORWID do not exist** in the override — Corwin has **no dedicated
  banter-timer file and no dream**. Her banters live inside BDCORWIJ (she initiates there;
  cross-NPC banters EXTERN into it). Both 2DA references are inert dangling entries.
- Non-dialog resources (for reference, not in scope): `BDSCHAEL.CRE`, scripts
  `BDSCHAEL.bcs` / `BDCORWIN.bcs` / `BDCORWIC.bcs`, plus `CORWIN7.CRE`, `CORWYVRN.CRE`.

## 2. Remix touches already applied (live on dev)

All confirmed present as `False()` / re-routes in the dev decompile.

| Component | Target | Mechanism | Effect on surface |
|---|---|---|---|
| 150 `csrcncl.d` | BDSCHAEL 46 DO 1 | `False()` | dead reply #267279 (assassination return-prompt) |
| 150 `csrcncl.d` | BDSCHAEL 162 DO 4 | `False()` | dead reply #234704 (Elfsong "someone tried to kill me") |
| 150 `csrcncl.d` | BDSCHAEL **21** | orphaned via `BDBELT 40.2` gate | state 21 ("keep assassination attempts to a minimum") unreachable |
| 195 `csr195.d` | BDSCHAEL 167 DO 0 | `False()` | dead reply #254918 → orphans **state 168** ("assassins Caelar sent after you") |
| 195 `csr195.d` | BDSCHAEL **227** reply 0 | `ALTER_TRANS` (moves `BD_plot=54` commit + EXIT) | skips **state 228** goodnight ("crusader poison" line); 228 orphaned |
| 195 `csr195.d` | BDCORWIN 11 DO 1 | `False()` | dead reply #242095 ("Caelar nearly killed me and my friend Imoen") |
| 150 (event) | BDSCHAEL **1–~9** | palace assassination-night **removed** | rescue-arrival states no longer reachable (not individually gated) |

**Vanilla (pre-existing) dead, not remix:** BDSCHAEL WEIGHT#6 + WEIGHT#41 states (2 `False()`),
BDCORWIJ `BD_Sacrifice_Corwin` branch (1 `False()`). No remix component touches **BDCORWIJ** at all.

## 3. Thematic buckets — BDSCHAEL (284, world/city-escort)

| States | Bucket | Status |
|---|---|---|
| 0 | Wilderness rest-nag | live |
| 1–9 | **Palace assassination-night rescue** (attack, Imoen wounded, Fenster, cleric) | **dead** (event removed by 150) |
| 10–21 | Council-assemble bridge + "keep civil tongue"/escort-downstairs | mostly orphaned (21 gated); reachability of 10–20 depends on re-pointed council entry — flag for rewrite |
| 22–31 | Palace departure framing (Ophyllis basement gold, "leave at first light") | live |
| 32–123 | **City-escort recruitment web** — Garrick/Safana/Coran @ Elfsong, Tiax @ jail, Minsc/Dynaheir @ Three Old Kegs, Rasaad @ Iron Throne; crowd/cutpurse/Sundries barks | live, **heavily duplicated** (many near-identical re-entry variants) |
| 124–153 | **Elfsong "tell me about yourself"** — father Audamar, Skie parallel, "keep it professional", Caelar backstory | live (character beat, partly voiced) |
| 154–180 | More escort tag-along variants ("I'll follow you out", hamster joke) | live, duplicative |
| 181–190 | **Sundries "conspirators/treason"** mini-quest (arrest traitors) | live |
| 191–224 | Recruit wrap-ups (Elfsong/jail/Iron Throne tour, "memories here") | live, duplicative |
| 225–247 | March-prep + goodnight + final departure (Quartermaster Belegarm, Eltan's gold, "caravan's at the gate") — **227/228 = remix re-route** | live (228 orphaned) |
| 248–266 | **Rohma daughter goodbye** (her most personal beat) | live (voiced) |
| 267–283 | Crowd-confrontation interjection (urchins) + recruit-location info dumps | live |

## 4. Thematic buckets — BDCORWIN (57, in-party plot/camp hub)

| States | Bucket | Status |
|---|---|---|
| 0–9 | Recruit / dismiss / rejoin micro-lines + guard rationale | live |
| 10–13 | Rest / scout small-talk ("You want to turn back?" — **11.1 gated**) | live |
| 14–23 | Coast Way → Bridgefort march (thunder at crossing, Bence/Duncan, "spoke to Argent?") | live |
| 24–37 | Crusade coordination / Bridgefort siege (Barghest, mobilize) | live |
| 38–46 | Caverns + Boareskyr aftermath (de Lancie, "make yourself scarce") | live |
| **47–52** | **Trial / arrest block** ("headsman's axe", "No. NO. This can't be") | **dies with epilogue pass** (not yet gated) |
| 53–56 | Joined hub ("What do you need?") / dismiss | live |

## 5. Thematic buckets — BDCORWIJ (335, interjections/banter/romance)

| States | Bucket | Status |
|---|---|---|
| 0–22 | Camp / Thayan-wizard confrontations + wander-off / rest interjections | live |
| 23–46 | **Boareskyr parley with Caelar** (drow-along objection, "only chance to talk to Caelar", "Revenge?") | live |
| 47–72 | Bridgefort siege / caravan + **Glint-unmasking** ("Gardnerson's not on the list") | live |
| 73–78 | Chicken/dog vignette, Barghest lore | live |
| **79–114** | **Beno Famari personal-quest arc** — ex-lover, Rohma's conception/parentage, confrontation + resurrection, "real love came with Rohma" | live (major character content) |
| 115–130 | Cavern/underground interjections (Butcher of Barrow, wyrmlings) | live |
| 131–144 | Bridgefort-betrayal aftermath / Marshal Nederlok scolding | live |
| 145–161 | **Skie rescue at the castle** ("did Skie leave willingly?", father-let-me-fall) | live |
| 162–196 | **Dragonspear Castle assault + Hell** (Hephernaan, catapult, portal, Belhifet, "you wager my soul?") | live (scope depends on later chapter cuts) |
| **197–202** | **Trial mirror** (duplicate of BDCORWIN 47–52) | **dies with epilogue pass** |
| 203–230 | Caverns puzzle interjections (rat/blackthorn, firebreath-potion distraction) | live |
| 231–253 | **Child-of-Bhaal suspicion** ("Are you a child of Bhaal?", Sarevok rumors, "blood will tell") | live |
| 254–308 | **Romance arc** (attraction, children, Rohma-vs-you choice, commit/breakup + jealousy variants, "I want to kiss you") | live (highest quality-sensitivity) |
| 309–335 | Combat aftermath + **Voghiln matchmaking** (silver earrings) + evil-party/goblin/lich interjections | live |

## 6. Rewrite scope estimate

**Gross Corwin voice:** 676 SAY lines (BDSCHAEL 284 / BDCORWIN 57 / BDCORWIJ 335), plus 847
CHARNAME REPLY lines if the player side is also reworded. 311 SAY (46%) currently carry VO,
which a text rewrite sheds (acceptable per mod rules).

**Not part of a live rewrite (~31 SAY):** BDSCHAEL 1–9 assassination rescue (dead), the two
trial blocks BDCORWIN 47–52 + BDCORWIJ 197–202 (~12, die with epilogue), plus the 3 already
`False()`-gated replies. → **LIVE Corwin SAY today ≈ 645** (BDSCHAEL ~264 / BDCORWIN ~51 /
BDCORWIJ ~329).

**Realistic unique load ≈ 500–540 lines.** BDSCHAEL's city-escort web (states 32–224) is the
big deflator: dozens of near-identical re-entry variants of the same 4–5 recruit pitches
(Safana/Coran, Minsc/Dynaheir, Rasaad, Tiax) collapse to ~130–150 unique meaningful lines,
not ~200.

**Biggest / highest-value buckets to rewrite (priority order):**
1. **BDCORWIJ (~335)** — romance arc (254–308), Beno personal quest (79–114), child-of-Bhaal
   suspicion (231–253), and parley/camp interjections. This is the core of the "her writing
   is poor" complaint and the most voiced (62%).
2. **BDSCHAEL character beats** — Elfsong backstory (124–153, ~30) and Rohma goodbye
   (248–266, ~19) carry her characterization; the surrounding escort web is high-volume but
   low-uniqueness (mechanical recruit routing).
3. **BDCORWIN (~51)** — functional, short plot/camp hub; lightest lift.

**Limitation:** interjection *entry triggers* live in area/party dialogs (BD0110/BD0120/…,
other NPCs' files) that EXTERN into BDCORWIJ; those inbound hooks were not enumerated here
(would require decompiling the full dialog set). The interjection *content* is fully contained
in BDCORWIJ's 335 states above.
